

from src.python.processor.data_processor import DataReader, BuildingProcessor

import matplotlib.pyplot as plt


####################################################################################
#
#   Class: SpeedTest
#
####################################################################################

class SpeedTest:
    def __init__(self,cpu_cores,sample_freqs):
        self.cpu_cores = cpu_cores
        self.sample_freqs = sample_freqs
        self.time_results = {freq: [] for freq in self.sample_freqs}

    def run(self):
        for freq in self.sample_freqs:
            print(f'\nProcessing all buildings for sample frequency:\t {freq}\n')
            for cores in self.cpu_cores:
                data_reader = DataReader(sample_freq=freq)
                processor   = BuildingProcessor(data_reader,record_time=True,cpu_cores=cores)
                
                time_result = processor.process_all_buildings()
                self.time_results[freq].append(time_result)

    def plot_results(self):
        plt.figure(figsize=(10, 6))
        
        for freq, results in self.time_results.items():
            plt.plot(self.cpu_cores,results,label=f'Sample Frequency: {freq}')
        plt.xlabel('Number of CPU Cores')
        plt.ylabel('Time to Process Data (s)')
        plt.title('Processing Time vs Number of CPU Cores for Different Sample Frequencies')
        plt.legend()
        plt.show()