# Modeling Population Flow

This project takes a dynamical systems approach to modeling population. Everything is explained in the Jupyter Notebooks.

## Copyright

Copyright 2024 Tyler A Reiser  
This repository and all its contents are licensed under the GNU General Public License v3.0 (GPL-3.0).  
By contributing to this project, you agree to license your contributions under the GPL-3.0 license.  
All rights reserved. No warranty is given.  
See LICENSE file for details.  

If you infringe on this copyright or license, then I will take legal action.  

## Workflow

1. Processing Procedure

    - Dataset Introduction: Campus WiFi
    - The `DataProcessor` Class
    - Class Methods
    - Optional Parameters
    - Speed-up: Parallel Data Processing
    - Performance Testing and Results

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
    /data
        /input
            /coords
                campusCoords.json
            /png_files
                campus_image.png
            /WiFiData
                Eduroam
                    building.csv....
                UCBGuest
                    building.csv....
                UCBWireless
                    building.csv....

        /output
            /building-plots
                "%b-%d-%Y"_to_"%b-%d-%Y"
                    /interval
                        AERO.png...
                    /svd
                        AERO.png...
                    /trunc-svd
                        AERO.png...
                    /nmf
                        AERO.png...
                    /tsnmf
                        AERO.png...
                    /special
                    
    /src
        /python
            __init__.py
            DataAnimator.py
            DataProcessor.py
            DataVisualization.py
                DataVisualizer
                GUIVisualizer
            MatrixDecompositions.py
            utils.py

        /scripts
            slurm
            mount
            run


    1. DataProcessor.ipynb
    2. DataVisualization.ipynb
    3. DataDecompositions.ipynb
    4. DataAnimator.ipynb


    README.md
    requirements.txt
```

## Acknowledgement

Built as a side project during summer 2023 by Tyler Reiser. This code has never been run on CU Research Computing resources - the goal was to build a system that could process WiFi information reports for the entire campus, eventually running it continuously on the Alpine supercomputing cluster.

It is too bad I failed out of the graduate program and could not finish the project. I also got a C- in the Data Mining course I took the summer while doing this project - one of two computer science classes I have taken in my academic career. 