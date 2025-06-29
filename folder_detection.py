import os
import json
from bisect import bisect_left
import datetime
import time

path = "D:/"
directories = [os.path.join(path, name) for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))]
folders = [os.path.basename(item) for item in directories]
created_date = [os.path.getctime(item) for item in folders]
modified_date = [os.path.getmtime(item) for item in folders]

new_data = [{"folder": folder, "modified-date": modified} for folder, modified in zip(folders,modified_date)]

"""with open("data.json", "w") as f:
    json.dump(data, f, indent=4)"""

with open("data.json", "r") as f:
    data = json.load(f)

if len(data) != len(folders):
    print("WTF")

for i in range(len(data)):
    if data[i]["folder"] != folders[i]:
        print(folders[i])
        print(data[i]["folder"])

def test_func():
    return "My Test Function"