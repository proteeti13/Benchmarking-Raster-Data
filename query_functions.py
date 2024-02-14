import xarray as xr
import numpy as np
import pandas as pd


#Aggregate 't2m' over a specified temporal range.
def temporal_range_aggregation(ds, start_date, end_date, variable="t2m", operation="mean"):

    subset = ds.sel(time=slice(start_date, end_date))[variable]
    if operation == 'mean':
        result = subset.mean(dim='time')
    elif operation == 'sum':
        result = subset.sum(dim='time')
    else:
        raise ValueError(f"Unsupported operation: {operation}")
    return result


#Extract a spatial subset for 't2m'
def spatial_subset_extraction(ds, lat_range, lon_range, variable="t2m"):
    subset = ds.sel(latitude=slice(*lat_range), longitude=slice(*lon_range))[variable]
    return subset


# Modify 't2m' data for a specific month and year, with checks for empty selections.
# Example: Increase 't2m' values by 'value' for the specified 'month' and 'year'

def temporal_data_modification(ds, year, month, modification="increase", value=1.0, variable="t2m"):

    year = int(year)
    month = int(month)

  
    ds_mod = ds.copy()
    time_indices = (ds['time'].dt.year == year) & (ds['time'].dt.month == month)

    if not ds['time'].loc[time_indices].size:
        print(f"No data found for year {year} and month {month}. Skipping modification.")
        return ds_mod


    if modification == "increase":
        ds_mod[variable].loc[{'time': time_indices}] += value
    elif modification == "decrease":
        ds_mod[variable].loc[{'time': time_indices}] -= value
    else:
        raise ValueError(f"Unsupported modification type: {modification}")

    return ds_mod




#Add a derived variable based on 't2m'
def add_derived_variable(ds, new_variable_name, base_variable='t2m', operation='multiply', factor=1.0):

    factor = float(factor) 
    if base_variable not in ds:
        raise ValueError(f"Base variable '{base_variable}' not found in the dataset.")
    
    if operation == 'multiply':
        ds[new_variable_name] = ds[base_variable] * factor
    elif operation == 'add':
        ds[new_variable_name] = ds[base_variable] + factor
    elif operation == 'subtract':
        ds[new_variable_name] = ds[base_variable] - factor
    elif operation == 'divide':
        ds[new_variable_name] = ds[base_variable] / factor
    else:
        raise ValueError(f"Unsupported operation: {operation}")
    
    return ds




#Aggregate 't2m' over a specified season
# Definee month ranges for seasons (northern hemisphere)
def seasonal_aggregation(ds, year, season, variable="t2m", operation="mean"):

    seasons_months = {
        'winter': [12, 1, 2],
        'spring': [3, 4, 5],
        'summer': [6, 7, 8],
        'autumn': [9, 10, 11]
    }
    selected_months = seasons_months[season]
    subset = ds.sel(time=(ds['time'].dt.month.isin(selected_months)) & (ds['time'].dt.year == year))[variable]
    if operation == 'mean':
        result = subset.mean(dim='time')
    elif operation == 'max':
        result = subset.max(dim='time')
    else:
        raise ValueError(f"Unsupported operation: {operation}")
    return result
