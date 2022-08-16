# Mid-term writeup

## Intro

Sections below summarize results & outputs from various steps in this project.

## Step 1 
### [S1_EX1] : Visualize range image channels
<img src="screenshots/S1_EX1_range_image.png" width="900">
Figure 1: Stacked range & intensity channels

### [S1_EX2] : Visualize Point Cloud
<p align="center">
    <img src="screenshots/S1_EX2_PCL_animation.gif" width="900">
</p>
Animation 2: Point Cloud Open3d Visualization

#### Examples with varying degree of visibility

Below are some example images along with a brief text description.
|                                                          |                                                               |
| :------------------------------------------------------: | :-----------------------------------------------------------: |
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
|     <figcaption>Cars behind other cards</figcaption>     |                   <figcaption></figcaption>                   |

#### Stable Vehicle Features
- Tyres
- Window shapes
- Windshield
- Side Mirrors
- Bumpers
- Vertical sides of the cars

In general, surfaces with **better relfectivity** register better on radar. Transparent (windows & windshields etc) have low reflectivity and therefore the range intensity is low. However, this transparency seems to help as the shape of the windshield or windows are easily identifiable. 

