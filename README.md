# Smart Campus Prototype

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
            EDUROAM
                building.csv....
            UCBGuest
                building.csv....
            UCBWireless
                building.csv....

    /output
        /building-plots
            /intervals
                /datetime-series
                /time-series
                
        /campus-plots

    /src
        /cpp

        /python
            __init__.py
            DataAnimator.py
            DataProcessor.py
            DataVisualizer.py
            DecompositionsMethods.py
            DecompositionsVisualizer.py
            TableBuilder.py
            performance_testing.py
            plot_functions.py
            utils.py

        /scripts
            slurm
            mount
            run

    MAIN.ipynb
    README.md
    requirements.txt
```

## Acknowledgement

This work utilized the Alpine high performance computing resource at the University of Colorado Boulder. Alpine is jointly funded by the University of Colorado Boulder, the University of Colorado Anschutz, Colorado State University, and the National Science Foundation (award 2201538).
