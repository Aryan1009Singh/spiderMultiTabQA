import os
import json

# Get the absolute path of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct absolute paths to the files
geotestSQL_path = os.path.join(script_dir, "../../../GEOQUERY/geo_test.sql")
geodevSQL_path = os.path.join(script_dir, "../../../GEOQUERY/geo_dev.sql")
geotrain_devSQL_path = os.path.join(script_dir, "../../../GEOQUERY/geo_tr.sql")
geotrainSQL_path = os.path.join(script_dir, "../../../GEOQUERY/geo_train.sql")

geotestNL_path = os.path.join(script_dir, "../../../GEOQUERY/geo_test.nl")
geodevNL_path = os.path.join(script_dir, "../../../GEOQUERY/geo_dev.nl")
geotrain_devNL_path = os.path.join(script_dir, "../../../GEOQUERY/geo_tr.nl")
geotrainNL_path = os.path.join(script_dir, "../../../GEOQUERY/geo_train.nl")

# Read the files
with open(geodevSQL_path, "r") as f:
    geodevSQL = f.readlines()

with open(geotestSQL_path, "r") as f:
    geotestSQL = f.readlines()

with open(geotrain_devSQL_path, "r") as f:
    geotrain_devSQL = f.readlines()

with open(geotrainSQL_path, "r") as f:
    geotrainSQL = f.readlines()

with open(geodevNL_path, "r") as f:
    geodevNL = f.readlines()

with open(geotestNL_path, "r") as f:
    geotestNL = f.readlines()

with open(geotrain_devNL_path, "r") as f:
    geotrain_devNL = f.readlines()

with open(geotrainNL_path, "r") as f:
    geotrainNL = f.readlines()

# Initialize dictionaries
combined = {}

# Create schema
def createSchema():
    j = 0
    for i in range(len(geodevSQL)):
        combined[j] = {
            "question": geodevNL[i].strip(),
            "query": geodevSQL[i].strip()
        }
        j += 1
    for i in range(len(geotestSQL)):
        combined[j] = {
            "question": geotestNL[i].strip(),
            "query": geotestSQL[i].strip()
        }
        j += 1
    for i in range(len(geotrain_devSQL)):
        combined[j] = {
            "question": geotrain_devNL[i].strip(),
            "query": geotrain_devSQL[i].strip()
        }
        j += 1
    for i in range(len(geotrainSQL)):
        combined[j] = {
            "question": geotrainNL[i].strip(),
            "query": geotrainSQL[i].strip()
        }
        j += 1

createSchema()



print(len(combined))

with open("../../../GEOQUERY/combined.json", "w") as json_file:
    json.dump(combined, json_file, indent=4)

print("Data saved")

