import importlib.util
import sys

import joblib
import pkg_resources


def get_package_file(filename: str) -> str:
    return pkg_resources.resource_filename("sqlidps", filename)


module_path = get_package_file("sql_tokenizer.so")
module_name = "sql_tokenizer"

spec = importlib.util.spec_from_file_location(module_name, module_path)
sql_tokenizer = importlib.util.module_from_spec(spec)
sys.modules[module_name] = sql_tokenizer
spec.loader.exec_module(sql_tokenizer)

model_path = get_package_file("model.pkl")
pipeline = joblib.load(model_path)

so_path = get_package_file("sql_tokenizer.so")


class PotentialSQLiPayload(Exception):
    def __init__(self, message="You have a Potential SQL payload in your data"):
        self.message = message
        super().__init__(self.message)


class SQLi:
    @staticmethod
    def _classify(text):
        prediction = pipeline.predict([text])
        if prediction[0] == 1:
            # raise PotentialSQLiPayload(f"{text} SQL payload detected...")
            print(f"{text} => SQL payload detected...")
            return "SQLi Payload"    
        else:
            return text

    @staticmethod
    def check(data):
        if isinstance(data, str):
            return SQLi._classify(data)
        elif isinstance(data, list):
            for value in data:
                return SQLi._classify(value)
        elif isinstance(data, dict):
            for value in data.values():
                return SQLi._classify(value)

    @staticmethod
    def parse(data, error="SQLi payload"):
        assert isinstance(data, dict), "Dictionary expected"
        cleaned = {}
        for key, value in data.items():
            try:
                SQLi._classify(value)
                cleaned[key] = value
            except PotentialSQLiPayload:
                cleaned[key] = error
        return cleaned
    

def welcome():
    print("Welcome to SQLiDPS - SQL Injection Detection and Prevention System")
    print("Find more at https://github.com/DPRIYATHAM/sqlidps/")
    # print console style font
    print(r"""
     ___  _____  __    ____  ____  ____  ___ 
    / __)(  _  )(  )  (_  _)(  _ \(  _ \/ __)     
    \__ \ )(_)(  )(__  _)(_  )(_) ))___/\__ \
    (___/(___/\\(____)(____)(____/(__)  (___/
    """)