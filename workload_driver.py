import json
import time
import pandas as pd
import xarray as xr
from test_query import temporal_range_aggregation
import os

grib_file_path = "E:/tu ilmenau/WS 24/Research Project/progress/ERA5-Land_2m_temperature_2000-2022_europe_2.grib"

# print("Current Working Directory:", os.getcwd())

def load_config(config_path=os.path.join(os.path.dirname(__file__), "benchmark_config.json")):
    with open(config_path, "r") as file:
        return json.load(file)

def run_benchmark(ds, query_configs, number_of_runs):
    results = []
    for config in query_configs:
        for time_range in config["time_ranges"]:  
            for _ in range(number_of_runs):  
                start_time = time.perf_counter()
                if config["type"] == "temporal_range_aggregation":
                    result = temporal_range_aggregation(
                        ds,
                        start_date=time_range["start"],  
                        end_date=time_range["end"],  
                        variable=config["variable"],
                        operation=config["operation"]
                    )
                execution_time = time.perf_counter() - start_time
                results.append({
                    "query_type": config["type"],
                    "start_date": time_range["start"],  
                    "end_date": time_range["end"],  
                    "execution_time": execution_time
                })
    return pd.DataFrame(results)


def main():
    ds = xr.open_dataset(grib_file_path, engine='cfgrib')
    config = load_config()
    query_configs = config["queries"]
    number_of_runs = config["number_of_runs"]  
    benchmark_results = run_benchmark(ds, query_configs, number_of_runs)  
    excel_file_path = r"E:/tu ilmenau/WS 24/Research Project/progress/benchmark_results.xlsx"
   
    benchmark_results.to_excel(excel_file_path, index=False)
    print("Benchmark completed. Results saved to 'benchmark_results.csv'.")


if __name__ == "__main__":
    main()
