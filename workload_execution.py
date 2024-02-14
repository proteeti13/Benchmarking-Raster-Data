
import pandas as pd
import xarray as xr
import json
import time
import psutil
from query_functions import (
    temporal_range_aggregation,
    spatial_subset_extraction,
    temporal_data_modification,
    add_derived_variable,
    seasonal_aggregation,
)

def load_config(config_path="benchmark_config.json"):
    with open(config_path, "r") as file:
        config = json.load(file)
    return config

def get_system_usage():
    return psutil.cpu_percent(), psutil.virtual_memory().used

def execute_query(ds, query):
    cpu_before, mem_before = get_system_usage()
    start_time = time.perf_counter()


    if 'lat_range' in query and isinstance(query['lat_range'], str):
        query['lat_range'] = json.loads(query['lat_range'])
    if 'lon_range' in query and isinstance(query['lon_range'], str):
        query['lon_range'] = json.loads(query['lon_range'])


    try:
        if query['type'] == 'TemporalRangeAggregation':
            result = temporal_range_aggregation(ds, query['start_date'], query['end_date'],
                                                query['variable'], query['operation'])
        elif query['type'] == 'SpatialSubsetExtraction':
            result = spatial_subset_extraction(ds, query['lat_range'], query['lon_range'],
                                               query['variable'])
        elif query['type'] == 'TemporalDataModification':
            result = temporal_data_modification(ds, int(query['year']), int(query['month']),
                                                query['modification'], float(query['value']),
                                                query['variable'])
        elif query['type'] == 'AddDerivedVariable':
            result = add_derived_variable(ds, query['new_variable_name'],
                                          query['base_variable'], query['operation'], float(query['factor']))
        elif query['type'] == 'SeasonalAggregation':
            result = seasonal_aggregation(ds, int(query['year']), query['season'],
                                          query['variable'], query['operation'])
        else:
            raise ValueError(f"Unsupported query type: {query['type']}")
    except Exception as e:

        result = None
        print(f"An error occurred while executing the query: {e}")

    execution_time = time.perf_counter() - start_time
    cpu_after, mem_after = get_system_usage()

    cpu_diff = cpu_after - cpu_before
    mem_diff = (mem_after - mem_before) / (1024**2) 


    return {
        "result": result,
        "execution_time_sec": execution_time,
        "cpu_usage_diff_percent": cpu_diff,
        "memory_usage_diff_mb": mem_diff
    }

def run_benchmark(workload_file, config):
    ds = xr.open_dataset(config["data_path"], engine='cfgrib')
    workload = pd.read_csv(workload_file)
    results = []

    for index, query in workload.iterrows():
        query_dict = query.to_dict()
        execution_details = execute_query(ds, query_dict)
        execution_details.update({
            "query_index": index,
            "query_type": query_dict['type']
        })
        results.append(execution_details)

    results_df = pd.DataFrame(results)
    results_df.to_csv("benchmark_results.csv", index=False)
    print("Benchmark completed. Results saved to 'benchmark_results.csv'.")

if __name__ == "__main__":
    config = load_config()
    run_benchmark("workload.csv", config)