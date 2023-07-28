from src.python.DataProcessor import *

def measure_data_processing_speed(sample_frequency_list=SAMPLE_FREQUENCY_LIST):
    """
    Function to measure and visualize data processing time for different CPU cores and sampling frequencies.
    
    Args:
        sample_frequency_list (List[str]): List of sampling frequencies to evaluate. Defaults to SAMPLE_FREQUENCY_LIST.

    Returns:
        DataFrame: Pandas DataFrame containing measured time in seconds for all combinations of cores and frequencies.
    """
    num_cores   = multiprocessing.cpu_count()
    core_list   = list(range(1, num_cores + 1))
    times_record  = {freq: [] for freq in sample_frequency_list}
    exceptions = []

    with ProcessPoolExecutor(max_workers=num_cores) as executor:
        
        data_processor = DataProcessor(cpu_cores=1, record_time=True, sample_freq=sample_frequency_list[0])
        
        for frequency in sample_frequency_list:
            for core_num in core_list:
                try:
                    data_processor.cpu_cores    = core_num
                    data_processor.sample_freq  = frequency
                    future      = executor.submit(data_processor.process_all_buildings)
                    total_time  = future.result()
                    times_record[frequency].append(total_time.total_seconds())
                except Exception as error:
                    exceptions.append((core_num, frequency, str(error)))
                    print(f"Error processing data with {core_num} cores and {frequency} frequency. Error: {error}")

    df_times = pd.DataFrame(times_record)
    
    plt.figure(figsize=(12, 5))
    sns.lineplot(data=df_times)
    plt.title("Data Processing Time by Number of Cores")
    plt.xlabel("Number of CPU Cores")
    plt.ylabel("Time (seconds)")
    plt.legend(title="Sample Frequency")
    plt.grid(True)
    plt.show()

    if exceptions:
        print("Errors occurred during processing:")
        for core_num, frequency, error in exceptions:
            print(f"Error processing data with {core_num} cores and {frequency} frequency. Error: {error}")

    return df_times 
