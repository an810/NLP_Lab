import json
from metric import Align
import pandas as pd

data = pd.read_csv("data/mamnon.csv")
error_data = []

for i in range(len(data)):
    error = []
    Canonical = data['Canonical'][i]
    Transcript = data['Transcript'][i]
    X, Y = Align(Canonical.split(" "), Transcript.split(" "))
    flag = False
    for j in range(len(X)):
        if X[j] == "S" and Y[j] == "s":
            error.append(1)
            flag = True
        elif X[j] == "r" and Y[j] == "z":
            error.append(2)
            flag = True
        elif X[j] == "n" and Y[j] == "l":
            error.append(3)
            flag = True
        elif X[j] == "tS" and Y[j] == "ts_":
            error.append(4)
            flag = True
        elif X[j] == "l" and Y[j] == "n":
            error.append(5)
            flag = True
    if flag == False:
        error = [0]
    error = list(set(error))
    error_data.append(error)

# Write the error data to a JSON file
with open("results/vi_top/mamnon_top5.json", "w") as json_file:
    json.dump(error_data, json_file)
