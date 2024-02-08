
import xarray as xr
import cdsapi
import eccodes
import cfgrib
import os
import timeit
import pandas as pd
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np

grib_file_path = "E:/tu ilmenau/WS 24/Research Project/progress/ERA5-Land_2m_temperature_2000-2022_europe_2.grib"


ds_2 = xr.open_dataset(grib_file_path, engine='cfgrib')
print(ds_2)


#Temporal Range Selection and Aggregation
def temporal_range_aggregation(ds, start_date, end_date, variable='t2m', operation='mean'):
    """
    Selects data within a time range and performs an aggregation operation.
    
    Args:
    ds (xarray.Dataset): The dataset.
    start_date (str): Start date in 'YYYY-MM-DD' format.
    end_date (str): End date in 'YYYY-MM-DD' format.
    variable (str): The variable to aggregate.
    operation (str): The aggregation operation ('mean', 'sum', etc.).
    
    Returns:
    xarray.DataArray: The aggregated data.
    """
    subset = ds.sel(time=slice(start_date, end_date))
    if operation == 'mean':
        return subset[variable].mean(dim='time')
    elif operation == 'sum':
        return subset[variable].sum(dim='time')
    else:
        raise ValueError(f"Unsupported operation '{operation}'. Only 'mean' and 'sum' are supported.")
    


aggregated_result = temporal_range_aggregation(
    ds=ds_2, 
    start_date='2020-01-01',
    end_date='2020-01-31',
    variable='t2m',  
    operation='mean'
)

print(aggregated_result)