"""
Animating WiFi

Date Created: Feb 15, 2023


"""

from src.python.utils import *

def load_json_data(json_path):    
    with open(json_path, 'r') as dataFile:
        coordinates_dict  = json.load(dataFile)
        access_points     = list(coordinates_dict.keys())
        return access_points, coordinates_dict

def process_data(access_points, coordinates_dict, interval):
    device_counts           = []
    access_point_coordinates = []
    
    for ap in access_points:
        df = table.grab(ap, interval)
        df['dt'] = pd.to_datetime(df['datetime'])
        device_counts.append(df['devicecount'].tolist())
        access_point_coordinates.append(coordinates_dict[ap])
        
    return device_counts, access_point_coordinates

def generate_heatmap(data):
    device_counts, access_point_coordinates, image_path, bins, i = data
    campus_map = plt.imread(image_path)
        
    x = [0, len(campus_map[1]),         0, len(campus_map[1])]
    y = [0,         0, len(campus_map[0]), len(campus_map[0])]
        
    for count, coord in zip(device_counts, access_point_coordinates):
        x += [coord[0]] * int(np.ceil(count[i]))
        y += [coord[1]] * int(np.ceil(count[i]))
            
    fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(8,8)) 

    data_points = np.asarray(list(zip(x, y)))
    x = np.asarray(x)
    y = np.asarray(y)
        
    density_estimate = gaussian_kde(data_points.T, bw_method='silverman')
        
    xi, yi = np.mgrid[x.min():x.max():bins*1j, y.min():y.max():bins*1j]
        
    zi = density_estimate(np.vstack([xi.flatten(), yi.flatten()]))
       
    ax.set_title('University of Colorado Boulder WiFi Density')
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    ax.pcolormesh(xi, yi, zi.reshape(xi.shape), shading='gouraud', cmap=plt.cm.jet, alpha=0.1)
    ax.contour(xi, yi, zi.reshape(xi.shape), 20)
    ax.imshow(campus_map, interpolation='nearest', alpha=1)
    plt.savefig('./data/output/animation/{}/{}.png'.format("output", i))

def create_animation(interval, json_path, image_path, bins, frame_interval):
    access_points, coordinates_dict = load_json_data(json_path)
    device_counts, access_point_coordinates = process_data(access_points, coordinates_dict, interval)

    # Use parallel processing to generate heatmaps
    with Pool() as pool:
        pool.map(generate_heatmap, [(device_counts, access_point_coordinates, image_path, bins, i) for i in range(1, len(device_counts[0]), frame_interval)])
