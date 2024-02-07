import os

for task in os.listdir("TestData"):
    for d in os.listdir(os.path.join("TestData", task)):
        print(task, d, len(os.listdir(os.path.join("TestData", task, d))))