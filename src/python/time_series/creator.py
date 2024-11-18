

########################################################################
#
# AUTHOR:         TYLER A. REISER  
# CREATED:        SEPTEMBER   2023  
# MODIFIED:       NOVEMBER    2024
#
# COPYRIGHT (c) 2024 Tyler A. Reiser
#
########################################################################

""" COPYRIGHT 2024 Tyler A Reiser. """


from datetime import datetime

from src.python.processor.data_processor import DataReader, BuildingProcessor
from src.python.processor.config_manager import ConfigManager
from src.python.time_series.event_plotting import DataVisualizer, CampusPlotter


class VisualizerCreator:
    """
    A class used to create DataVisualizer and CampusPlotter instances.

    ...

    Attributes
    ----------
    start_date : datetime
        The start date for the DataReader
    end_date : datetime
        The end date for the DataReader
    config_manager : ConfigManager
        An instance of ConfigManager
    data_reader : DataReader
        An instance of DataReader
    data_processor : BuildingProcessor
        An instance of BuildingProcessor

    Methods
    -------
    create_visualizer(config_name):
        Returns a DataVisualizer instance for the given configuration name.
    create_visualizers(config_names):
        Returns a dictionary of DataVisualizer instances for the given configuration names.
    create_campus_plotter():
        Returns a CampusPlotter instance.
    """


    def __init__(self, start_date, end_date, config_file="config.json" ):
        
        self.start_date         = datetime.strptime( start_date, '%Y-%m-%d' )
        self.end_date           = datetime.strptime( end_date,   '%Y-%m-%d' )
        self.config_manager     = ConfigManager(config_file)
    
        self.timeseries_configs = [
            "Config1", "Config2", "Config3", "Config4","Config5", "Config6", "Config7", "Config8","Config9", "Config10"
            ]
        self.campus_configs     = [ "campus-plotter1", "campus-plotter2", "normalized-campus-plotter" ]


    def create_processor(self):
        data_reader     = DataReader( start_date=self.start_date, end_date=self.end_date )
        data_processor  = BuildingProcessor( data_reader )
        return data_processor


    def create_visualizer(self, config_name):
        """Returns a DataVisualizer instance for the given configuration name."""
        config = self.config_manager.get_configuration(config_name)
        return DataVisualizer(self.create_processor(), config)


    def create_visualizers(self):
        """Returns a dictionary of DataVisualizer instances for the given configuration names."""
        return {config: self.create_visualizer(config) for config in  self.timeseries_configs}


    def create_campus_plotter(self, config_name):
        """Returns a CampusPlotter instance with and without normalization."""
        data    = self.create_processor().process_all_buildings()["Campus"]
        config  = self.config_manager.get_configuration(config_name)
        return CampusPlotter(data, config)
    
    
    def create_campus_plotters(self):
        """Returns a dictionary of DataVisualizer instances for the given configuration names."""
        return {config: self.create_campus_plotter(config) for config in  self.campus_configs}

