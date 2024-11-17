# Modeling Population Flow

This project takes a dynamical systems approach to modeling population. Everything is explained in the Jupyter Notebooks and will be updated over the next few months. It is a work in progress and a side-project that is not currently funded. If you are interested in helping me, Tyler Reiser, fund this project or if you would like to fund this project, please reach out. Thanks.

## Workflow

> NOTE THE WORKFLOW SECTION WILL BE UPDATED WITHIN THE NEXT WEEK. EVERYTHING ELSE IS UP-TO-DATE.

1. Processing Procedure

    - Dataset Introduction: Campus WiFi
    - The `DataProcessor` Class
    - Class Methods
    - Optional Parameters
    - Speed-up: Parallel Data Processing
    - Performance Testing and Results
`
2. Data Visualization

    - Time-Series Visualization
    - The `DataVisualization` Module
    - Classes in this Module
        - The `DataVisualizer` Class
        - The `InteractiveVisualizer` Class

3. Matrix Decompositions

    - SVD
    - Truncated-SVD
    - NMF
    - TSNMF

4. Data Animation

    - The `DataAnimator` Class

## Directory Information

```bash
/ModelingPopulationFlow
    .env
    .vscode

    /data
        /input
            /configs
            /coords
                campusCoords.json
                engineeringCoords.json

            /events
                event_dict.py  

            /png_files
                main_campus.png
                east_campus.png
                engineering_quad.png

            /WiFiData-old
                /Eduroam
                    building.csv...
                /UCBGuest
                    building.csv...
                /UCBWireless
                    building.csv...

            /WiFiData-new
                IN-PROGRESS ... a few weeks

        /output
            /building-plots
                /all-buildings
                    sparsity_3networks-AllData.png

                /chunks
                    /normalized
                        "%b-%d-%Y"_to_"%b-%d-%Y"
                            /svd
                                AERO.png...
                            /trunc-svd
                                AERO.png...
                            /nmf
                                AERO.png...
                            /tsnmf
                                AERO.png...

                    /special
                    /time-series

                /single
                    /normalized
                    /time-series
                    /interval

            /campus-plots
    
    /notebooks
        DataAnimator.ipynb
        DataDecompositions.ipynb
        DataVisualization.ipynb
        TEST.ipynb
                    
    /src
        /python
            /data_plotter
                sparsity_plotter.py
                bar_charts.py

            /decomps
                nmf.py
                svd.py

            /processor
                config_manager.py
                data_processor.py
                sparsity.py
            
            /sindy

            /time_series
                creator.py
                event_plotting.py
                plot_builder.py

            /gui
                launcher.py

    .gitignore
    MAIN.ipynb
    config.json
    config2.json
    README.md
    requirements.txt
```

## Acknowledgement

Built as a side project during summer 2023 by Tyler Reiser. This code has never been run on CU Research Computing resources - the goal was to build a system that could process WiFi information reports for the entire campus, eventually running it continuously on the Alpine supercomputing cluster.

---

AUTHOR:         TYLER A. REISER  
CREATED:        SEPTEMBER   2023  
MODIFIED:       NOVEMBER    2024

COPYRIGHT (c) 2024 Tyler A. Reiser
