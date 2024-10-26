import os
import json

# Get the absolute path of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct absolute paths to the files
devSQL_path = os.path.join(script_dir, "../../../ATIS/dev.sql")
testSQL_path = os.path.join(script_dir, "../../../ATIS/test.sql")
train_devSQL_path = os.path.join(script_dir, "../../../ATIS/train_dev.sql")
trainSQL_path = os.path.join(script_dir, "../../../ATIS/train.sql")

testNL_path = os.path.join(script_dir, "../../../ATIS/test.nl")
devNL_path = os.path.join(script_dir, "../../../ATIS/dev.nl")
train_devNL_path = os.path.join(script_dir, "../../../ATIS/train_dev.nl")
trainNL_path = os.path.join(script_dir, "../../../ATIS/train.nl")

# Read the files
with open(devSQL_path, "r") as f:
    devSQL = f.readlines()

with open(testSQL_path, "r") as f:
    testSQL = f.readlines()

with open(train_devSQL_path, "r") as f:
    train_devSQL = f.readlines()

with open(trainSQL_path, "r") as f:
    trainSQL = f.readlines()

with open(devNL_path, "r") as f:
    devNL = f.readlines()

with open(testNL_path, "r") as f:
    testNL = f.readlines()

with open(train_devNL_path, "r") as f:
    train_devNL = f.readlines()

with open(trainNL_path, "r") as f:
    trainNL = f.readlines()

# Initialize dictionaries
combined = {}

# Create schema
def createSchema():
    j = 0
    for i in range(len(devSQL)):
        combined[j] = {
            "question": devNL[i].strip(),
            "query": devSQL[i].strip()
        }
        j += 1
    for i in range(len(testSQL)):
        combined[j] = {
            "question": testNL[i].strip(),
            "query": testSQL[i].strip()
        }
        j += 1
    for i in range(len(train_devSQL)):
        combined[j] = {
            "question": train_devNL[i].strip(),
            "query": train_devSQL[i].strip()
        }
        j += 1
    for i in range(len(trainSQL)):
        combined[j] = {
            "question": trainNL[i].strip(),
            "query": trainSQL[i].strip()
        }
        j += 1

createSchema()



print(len(combined))

with open("../../../ATIS/combined.json", "w") as json_file:
    json.dump(combined, json_file, indent=4)

print("Data saved")

