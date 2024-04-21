#!/usr/bin/env python
# This file converts color specific pixel from a graph into a list. This files takes in a png file of a continous graph where the color of the graph is based off HSV and outputs two text files of discritization of points on the graph, one file for the horizontal axis and one text file for the vertial axis values. For the pressure file, the outputs are a list of time points and pressure values. Please make note of comments labeled # USERS: .

# The imported images are rotated so that the top of the image is a "sideways" vertical axis, the left of the image is a "sideways" horizontal axis. 

# USERS: will need to update lines 51-53, 68, 89,134, and 136 for specific situations. line 102 is specific to the color range of a users graph

#Import the classes use 
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
  


# npArr is the array that results from finding all of a 'certain colored' pixels
# this finds our median best points so that we dont have a "clump" of points but rather a beautiful line  
# NOTE -- this method only works because the Y values are garunteed to be ordered w.r.t the corresponding x values.
def choose_best_points(npArr):
  # numpy gives us an array containing an array of x coordinates
  # and an array of y coordinates, so we grab those arrays here.
  # NOTE -- for this script, our images are rotated
  xs = npArr[1]
  ys = npArr[0]
  # these will be the arrays we will return out from this function, will print out as .txt
  outX, outY = [], []
  # find the unique elements and their indicies in the original array of ys.
  #if didn't have return_index=True then couldn't get back indicies
  uniques, indicies = np.unique(ys, return_index=True)
  
  # for each index of a unique y value
  for i in range(0, len(indicies)):
    # if we can compare the current index to the next index
    if i + 1 < len(indicies):
      # grab the index of the current unique value and the index of the next unique value
      currIdx, nextIdx = indicies[i], indicies[i + 1]
      # find the index in the array of ys that would be inbetween our two unique values
      median = int((nextIdx - currIdx) / 2)
      # grab the corresponding element from the original arrays and put them in our arrays
      outX.append(xs[currIdx + median])
      outY.append(ys[currIdx + median])

  # return a numpy array that is like the one we got as input
  return np.asarray([outX, outY])


 # USER: For every image/graph, you need to update zeroZero, secondYPixels, secondXPixels. These are the true pixel values at the (zero, zero) of your graph, at the (zero, First labled X pixel Height,), and at the (First labled Y pixel Height, zero)
# this command gives us pixel/ml and pixel/second
# tick want (first two in time) to upper left hand corner, y values should be the same. Put these values in firstXPixels and secondXPixels. You should do this for the rotated image 
# For image 'DS14_P1_Pressure.png', zeroZero = (76, 48), secondYPixels = (76, 146), secondXPixels = (121,48)
def map_to_units(filteredNpArray):
  zeroZero = (64, 53)
  secondYPixels = (64,127)
  secondXPixels = (91, 53)

  
  xPixels = filteredNpArray[0]
  yPixels = filteredNpArray[1]

  pixelsPerMl = abs(zeroZero[1] - secondYPixels[1])
  pixelsPerSecond = abs(zeroZero[0] - secondXPixels[0])

  offsetX = zeroZero[0] / pixelsPerSecond
  offsetY = zeroZero[1] / pixelsPerMl

#the five depends on the unit/scale of the vertical axis
# USER: update the vertAxisScale. This is based of the scale of the vertical axis of the non-rotated image
# For "DS14_P1_Pressure.png", vertAxisScale = 10
  vertAxisScale = 10
  xs = [((xPx / pixelsPerSecond) - offsetX)* vertAxisScale for xPx in xPixels]
  ys = [((yPx / pixelsPerMl) - offsetY) for yPx in yPixels]

  return np.asarray([ys, xs])

def flip_array(processedNpArray):
  return np.asarray([processedNpArray[1], processedNpArray[0]])

def pressure():
    # USER: rotate the image before you import it in here
    # this function imports image and convert to RGB using HSV
    # . . HSV and RGB are ways of representing colors in bytes. HSV (Hue, Saturation, Value)
    # . . Is easier to use here since colors have a specific value range in which they fall,
    # . . so we only have to compare one number rather than three.
    #
    # . . We're only opening the image in both formats since we want to set the white pixels at
    # . . the end of this method. If we don't care about that visualization, we can just use HSV
    # . . all the way through
    #HSV allows you to have one value as opposed to three values like RGB
    # USER: must change the name of the rotated photo based on your use case
    RGBim = Image.open("DS14_P1_Pressure.png").convert('RGB')
    HSVim = RGBim.convert('HSV')
    #this is not necessary but helpful later when we "plot" our pixels for result.png
    RGBna = np.array(RGBim)
    HSVna = np.array(HSVim)

    # Extract Hue
    #for every row, and for every HSV in that row, take the first value wihc is the hue
    H = HSVna[:,:,0]

    # Find all color specific pixels, i.e. where 100 < Hue < 140
    #lo,hi = 100,140
    # USER: update HSV you will accept, for yellow pixels we use 50 < Hue < 58
    lo,hi=50,58
    # Rescale to 0-255, rather than 0-360 because we are using uint8
    lo = int((lo * 255) / 360)
    hi = int((hi * 255) / 360)
    # . . "query" arrays for certain conditions.
    # . . In this case, we want to find all the HSV values where the V is between lo and hi
    green = np.where((H>lo) & (H<hi))
    
    #rescale image so that we start at (0,0)
    #to do this we look at starting x and y values and subtract every element in green matrix by that pair
    # green = offset_xy(green)
    green = choose_best_points(green)

    # do the overlay before we map the green points to real values
    RGBna[[green[1], green[0]]] = [255,255,255]
    Image.fromarray(RGBna).save('result.png')

    # Formatting each value in the array as an integer number
    # By default, numpy uses %12f or something like that which leads to 12-digit percision
    # floating point values, but pixels are always integers so we don't want that.
    np.savetxt('pixels_y.txt', green[0], newline=',', fmt='%d')
    np.savetxt('pixels_x.txt', green[1], newline=',', fmt='%d')

    green = map_to_units(green)
    green = flip_array(green)
    # USER: You need to change cutoff of these values depending on each data set
    # Some cut offs may need to be longer or shorter, we do this specifically if our
    # pressure curves includes 2.5 breaths and we only want the first two full breaths
    print(len(green[0]))
    #print(green)
    green=list(green)
    green[0]=green[0][0:963]
    green[1]=green[1][0:963] 

    #print(green)

    np.savetxt('units_Pressure_y.txt', green[0], newline=',', fmt='%.4f')
    np.savetxt('units_Time_x.txt', green[1], newline=',', fmt='%.4f')

    plt.scatter(green[1], green[0])
    plt.savefig('out.png')

pressure()