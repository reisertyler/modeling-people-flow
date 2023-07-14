"""
Creating a Summary Table of all CSV files

Date Created: Feb 13, 2023

get_building_identifiers: This function takes a filename as an argument and returns the building identifier. 
It assumes the filename follows a specific format where the building identifier comes before the first underscore.

plot_multiple_buildings: This function takes a list of buildings, an index range, and a normalization method as arguments. 
It plots the device count over time for each building in the list. 
The device count can be normalized using either z-score normalization or min-max normalization. 
The function loads the data for each building, applies the normalization if specified, and plots the device count over the specified index range. 
The plot includes a legend, title, and labels for the x-axis and y-axis. 
The improved code improves clarity by using more descriptive function and variable names, and improves the plots by increasing the font size for the legend and changing the y-axis label to reflect the normalization. 
The speed of the code should be about the same, as the main operations are loading and plotting data, which have a fixed cost.


"""

from src.python.utils import *
from src.python import plots_3d

def get_building_identifiers(filename):
    return filename.split('_')[0]

def list_all_buildings(file_list):
    return [get_building_identifiers(file) for file in file_list]

def build_summary_table(file_list, save_file=True):
    column_names = ['Building', 'Data Count', 'User Mean', 'STD. VAR.', 'Min', 'Max', '25%', '50', '75%']
    building_list = list_all_buildings(file_list)
    summary_table = pd.DataFrame(columns=column_names)

    for file in file_list:
        building = get_building_identifiers(file)
        df = pd.read_csv(f'./WiFiData/{file}', header=None)
        df.columns = ['datetime', 'usercount']
        summary_data = df['usercount'].describe()
        summary_row = pd.DataFrame([[
            building, 
            int(summary_data['count']), 
            round(summary_data['mean'], 1), 
            round(summary_data['std'], 1), 
            summary_data['min'], 
            summary_data['max'],
            summary_data['25%'], 
            summary_data['50%'], 
            summary_data['75%']
        ]], columns=column_names)

        summary_table = pd.concat([summary_table, summary_row])

    if save_file:
        summary_table.to_csv("Summary.csv", index=False)

    return summary_table

def load_building_data(building, index_range='all'):
    df = pd.read_csv(f'./WiFiData/{building}_Extracted_Data_8-16-2019.csv', header=None)
    df.columns = ['datetime', 'devicecount']

    if index_range != 'all':
        start_index, end_index = index_range
        df = df.loc[start_index:end_index]

    return df

def expand_fields(df, convert_datetimes=True, add_hours=True,
                  add_minutes=True, add_time=True, add_date=True, add_dayofweek=True):
    if convert_datetimes:
        df['datetime'] = pd.to_datetime(df['datetime'])
        
    if add_hours:
        df['Hour'] = df['datetime'].dt.hour
    if add_minutes:
        df['Minute'] = df['datetime'].dt.minute
    if add_time:
        df['Time'] = df['datetime'].dt.time
    if add_date:
        df['Date'] = df['datetime'].dt.date
    if add_dayofweek:
        df['Day of Week'] = df['datetime'].dt.day_name()

    return df

def plot_data(df, x_values, y_values, title="", subtitle="", xlabel='Date', ylabel='Device Count'):
    plt.figure(figsize=(12,4))
    plt.plot(x_values, y_values, color='blue', linewidth=0.7)
    plt.gca().set(title=subtitle, xlabel=xlabel, ylabel=ylabel)
    plt.suptitle(title, fontsize=9, fontweight='bold')
    plt.show()

def plot_building_usage(building, index_range):
    df = load_building_data(building, index_range)
    df['datetime'] = pd.to_datetime(df['datetime'])
    
    start_index, end_index = index_range

    plot_data(df, 
              x_values=df.loc[start_index:end_index, "datetime"], 
              y_values=df.loc[start_index:end_index, "devicecount"],
              subtitle=f'{df["datetime"].loc[start_index]} to {df["datetime"].loc[end_index]}', 
              title=f'{building}: Device Count vs Time')
    
    