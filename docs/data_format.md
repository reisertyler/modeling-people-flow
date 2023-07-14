#### Data Format
The data sets in this drive contain Wifi Information for each building on campus from [2019-08-16 08:10:53] to [2021-05-25 06:57:08]. The data is segmented into three folders: “UCB Wireless”, “UCB Guest”,  and “Eduroam”; each Folder contains data sets from each network . Every file is a CSV file named in the following format: [Building Code]_Extracted_Data_[Start Date]. 

Files contain the date and time in column zero and the active connected client count in column one. An example of file data is given below from the UCB Wireless network in Aden Hall. This first row of this example dataset would be read as “In Aden Hall, on August 16, 2019 at 8:10:53, there were eight devices connected to UCB Wireless”. 

#### ADEN HALL EXAMPLE  
| Time       | Device Count | 
| ------------------- | --- |
| 2019-08-16 08:10:53 | 8.0 |
| 2019-08-16 08:18:58 | 4.0 |
| 2019-08-16 08:28:17 | 5.0 |
| 2019-08-16 08:32:10 | 9.0 |
| 2019-08-16 08:37:38 | 6.0 |
| 2019-08-16 08:42:51 | 9.0 |
| 2019-08-16 08:47:59 | 5.0 |

#### Building Details
There are three main categories of buildings, designated by campus. A list of the campus building codes connected with building name and location can be found [here](https://github.com/reisertyler/wifi-data/blob/main/_MaBL.pdf). The following table describes the three differences.

| Residents                  | Classrooms                                                       | Community |
| ----- | --- | --- |
| “Living spaces like dorms” | “Places where learning takes place, lectres, office hours, etc.” |“Spaces where students congregate that are not a classroom or dorm room; may include leisure activities, school related activities, etc.”

Here is a list of buildings to be used in code:
```python
# Lists of Buildings and Dates
# Date Created: July 30, 2022
Community = ['ALUM','C4C','LIBR','REC','Rec','STAD','STSB','STTB','stad']

Residential = ['ADEN', 'ANDS', 'ARNT', 'BCAPA', 'BCAPB', 'BRKT', 'BUCK', 'CHEY', 'KITW', 'CROS', 
               'CKRL', 'FRND', 'HLET', 'DLYT', 'HLMS', 'LIBY', 'SMTH', 'REED', 'STRN', 'SWLL', 
               'WLRD', 'WVC', 'WVE', 'WVN', 'WVRC', 'arnt', 'bker', 'kcen', 'kitw', 'URES']

EngineeringQuad = ['CKRL', 'ADEN', 'CROS', 'BRKT']

all_buildings = ['ADEN', 'AERO', 'ALMG', 'ALUM', 'ANDS', 'ARNT', 'ATLS', 'BCAPA', 'BCAPB', 'BIOT',
                 'bker', 'BRKT', 'BUCK',  'C4C', 'CARL', 'CASA', 'CASE', 'CHEY', 'CHMP', 'CKRL',
                 'CROS', 'DACR', 'DACR', 'DALW',  'DLC', 'DLYT', 'DUAN', 'ECAD', 'ECCE', 'ECCR',
                 'ECEE', 'ECES', 'ECME', 'ECON', 'ECOT', 'ECST', 'EDEP', 'EHSC', 'EKLC', 'ENVD',
                 'FRND', 'GOLD', 'GUGG', 'HEND', 'HLET', 'HLMS', 'ITLL', 'kcen', 'KITW',
                 'KOBL', 'KTCH', 'LESS', 'LIBR', 'LIBY', 'LSRL',  'MUS', 'RAMY' , 'REC', 'REED',
                 'SEEC', 'SEEL', 'SMTH', 'SPSC', 'STAD', 'STRN', 'STSB', 'STTB', 'SWLL',  'UMC',
                 'URES',  'VAC', 'WLAW', 'WLRD',  'WVC', 'WVE', 'WVN', 'WVRC']
```
