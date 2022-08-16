# Mid-term Project writeup

## Intro

Sections below summarize results & outputs from various steps in this project.
The [commits messages](https://github.com/brijs/udacity-self-driving-project-2/commits/main) contain the corresponding exercise IDs for easy identification.

## Step 1 : Compute Lidar Point-CLoud from Range Image
### [S1_EX1] : Visualize range image channels
<img src="screenshots/S1_EX1_range_image.png" width="800">
<figcaption>Figure 1: Stacked range & intensity channels</figcaption>

### [S1_EX2] : Visualize Point Cloud
<p align="center">
    <img src="screenshots/S1_EX2_PCL_animation.gif" width="600">
    <figcaption align="center">Animation 1: Point Cloud Open3d Visualization</figcaption>
</p>


#### Examples with varying degree of visibility

Below are some example images along with a brief text description.
|                                                          |                                                               |
|:--------------------------------------------------------:|:-------------------------------------------------------------:|
|  <img src="screenshots/S1_EX2_PCL_1.jpg" width="400" >   |     <img src="screenshots/S1_EX2_PCL_2.jpg" width="400">      |
|          <figcaption>Car too close</figcaption>          | <figcaption>Rear view: Car hidden behind another</figcaption> |
|                                                          |                                                               |
|  <img src="screenshots/S1_EX2_PCL_3.jpg" width="400" >   |     <img src="screenshots/S1_EX2_PCL_4.jpg" width="400">      |
|  <figcaption>Left: Tyres & Window features</figcaption>  |         <figcaption>Obstructed by trees</figcaption>          |
|                                                          |                                                               |
|  <img src="screenshots/S1_EX2_PCL_4a.jpg" width="400" >  |     <img src="screenshots/S1_EX2_PCL_5.jpg" width="400">      |
|    <figcaption>Car's bottom out of view</figcaption>     |           <figcaption>Car with trailer</figcaption>           |
|                                                          |                                                               |
|  <img src="screenshots/S1_EX2_PCL_6.jpg" width="400" >   |     <img src="screenshots/S1_EX2_PCL_7.jpg" width="400">      |
|     <figcaption>Tyres, windows, bumpers</figcaption>     |             <figcaption>Car Mirrors</figcaption>              |
|                                                          |                                                               |
|  <img src="screenshots/S1_EX2_PCL_8.jpg" width="400" >   |     <img src="screenshots/S1_EX2_PCL_9.jpg" width="400">      |
| <figcaption>Construction truck & Road Signs</figcaption> |        <figcaption>Car behind pedestrians</figcaption>        |
|                                                          |                                                               |
|  <img src="screenshots/S1_EX2_PCL_10.jpg" width="400" >  |                                                               |
|     <figcaption>Cars behind other cars</figcaption>      |                   <figcaption></figcaption>                   |

#### Stable Vehicle Features
- Tyres
- Window shapes
- Windshield
- Side Mirrors
- Bumpers
- Vertical sides of the cars

In general, surfaces with **better relfectivity** register better on radar. Transparent (windows & windshields etc) have low reflectivity and therefore the range intensity is low. However, this transparency seems to help as the shape of the windshield or windows are easily identifiable. 


## Step 2 : Create Birds-Eye View from Lidar PCL

### [S2_EX1] : Convert sensor coordinates to BEV-map coordinates 
|                                                     |
|:---------------------------------------------------:|
| <img src="screenshots/S2_EX1_bev.jpg" width="400" > |
|        <figcaption>BEV from PCL</figcaption>        |

### [S2_EX2] & [S2_EX3] : Compute Intensity & Height layers of BEV-map
|                                                                   |                                                               |
| :---------------------------------------------------------------: | :-----------------------------------------------------------: |
| <img src="screenshots/S2_EX1_bev_img_intensity.jpg" width="400" > | <img src="screenshots/S2_EX1_bev_img_height.jpg" width="400"> |
|            <figcaption>BEV Img Intensity</figcaption>             |            <figcaption>BEV Img Height</figcaption>            |


## Step 3 : Model-based Object Detection in BEV Image

### [S3_EX1] & [S3_EX2] : Add FPN Resnet model, and extract 3D bounding boxes from model response
|                                                                  |
|:----------------------------------------------------------------:|
|   <img src="screenshots/S3_EX_model_detect.jpg" width="400" >    |
| <figcaption>FPN Resnet model output: bounding boxes</figcaption> |



## Step 4 : Performance Evaluation for Object Detection

![](screenshots/S4_precision_recall.jpg)
<figcaption>Precision Recall performance</figcaption>