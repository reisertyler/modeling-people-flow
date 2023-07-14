"""
Wifi Dataset Extraction - BASIC

Date Created: Feb 8, 2023

The code you provided is written in Python and uses the pandas, numpy, and scipy libraries to perform operations on a dataset, 
specifically extracting data from a CSV file and interpolating missing data points. 
The code is well-structured, but there are some areas where it could be improved for readability and efficiency.

These functions read time-series data from a CSV file, interpolate the data linearly at a specified sample rate, and build a study based on the specified buildings, days, and year.
"""

from src.python.utils import *

def generate_dates(start_date: date, end_date: date) -> List[date]:
    """
    Generate a list of dates between start_date and end_date inclusive.

    Parameters:
    start_date (date): The start date.
    end_date (date): The end date.

    Returns:
    List[date]: A list of dates between start_date and end_date inclusive.
    """
    delta = timedelta(days=1)
    dates = [start_date + timedelta(days=i) for i in range((end_date-start_date).days + 1)]
    return dates

def get_start_and_stop_times(day: str, year: int) -> Tuple[datetime, datetime]:
    """
    Generate the start and stop times for a given day and year.

    Parameters:
    day (str): The day in the format 'MM-DD'.
    year (int): The year.

    Returns:
    Tuple[datetime, datetime]: A tuple where the first element is the start time and the second element is the stop time.
    """
    start_time = datetime.strptime(f'{year}-{day} 00:00:00', '%Y-%m-%d %H:%M:%S')
    stop_time = start_time + timedelta(days=1)
    return start_time, stop_time

def separate_dates_into_weekdays_and_weekends(dates: List[datetime.date]) -> Tuple[List[datetime.date], List[datetime.date]]:
    """
    Separate a list of dates into weekdays and weekends.

    Parameters:
    dates (List[datetime.date]): A list of dates.

    Returns:
    Tuple[List[datetime.date], List[datetime.date]]: A tuple where the first element is a list of weekdays and the second element is a list of weekends.
    """
    weekdays = [date for date in dates if date.weekday() < WEEKDAY_THRESHOLD]
    weekends = [date for date in dates if date.weekday() >= WEEKDAY_THRESHOLD]
    return weekdays, weekends

def remove_outliers_IQR(dates: List[datetime.date]) -> List[datetime.date]:
    """
    Remove outliers from a list of dates using the Interquartile Range (IQR) method.

    Parameters:
    dates (List[datetime.date]): A list of dates.

    Returns:
    List[datetime.date]: A list of dates with outliers removed.
    """
    Q1 = np.percentile(dates, 25)
    Q3 = np.percentile(dates, 75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return [date for date in dates if lower_bound <= date <= upper_bound]

def read_time_series_data(file_path: str) -> pd.DataFrame:
    """
    Read time-series data from a CSV file.

    Parameters:
    file_path (str): The path of the CSV file.

    Returns:
    pd.DataFrame: A DataFrame containing the time-series data.
    """
    data_mat = pd.read_csv(file_path, header=None, names=['times','count'])
    data_mat['times'] = pd.to_datetime(data_mat['times'])
    data_mat.set_index('times', inplace=True)
    return data_mat

def get_filename(building_name: str) -> str:
    """
    Generate a filename based on the building name.

    Parameters:
    building_name (str): The name of the building.

    Returns:
    str: The generated filename.
    """
    return building_name + COMMON

def get_seconds_from_start(timestamps: pd.DatetimeIndex) -> np.ndarray:
    """
    Convert a list of timestamps to the number of seconds since the first timestamp.

    Parameters:
    timestamps (pd.DatetimeIndex): A list of timestamps.

    Returns:
    np.ndarray: An array containing the number of seconds since the first timestamp for each timestamp.
    """
    start_time = timestamps[0]
    seconds_from_start = (timestamps - start_time).total_seconds()
    return seconds_from_start

def get_start_and_stop_times(day: str, year: int) -> Tuple[datetime, datetime]:
    """
    Generate the start and stop times for a given day and year.

    Parameters:
    day (str): The day in the format 'MM-DD'.
    year (int): The year.

    Returns:
    Tuple[datetime, datetime]: A tuple where the first element is the start time and the second element is the stop time.
    """
    start_time = datetime.strptime(f'{year}-{day} 00:00:00', '%Y-%m-%d %H:%M:%S')
    stop_time = start_time + timedelta(days=1)
    return start_time, stop_time

def interpolate_time_series_data_linearly(df: pd.DataFrame, sample_rate: str) -> pd.DataFrame:
    """
    Interpolate the time-series data linearly at the specified sample rate.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the time-series data.
    sample_rate (str): The sample rate for interpolation.

    Returns:
    pd.DataFrame: A DataFrame containing the interpolated time-series data.
    """
    new_range = pd.date_range(df.index[0], df.index.values[-1], freq=sample_rate)
    new_range_numeric = get_seconds_from_start(new_range)
    OGnumeric_vals = get_seconds_from_start(df.index)
    data = df['count']
    f = interpolate.interp1d(OGnumeric_vals, data, kind='linear')
    interp_count = pd.Series(f(new_range_numeric))
    mat = pd.DataFrame(data={'newTimes': new_range, 'newCount': interp_count})
    mat.set_index('newTimes', inplace=True)
    return mat

def build_study(building_names: List[str], set_of_days: List[str], year: int, day_period: int = 144) -> Tuple[np.ndarray, np.ndarray, pd.DatetimeIndex]:
    """
    Build a study based on the specified buildings, days, and year.

    Parameters:
    building_names (List[str]): A list of building names.
    set_of_days (List[str]): A list of days.
    year (int): The year.
    day_period (int): The number of periods in a day. Default is 144 (for 10-minute intervals).

    Returns:
    Tuple[np.ndarray, np.ndarray, pd.DatetimeIndex]: A tuple where the first element is a 1D array containing the building names and dates, the second element is a 2D array containing the data matrix, and the third element is a DatetimeIndex containing the dates.
    """
    m = len(set_of_days) * len(building_names)
    n = day_period
    DM = np.zeros((n, m))
    y = np.zeros((1, m), dtype=np.dtype('a16'))
    for k, i in enumerate(building_names):
        path = DATA_PATH + get_filename(i)
        test = read_time_series_data(path)
        dm_interp_full = interpolate_time_series_data_linearly(test, '10min')
        for j, day in enumerate(set_of_days):
            index = k * len(set_of_days) + j
            start, stop = get_start_and_stop_times(day, year)
            temp = dm_interp_full.loc[start:stop]
            y[0, index] = i + ": " + day
            DM[:, index] = temp['newCount']
            dates = temp.index      
    return y, DM, dates