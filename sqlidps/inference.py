import html
import importlib.resources as resources
import importlib.util
import re
import sys

import numpy as np

import sqlidps.sql_tokenizer as sql_tokenizer


def get_package_file(filename: str) -> str:
    with resources.path("sqlidps", filename) as path:
        return str(path)


model_path = get_package_file("model.npz")


def decode_encodings(text: str) -> str:
    assert isinstance(text, str)
    try:
        text = text.replace("\\", "\\\\")
        text = text.encode("utf-8").decode("unicode_escape")
    except Exception as e:
        return ""
    text = re.sub(
        r"%([0-9A-Fa-f]{2})", lambda m: bytes.fromhex(m.group(1)).decode("latin1"), text
    )
    text = re.sub(r"[Uu]\+([0-9A-Fa-f]{4,6})", lambda m: chr(int(m.group(1), 16)), text)
    text = html.unescape(text)
    return text


class Inference:
    def __init__(self, model_path="model.npz"):
        data = np.load(model_path, allow_pickle=True)
        keys = data["vocabulary_keys"]
        vals = data["vocabulary_vals"]
        self.vocabulary_ = {k.lower(): int(v) for k, v in zip(keys, vals)}
        self.inv_vocabulary_ = {v: k.lower() for k, v in self.vocabulary_.items()}
        self.idf_ = data["idf"]
        self.classes_ = data["classes"]
        self.trees_ = []
        for i in range(len(data["children_left"])):
            self.trees_.append(
                {
                    "children_left": data["children_left"][i],
                    "children_right": data["children_right"][i],
                    "feature": data["feature"][i],
                    "threshold": data["threshold"][i],
                    "value": data["value"][i],
                }
            )

        self.tokenizer = sql_tokenizer
        self.debug =False 

        if self.debug:
            print(f"Loaded vocabulary size: {len(self.vocabulary_)}")
            sample_keys = list(self.vocabulary_.items())[:10]
            print(f"Sample vocab items (lowercase key -> idx): {sample_keys}")
            print(f"IDF vector length: {len(self.idf_)}")
            print(f"Classes: {self.classes_}")
            print(f"Number of trees: {len(self.trees_)}")

    def _transform(self, docs):
        n_docs = len(docs)
        n_feats = len(self.idf_)
        X = np.zeros((n_docs, n_feats), dtype=float)

        for i, doc in enumerate(docs):
            tokens = self.tokenizer.tokenize(doc)
            if self.debug:
                print(f"\nDocument {i}: '{doc}'")
                print(f"Tokens: {tokens}")

            tf = {}
            for t in tokens:
                key = t.lower()
                idx = self.vocabulary_.get(key)
                if idx is not None:
                    tf[idx] = tf.get(idx, 0) + 1
            if self.debug:
                matched = {self.inv_vocabulary_[k]: v for k, v in tf.items()}
                print(f"Term frequencies (matched): {matched}")

            vec = np.zeros(n_feats, dtype=float)
            for idx, cnt in tf.items():
                vec[idx] = cnt * self.idf_[idx]
            if self.debug:
                nonzero = np.nonzero(vec)[0]
                print(
                    "Non-zero TF-IDF entries:",
                    {self.inv_vocabulary_[i]: vec[i] for i in nonzero},
                )

            norm = np.linalg.norm(vec)
            if self.debug:
                print(f"Vector norm before normalization: {norm}")
            if norm > 0:
                vec /= norm
            if self.debug:
                print(
                    "Normalized vector values:",
                    {self.inv_vocabulary_[i]: vec[i] for i in nonzero},
                )

            X[i] = vec
        return X

    def _predict_tree(self, x, tree):
        node = 0
        while True:
            left = tree["children_left"][node]
            right = tree["children_right"][node]
            if left == right:
                return np.argmax(tree["value"][node])
            feat = tree["feature"][node]
            thresh = tree["threshold"][node]
            node = left if x[feat] <= thresh else right

    def predict(self, docs):
        X = self._transform(docs)
        preds = []
        for i, x in enumerate(X):
            votes = np.zeros(len(self.classes_), dtype=int)
            for tree in self.trees_:
                cls_idx = self._predict_tree(x, tree)
                votes[cls_idx] += 1
            probs = votes / len(self.trees_)
            if self.debug:
                print(f"Votes for doc {i}: {votes}")
                print(f"Probability estimates: {probs}")
            pred_idx = np.argmax(votes)
            preds.append(self.classes_[pred_idx])
        return np.array(preds)


class PotentialSQLiPayload(Exception):
    def __init__(self, message="You have a Potential SQL payload in your data"):
        self.message = message
        super().__init__(self.message)


pipeline = Inference(model_path=model_path)


class SQLi:
    @staticmethod
    def _classify(text):
        prediction = pipeline.predict([decode_encodings(text)])
        if prediction[0] == 1:
            raise PotentialSQLiPayload(f"{text} is a potential payload.")
        else:
            return prediction[0]

    @staticmethod
    def check(data):
        if isinstance(data, str):
            SQLi._classify(data)
        elif isinstance(data, list):
            for value in data:
                SQLi._classify(value)
        elif isinstance(data, dict):
            for value in data.values():
                SQLi._classify(value)

    @staticmethod
    def parse(data, error="potential payload"):
        assert isinstance(data, dict), "Dictionary expected"
        cleaned = {}
        for key, value in data.items():
            try:
                SQLi._classify(value)
                cleaned[key] = value
            except PotentialSQLiPayload:
                cleaned[key] = error
        return cleaned
