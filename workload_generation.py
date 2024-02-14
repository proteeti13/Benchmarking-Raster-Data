
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import csv

def generate_parameters(query_type):

    if query_type == "TemporalRangeAggregation":
        start_date = datetime(2020, 1, 1)
        end_date = start_date + timedelta(days=np.random.randint(30, 60))
        return {
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
            "variable": "t2m",
            "operation": np.random.choice(["mean", "sum"])
        }
    
    

    elif query_type == "SpatialSubsetExtraction":

        lat_range = [np.random.uniform(-90, 90), np.random.uniform(-90, 90)]
        lat_range.sort()
        lon_range = [np.random.uniform(-180, 180), np.random.uniform(-180, 180)]
        lon_range.sort()
        return {
            "lat_range": lat_range,
            "lon_range": lon_range,
            "variable": "t2m"
        }

    elif query_type == "TemporalDataModification":
        month = np.random.choice(range(1, 13))
        year = np.random.choice(range(2000, 2023))  
        return {
            "year": year,
            "month": month,
            "modification": "increase",
            "variable": "t2m",
            "value": np.random.uniform(0.1, 2.0)
        }

    elif query_type == "AddDerivedVariable":
        return {
            "new_variable_name": "t2m_modified",
            "base_variable": "t2m",
            "operation": "multiply",
            "factor": np.random.uniform(1.1, 1.5)
        }

    elif query_type == "SeasonalAggregation":
        season = np.random.choice(["winter", "spring", "summer", "autumn"])
        year = np.random.choice(range(2000, 2023))  
        return {
            "year": year,
            "season": season,
            "variable": "t2m",
            "operation": np.random.choice(["mean", "max"])
        }


    
def generate_workload(config_path="benchmark_config.json", workload_file="workload.csv"):
    with open(config_path, "r") as file:
        config = json.load(file)
    
    queries = []
    total_queries = config.get("total_queries", 100)
    
    for query_config in config["queries"]:
        num_queries = int(total_queries * query_config.get("weight", 0) / 100)
        for _ in range(num_queries):
            params = generate_parameters(query_config["type"])
            queries.append({"type": query_config["type"], **params})
    
    with open(workload_file, 'w', newline='') as csvfile:
        fieldnames = ['type', 'start_date', 'end_date', 'variable', 'operation', 'lat_range', 'lon_range', 'year', 'month', 'modification', 'value', 'new_variable_name', 'base_variable', 'factor', 'season']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for query in queries:
            
            if 'lat_range' in query:
                query['lat_range'] = json.dumps(query['lat_range'])
            if 'lon_range' in query:
                query['lon_range'] = json.dumps(query['lon_range'])


            for key in ['year', 'month', 'value', 'factor']:
                if key in query:
                    query[key] = str(query[key])
            


            writer.writerow(query)
    
    print(f"Workload file '{workload_file}' generated with {len(queries)} queries.")



generate_workload()


# try:
#     with open('workload.csv', 'r') as file:
#         csv_contents = file.readlines()
# except Exception as e:
#     error_message = str(e)


# print(error_message if 'error_message' in locals() else 'File read successfully.')
# print(csv_contents[:5])  