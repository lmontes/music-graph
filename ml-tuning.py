import joblib
import pandas as pd

from sklearn.metrics import *
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer


random_seed = 0
param_grid = {}
pipeline_steps = []

df = pd.read_csv("data/dataset.csv", header=0, sep=";")

X = df["text"].values
y = df["class"].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=random_seed, shuffle=True)

pipeline_steps.append(("cv", CountVectorizer(max_features=10000, strip_accents="unicode")))
param_grid["cv__stop_words"] = [None, "english"]
param_grid["cv__ngram_range"] = [(1, 3)]  # [(1, 1), (1, 2), (1, 3), (2, 2), (2, 3)]


pipeline_steps.append(("tfidf", TfidfTransformer()))

pipeline = Pipeline(pipeline_steps, memory="/tmp")

grid = GridSearchCV(pipeline, cv=5, n_jobs=4, param_grid=param_grid, verbose=3)

pipeline_steps.append(("model", RandomForestClassifier(random_state=random_seed)))
param_grid["model__n_estimators"] = [50, 100, 200]
param_grid["model__max_depth"] = [None, 5, 10]

grid.fit(X_train, y_train)

predictions = grid.best_estimator_.predict(X_test)
score = accuracy_score(y_test, predictions)


print("Best score: ", grid.best_score_)
print("Best parameters: ", grid.best_params_)
print("")
print("Test accuracy: %0.3f" % score)
print("Confusion matrix\n")
print(confusion_matrix(y_test, predictions, labels=["musician", "other"]))


joblib.dump(grid.best_estimator_, "data/model.pkl")


# Save variable importances to file
vocabulary = grid.best_estimator_.named_steps["cv"].vocabulary_
vocabulary_reversed = dict(map(lambda kv: (kv[1], kv[0]), vocabulary.items()))
importances = list(grid.best_estimator_.named_steps["model"].feature_importances_)

vars = [(vocabulary_reversed[i], importances[i]) for i in range(len(importances))]
vars = list(sorted(vars, key=lambda kv: kv[1], reverse=True))

importances_file = open("data/model-feature-importances.csv", "w")
importances_file.write("feature;importance\n")

for kv in vars:
    importances_file.write("%s;%s\n" % kv)
