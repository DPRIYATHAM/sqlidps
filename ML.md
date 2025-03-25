## Classification Report - Opted (Random Forest)

### Random Forest (n_estimators=100)
```
Classification Report:
              precision    recall  f1-score   support

           0    0.99665   0.99358   0.99511      3893
           1    0.98914   0.99433   0.99173      2291

    accuracy                        0.99386      6184
   macro avg    0.99290   0.99395   0.99342      6184
weighted avg    0.99387   0.99386   0.99386      6184
```

### SVC (kernel="linear", C=1.0)
```
Classification Report:
              precision    recall  f1-score   support

           0    0.97545   0.94914   0.96211      3893
           1    0.91736   0.95941   0.93791      2291

    accuracy                        0.95294      6184
   macro avg    0.94641   0.95427   0.95001      6184
weighted avg    0.95393   0.95294   0.95315      6184
```
### Passive Aggressive (max_iter=1000)
```
Classification Report:
              precision    recall  f1-score   support

           0    0.96877   0.95608   0.96238      3893
           1    0.92699   0.94762   0.93719      2291

    accuracy                        0.95294      6184
   macro avg    0.94788   0.95185   0.94978      6184
weighted avg    0.95329   0.95294   0.95305      6184
```
### One vs Rest (SVC(kernel='linear', probability=True))
```
Classification Report:
              precision    recall  f1-score   support

           0    0.97545   0.94914   0.96211      3893
           1    0.91736   0.95941   0.93791      2291

    accuracy                        0.95294      6184
   macro avg    0.94641   0.95427   0.95001      6184
weighted avg    0.95393   0.95294   0.95315      6184
```
