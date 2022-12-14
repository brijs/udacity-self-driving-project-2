# ---------------------------------------------------------------------
# Project "Track 3D-Objects Over Time"
# Copyright (C) 2020, Dr. Antje Muntzinger / Dr. Andreas Haja.
#
# Purpose of this file : Process the point-cloud and prepare it for object detection
#
# You should have received a copy of the Udacity license together with this program.
#
# https://www.udacity.com/course/self-driving-car-engineer-nanodegree--nd013
# ----------------------------------------------------------------------
#

# general package imports
import cv2
import open3d as o3d
import numpy as np
import torch
import zlib

# add project directory to python path to enable relative imports
import os
import sys
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

# waymo open dataset reader
from tools.waymo_reader.simple_waymo_open_dataset_reader import utils as waymo_utils
from tools.waymo_reader.simple_waymo_open_dataset_reader import dataset_pb2, label_pb2

# object detection tools and helper functions
import misc.objdet_tools as tools

# visualize lidar point-cloud
def show_pcl(pcl):

    ####### ID_S1_EX2 START #######     
    #######
    print("student task ID_S1_EX2")

    # o3d.utility.set_verbosity_level(o3d.utility.VerbosityLevel.Debug)

    global frame_render_loop
    frame_render_loop = True
    # step 1 : initialize open3d with key callback and create window
    def skip_to_next_frame(vis):
        # This callback lets us break out of the simulated visualization.run() loop while still preservering the visualization window
        global frame_render_loop
        frame_render_loop = False
        vis.poll_events()

    def destroy_vis(vis):
        global frame_render_loop
        frame_render_loop = False
        vis.close() # notify the window to be closed. 
        # vis.destroy_window() # This kills the entire app, so not so useful
        vis.poll_events() # call this once to process the close Event

    if not show_pcl.is_o3d_initialized:
        show_pcl.vis = o3d.visualization.VisualizerWithKeyCallback()
        show_pcl.vis.register_key_callback(262, skip_to_next_frame) # right arrow
        show_pcl.vis.register_key_callback(256, destroy_vis) #Esc
        show_pcl.vis.create_window()
    
    # step 2 : create instance of open3d point-cloud class
    if not show_pcl.is_o3d_initialized:
        # For add/update_geometry to work, we need to keep the same "pointer"
        show_pcl.pcd = o3d.geometry.PointCloud()

    # step 3 : set points in pcd instance by converting the point-cloud into 3d vectors (using open3d function Vector3dVector)
    show_pcl.pcd.points = o3d.utility.Vector3dVector(pcl[:,:3])

    # step 4 : for the first frame, add the pcd instance to visualization using add_geometry; for all other frames, use update_geometry instead
    if not show_pcl.is_o3d_initialized:
        show_pcl.vis.add_geometry(show_pcl.pcd)
    else:
        show_pcl.vis.update_geometry(show_pcl.pcd)
    
    # step 5 : visualize point cloud and keep window open until right-arrow is pressed (key-code 262)
    show_pcl.is_o3d_initialized = True

    # We simulate the Visualization.run() loop here, and use the callback(s) to give control back to the caller without destroying the window
    while (frame_render_loop):
        show_pcl.vis.poll_events()
        show_pcl.vis.update_renderer()


# A global flag to initialize o3d only once. This is needed given how show_pcl() is called in a loop (loop_over_dataset.py)
show_pcl.is_o3d_initialized = False

    #######
    ####### ID_S1_EX2 END #######     

# visualize range image
def show_range_image(frame, lidar_name):

    ####### ID_S1_EX1 START #######     
    #######
    print("student task ID_S1_EX1")

    # step 1 : extract lidar data and range image for the roof-mounted lidar
    lidar = next(l for l in frame.lasers if l.name == lidar_name)
    
    # step 2 : extract the range and the intensity channel from the range image
    if len(lidar.ri_return1.range_image_compressed) > 0: # use first response
        ri = dataset_pb2.MatrixFloat()
        ri.ParseFromString(zlib.decompress(lidar.ri_return1.range_image_compressed))
        ri = np.array(ri.data).reshape(ri.shape.dims)

    # step 3 : set values <0 to zero
    ri[ri<0] = 0.0
    
    # step 4 : map the range channel onto an 8-bit scale and make sure that the full range of values is appropriately considered
    ri_range = ri[:,:,0]
    ri_range = ri_range * 255 / (np.amax(ri_range) - np.amin(ri_range))
    img_range = ri_range.astype(np.uint8)
    
    # step 5 : map the intensity channel onto an 8-bit scale and normalize with the difference between the 1- and 99-percentile to mitigate the influence of outliers
    ri_intensity = ri[:,:,1]
    # print (np.percentile(ri_intensity, 99), np.amax(ri_intensity)) # 0.546875 91648.0
    ri_intensity[ri_intensity<=np.percentile(ri_intensity, 1)] = 0.0
    ri_intensity[ri_intensity>np.percentile(ri_intensity, 99)] = np.percentile(ri_intensity, 99)
    ri_intensity = ri_intensity * 255 / (np.percentile(ri_intensity, 99) - np.percentile(ri_intensity, 1)) 
    img_intensity = ri_intensity.astype(np.uint8)

    
    # step 6 : stack the range and intensity image vertically using np.vstack and convert the result to an unsigned 8-bit integer
    img_range_intensity = np.vstack((img_range, img_intensity))
    
    # Crop image to +/- 90 deg
    deg_90 = np.int_(img_range_intensity.shape[1]/4)
    lr_center = np.int_(img_range_intensity.shape[1]/2)
    img_range_intensity = img_range_intensity[:, lr_center-deg_90:lr_center+deg_90]

    #######
    ####### ID_S1_EX1 END #######     
    
    return img_range_intensity


# util method
def render_image_map(image_map, name = 'img'):
    image_map = image_map * 255
    image_map = image_map.astype(np.uint8)
    cv2.imshow(name, image_map)
    if cv2.waitKey(0) & 0xFF == 27:
        cv2.destroyAllWindows()

# create birds-eye view of lidar data
def bev_from_pcl(lidar_pcl, configs):
    show_vis = False

    # remove lidar points outside detection area and with too low reflectivity
    mask = np.where((lidar_pcl[:, 0] >= configs.lim_x[0]) & (lidar_pcl[:, 0] <= configs.lim_x[1]) &
                    (lidar_pcl[:, 1] >= configs.lim_y[0]) & (lidar_pcl[:, 1] <= configs.lim_y[1]) &
                    (lidar_pcl[:, 2] >= configs.lim_z[0]) & (lidar_pcl[:, 2] <= configs.lim_z[1]))
    lidar_pcl = lidar_pcl[mask]
    
    # shift level of ground plane to avoid flipping from 0 to 255 for neighboring pixels
    lidar_pcl[:, 2] = lidar_pcl[:, 2] - configs.lim_z[0]

    # TODO: filter points with low reflectivity?  configs.lim_r = [0, 1.0] # reflected lidar intensity

    # convert sensor coordinates to bev-map coordinates (center is bottom-middle)
    ####### ID_S2_EX1 START #######     
    #######
    print("student task ID_S2_EX1")

    ## step 1 :  compute bev-map discretization by dividing x-range by the bev-image height (see configs)
    bev_discret_x =  (configs.lim_x[1] - configs.lim_x[0]) / configs.bev_height
    bev_discret_y =  (configs.lim_y[1] - configs.lim_y[0]) / configs.bev_width

    ## step 2 : create a copy of the lidar pcl and transform all metrix x-coordinates into bev-image coordinates    
    lidar_pcl_cpy = np.copy(lidar_pcl)
    lidar_pcl_cpy[:,0] = np.int_(lidar_pcl_cpy[:,0] / bev_discret_x)

    # step 3 : perform the same operation as in step 2 for the y-coordinates but make sure that no negative bev-coordinates occur
    lidar_pcl_cpy[:,1] = np.int_(lidar_pcl_cpy[:,1] / bev_discret_y + (configs.bev_width + 1) / 2)

    # step 4 : visualize point-cloud using the function show_pcl from a previous task
    if show_vis:
        show_pcl(lidar_pcl_cpy)
    
    #######
    ####### ID_S2_EX1 END #######     
    
    
    # Compute intensity layer of the BEV map
    ####### ID_S2_EX2 START #######     
    #######
    print("student task ID_S2_EX2")

    ## step 1 : create a numpy array filled with zeros which has the same dimensions as the BEV map
    intensity_map = np.zeros((configs.bev_height+1, configs.bev_width+1))

    # step 2 : re-arrange elements in lidar_pcl_cpy by sorting first by x, then y, then -z (use numpy.lexsort)
    lidar_pcl_cpy[lidar_pcl_cpy[:,3] > configs.lim_r[1],3] = configs.lim_r[1] # Cap max intensity to 1.0 some values are in the thousands
    lidar_pcl_cpy[lidar_pcl_cpy[:,3] < configs.lim_r[0],3] = configs.lim_r[0]
    idx_intensity = np.lexsort((-lidar_pcl_cpy[:,3], lidar_pcl_cpy[:,1], lidar_pcl_cpy[:,0]))
    lidar_pcl_top = lidar_pcl_cpy[idx_intensity]

    ## step 3 : extract all points with identical x and y such that only the top-most z-coordinate is kept (use numpy.unique)
    ##          also, store the number of points per x,y-cell in a variable named "counts" for use in the next task
    _, idx_intensity_unique, counts = np.unique(lidar_pcl_top[:,0:2], axis=0, return_index=True, return_counts=True)
    lidar_pcl_top = lidar_pcl_top[idx_intensity_unique]
    #NOTE: it does not look like the "counts" calculation is needd here. It is already calculated below for density calculation


    ## step 4 : assign the intensity value of each unique entry in lidar_top_pcl to the intensity map 
    ##          make sure that the intensity is scaled in such a way that objects of interest (e.g. vehicles) are clearly visible    
    ##          also, make sure that the influence of outliers is mitigated by normalizing intensity on the difference between the max. and min. value within the point cloud
    intensity_map[np.int_(lidar_pcl_top[:,0]), np.int_(lidar_pcl_top[:,1])] = lidar_pcl_top[:,3] / (np.amax(lidar_pcl_top[:,3])- np.amin(lidar_pcl_top[:,3]))

    ## step 5 : temporarily visualize the intensity map using OpenCV to make sure that vehicles separate well from the background
    if show_vis:
        render_image_map(intensity_map, "img_intesity")

    #######
    ####### ID_S2_EX2 END ####### 


    # Compute height layer of the BEV map
    ####### ID_S2_EX3 START #######     
    #######
    print("student task ID_S2_EX3")

    ## step 1 : create a numpy array filled with zeros which has the same dimensions as the BEV map
    height_map = np.zeros((configs.bev_height+1, configs.bev_width+1))

    ## step 2 : assign the height value of each unique entry in lidar_top_pcl to the height map 
    ##          make sure that each entry is normalized on the difference between the upper and lower height defined in the config file
    ##          use the lidar_pcl_top data structure from the previous task to access the pixels of the height_map
    sorted_idx_height = np.lexsort((-lidar_pcl_top[:,2], lidar_pcl_top[:,1], lidar_pcl_top[:,0]))
    lidar_pcl_top = lidar_pcl_top[sorted_idx_height]
    _, idx_height_unique = np.unique(lidar_pcl_top[:, 0:2], axis=0, return_index=True)
    lidar_pcl_top = lidar_pcl_top[idx_height_unique]

    height_map[np.int_(lidar_pcl_top[:,0]), np.int_(lidar_pcl_top[:,1])] = lidar_pcl_top[:, 2] / float(np.abs(configs.lim_z[1] - configs.lim_z[0]))


    ## step 3 : temporarily visualize the intensity map using OpenCV to make sure that vehicles separate well from the background
    if show_vis:
        render_image_map(height_map, "img_height")

    #######
    ####### ID_S2_EX3 END #######       

    # Compute density layer of the BEV map
    density_map = np.zeros((configs.bev_height + 1, configs.bev_width + 1))
    _, _, counts = np.unique(lidar_pcl_cpy[:, 0:2], axis=0, return_index=True, return_counts=True)
    normalizedCounts = np.minimum(1.0, np.log(counts + 1) / np.log(64)) 
    density_map[np.int_(lidar_pcl_top[:, 0]), np.int_(lidar_pcl_top[:, 1])] = normalizedCounts
        
    # assemble 3-channel bev-map from individual maps
    bev_map = np.zeros((3, configs.bev_height, configs.bev_width))
    bev_map[2, :, :] = density_map[:configs.bev_height, :configs.bev_width]  # r_map
    bev_map[1, :, :] = height_map[:configs.bev_height, :configs.bev_width]  # g_map
    bev_map[0, :, :] = intensity_map[:configs.bev_height, :configs.bev_width]  # b_map

    # expand dimension of bev_map before converting into a tensor
    s1, s2, s3 = bev_map.shape
    bev_maps = np.zeros((1, s1, s2, s3))
    bev_maps[0] = bev_map

    bev_maps = torch.from_numpy(bev_maps)  # create tensor from birds-eye view
    input_bev_maps = bev_maps.to(configs.device, non_blocking=True).float()
    return input_bev_maps
