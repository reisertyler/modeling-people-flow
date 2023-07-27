## WiFi Traffic Analysis
This is a project by the NSF-GHOST, Traffic Analysis team at University of Colorado Boulder to hide network traffic and events. The campus WiFi system is used to simulate a 5G network for a proof-of-concept demonstration. This project is done in collaboration with Federated Wireless and includes support from University of Colorado Office of Information Technology. For a summary of our data, use [this link](https://github.com/NSF-GHOST/WiFi/blob/main/Summary.csv).

---

```bash
/smart-and-connected-campus
    /src
        /python
            __init__.py
            extraction.py
            utils.py
            plots_3d.py
            data_processing.py
    /notebooks
        smart_and_connected_campus.ipynb
    /data
        /input
            /coords
                campusCoords.json
            /png_files
                campus_image.png
            /WiFiData
                building1.csv
                building2.csv
        /output
    /scripts
        script1.sh
    /config
    README.md
    requirements.txt
```

\__init__.py: This file is read when Python initiates a package.
extraction.py: This is where you can do all your data extraction.
utils.py: A central place to store functions and classes that can be used throughout the project.
plots_3d.py: This module can contain functions to generate or manipulate your 3D plots.
data_processing.py: This file will handle processing of data in parallel using joblib.

### [Documentation](https://github.com/NSF-GHOST/WiFi/tree/main/docs)  
Look here for help using this package. 
|           File Name           |    Description   |
|              ---              |        ---       | 
|  GHOST/Traffic Analysis       | A brief introduction... | 
| [Explaination and Example on Data Format](https://github.com/NSF-GHOST/WiFi/tree/main/docs/data_format.md) | Minimal overview on how the data is processed. |
| Matrix Factorization Methods  | SVD, NMF, etc... |  
| SINDy                         | What is SINDy? |  
| [Reference List](https://github.com/NSF-GHOST/WiFi/tree/main/docs/reference_list.md)  | A complete list of references used on this project, with descriptions, notes, and summaries on interesting and useful points. |

### [Notebooks](https://github.com/NSF-GHOST/WiFi/tree/main/notebooks)  
Jupyter notebooks are used to show the use of the code stored in the ./src/ directory. Each notebook contains code and additional documentaion in markdown format.
|      File Name     |   Description   |
|         ---        |       ---       |
| [Data Extraction](https://github.com/NSF-GHOST/WiFi/tree/main/sindy_multi.ipynb)                       | info |
| [NMF/SVD](https://github.com/NSF-GHOST/WiFi/tree/main/sindy_multi.ipynb)                          | info |
| [SINDy](https://github.com/NSF-GHOST/WiFi/tree/main/sindy_multi.ipynb)                            | info |
| [Animation: CAMPUS ](https://github.com/NSF-GHOST/WiFi/tree/main/sindy_multi.ipynb)  | info |
 
---
### Other Info
#### Cloning
Clone this repo on your machine or click the green button (above on GitHub) to download the zip. Or, use "git clone" in your favorite terminal at the location on your machine. Directions can be found [here](https://github.com/CUBoulder-Curry-Research/.github/blob/main/README.md).

#### OLD WiFi Package Details
The first iteration of this project is available in another repository. Use the code in [Data-Extraction](https://github.com/reisertyler/wifi-data/tree/main/Data-Extraction) to extract and plot from the .csv files. Use the code in [NMF](https://github.com/reisertyler/wifi-data/tree/main/NMF) as an example if more code is needed. The .csv files for the UMC and Library can be found [here](https://github.com/reisertyler/wifi-data/tree/main/UMC_Lib-data).

---
[RETURN TO ORGANIZATION HOMEPAGE](https://github.com/NSF-GHOST) 