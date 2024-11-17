
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

import os
import os
import json   

 
###################################################################################
#
#   Class: ConfigManager
#
###################################################################################

class ConfigManager:
    
    def __init__(self, file_path: str):
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Configuration file not found: {file_path}")

        self.configs        = self._load_configurations(file_path)
        self.base_config    = self.configs["BaseConfig"]


    @staticmethod
    def _load_configurations(file_path) -> dict:

        with open(file_path, "r") as f:
            
            return json.load(f)


    def get_configuration(self, config_name) -> dict:
        
        specific_config = self.configs.get(config_name)
        
        if specific_config is None:
            raise KeyError(f"Configuration not found: {config_name}")

        return self._merge_configs(self.base_config, specific_config)


    @staticmethod
    def _merge_configs(base_config: dict, specific_config: dict) -> dict:
        
        merged_config = base_config.copy()
        merged_config.update(specific_config)
        
        return merged_config