import pandas as pd

def convert_to_datetime(start,end):
    try:
        start = pd.to_datetime(start)
        end = pd.to_datetime(end)
    except ValueError:
        raise ValueError("Error: start and end must be in the format of YYYY-MM-DD HH:MM:SS")
    if start > end:
        start,end = end,start
    return start,end