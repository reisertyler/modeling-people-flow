from src.python.utils import *


'''

Plotting functions and visualization tools.
Date Created: Jul 28, 2023 by T.Reiser

'''


def display_images( OUTPUT_PATH_DT_SERIES: str, thumbnail_size: Tuple[int, int] = (200, 200)    ):
    """
    Display a series of images in a Matplotlib figure.

    Parameters:
    OUTPUT_PATH_DT_SERIES (str): Path to the series of images.
    thumbnail_size (tuple): Width and height (pixels) to which to resize the images.

    Returns:
    None
    """
    
    image_files = [ file for file in os.listdir(    OUTPUT_PATH_DT_SERIES   ) if file.endswith((".png"))   ]

    fig     = plt.figure(figsize=(18, 20))
    columns = 6
    rows    = 15

    fig.subplots_adjust(    hspace=0.5, wspace=-0.75    )

    for i, image_file in enumerate(image_files):
        image_path  = os.path.join(OUTPUT_PATH_DT_SERIES, image_file)
        img         = Image.open(image_path)
        img.thumbnail(thumbnail_size)
        ax          = fig.add_subplot(rows, columns, i+1)
        
        ax.imshow(img)
        ax.axis('off')
        ax.set_title(image_file, fontsize=6)

    plt.show()
    

def image_viewer(   OUTPUT_PATH_DT_SERIES: str, thumbnail_size: Tuple[int, int] = (1800, 1800)  ):
    """
    An image viewer that cycles through a series of images based on OpenCV2.

    Parameters:
    OUTPUT_PATH_DT_SERIES (str): Path to the series of images.
    thumbnail_size (tuple): Width and height (pixels) to which to resize the images.

    This viewer includes controls for navigation:
    'n' - move to the next image
    'p' - move to the previous image
    ESC - close the image viewer window

    Returns:
    None
    """
    
    image_files = [ file for file in os.listdir( OUTPUT_PATH_DT_SERIES   ) if file.endswith((".png"))   ]
    images      = []

    for img_file in image_files:
        img = Image.open(os.path.join(OUTPUT_PATH_DT_SERIES, img_file))
        img.thumbnail(thumbnail_size)
        images.append(img)
    
    def nothing(x):
        pass

    n = len(images)
    
    cv2.namedWindow(    'ImageWindow'   )
    cv2.createTrackbar( 'Image Index','ImageWindow',0,n-1,nothing   )

    while(1):
        
        i       = cv2.getTrackbarPos(   'Image Index','ImageWindow' )
        img_np  = np.array( images[i]   )
        img_bgr = cv2.cvtColor( img_np, cv2.COLOR_RGB2BGR    )
    
        cv2.imshow('ImageWindow', img_bgr)
        
        k       = cv2.waitKey(1) & 0xFF
        
        if k == 27:
            break
        
        elif k == ord('n'):
            i = (i + 1) % n
            cv2.setTrackbarPos('Image Index','ImageWindow',i)
            
        elif k == ord('p'):
            i = (i - 1) % n
            cv2.setTrackbarPos('Image Index','ImageWindow',i)