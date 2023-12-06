# Smart Campus: Modeling Events

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
/smart-campus
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

    /notebooks
        1. DataProcessor.ipynb
        2. DataVisualization.ipynb
        3. DataDecompositions.ipynb
        4. DataAnimator


    README.md
    requirements.txt
```

## Acknowledgement

This work utilized the Alpine high performance computing resource at the University of Colorado Boulder. Alpine is jointly funded by the University of Colorado Boulder, the University of Colorado Anschutz, Colorado State University, and the National Science Foundation (award 2201538).
