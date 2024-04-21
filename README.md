ConvertVolume and pressure are two files that convert an image of a graph into two text files that contain the matching input and output points of the graph using an acceptable HSV range for the graph. Each file outputs two arrays, pixels_x.txt and pixels_y.txt as well as 'out.png', a plotted png of the two arrays.

ConvertVolume converts a graph of volume (ml per second) to the corresponding points of the graph using HSV. The file pressure converts a graph of pressure (ml per second) to the corresponding points of the graph using HSV.

Note the images need to be properly rotated to use the files. See 'DS14_P1_Pressure.png' and 'ZoomMechVent_DS25_P1.png' for examples of rotation.
 
Users can specify the axises scale. Users must define where the true (zero, zero) is on the graph, as well as where the first numerical scale for both the horizontal and vertical axis are. 
  
The only difference between the pressure and ConvertVolume file is the definition of the acceptable HSV range. The user should be able to generalize any image of a graph given the scales and accepted HSV are updated. Mac Users can use 'Digital Color Meter' to determine acceptable ranges of HSV.

Two images with graphs, one with pressure, the other with volume, are included to help test each function. Note the 'USER:' notes throughout the code.