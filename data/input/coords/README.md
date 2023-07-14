## Coordinates from Image

I used this web app to find the cartesian pixel coordinates for each building: https://plotdigitizer.com/app. This isn't hard to do but it takes a really long time. If a heatmap is wanted for more than one image...it makes more sense to pay a developer to finish the coordinate from map code and to make it adaptable to all images. But, I'm only showing one image, so I just put in several hours of mapping coordinates using this method:

1. Load the image in the webapp above
2. Look for the 4 little X1,X2,Y1,Y2 pointers around the middle of the image
3. Put X1, Y1 into the top left corner
4. Put X2 in the TOP RIGHT corner
5. Put Y2 in the BOTTOM RIGHT corner
6. Look at the file information on your machine for the image loaded to get the demensions
7. Fill in the demensions on the right of the webapp...you're defining the xy-axis...
    - if you dont get it, think about it, and look at these detailed directions:
    - https://plotdigitizer.com/how-extract-data-xy-plotdigitizer

Now that the image is loaded, click on the building to drop a pin and the coordinates will be on the left. I loaded them into JSON files, by hand, as dictionaries. So, the JSON file will look like this:

```json
// East campus JSON example:
{
    "AERO": [
        3487.9709792509043,
        1891.1346087801896
    ],
    "BIOT": [
        2012.821418763276,
        2469.9608791924957
    ],
    "LSRL": [
        953.7231348462343,
        1088.7803300493108
    ],
    "SEEC": [
        662.4936557695178,
        578.7210031347963
    ],
    "SEEL": [
        4239.20864986536,
        2360.7131395386377
    ],
    "SPSC": [
        2956.213608259199,
        1218.1097141749863
    ]
}
```

#### Other links...
https://reference.wolfram.com/language/workflow/GetCoordinatesFromAnImage.html

https://stackoverflow.com/questions/44068654/finding-all-the-x-and-y-coordinates-of-an-image-in-python-opencv

https://stackoverflow.com/questions/60782965/extract-x-y-coordinates-of-each-pixel-from-an-image-in-python

