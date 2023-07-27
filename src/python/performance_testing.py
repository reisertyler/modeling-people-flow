from src.python.utils import *
from src.python.DataProcessor import *

import seaborn as sns

def dataProcessor_speedUp_visual(sample_freq_list=SAMPLE_FREQUENCY_LIST):
    
    max_cores   = multiprocessing.cpu_count()
    cores       = list(range(1, max_cores + 1))
    times_dict  = {freq: [] for freq in sample_freq_list}
    errors = []

    with ProcessPoolExecutor(max_workers=max_cores) as executor:
        
        data_processor = DataProcessor(cpu_cores=1, record_time=True, sample_freq=sample_freq_list[0])
        
        for freq in sample_freq_list:
            for i in cores:
                try:
                    data_processor.cpu_cores    = i
                    data_processor.sample_freq  = freq
                    future      = executor.submit(data_processor.process_all_buildings)
                    total_time  = future.result()
                    times_dict[freq].append(total_time.total_seconds())
                except Exception as e:
                    errors.append((i, freq, str(e)))
                    print(f"Error processing data with {i} cores and {freq} frequency: {e}")

    df = pd.DataFrame(times_dict)
    
    plt.figure(figsize=(15, 5))
    sns.lineplot(data=df)
    plt.title("Data Processing Time by Number of Cores")
    plt.xlabel("Number of CPU Cores")
    plt.ylabel("Time (seconds)")
    plt.legend()
    plt.grid(True)
    plt.show()

    if errors:
        print("Errors occurred during processing:")
        for i, freq, error in errors:
            print(f"Error processing data with {i} cores and {freq} frequency: {error}")

    return df
