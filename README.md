## how to use FindCoordinates:
Step1: create a directory and name it Surface_***
       here, *** is the gan generated img without .jpg extension

Step2: put two images, the gan generated img(with red dots that specially generated, it should be named as ***_red.jpg) and the generated image without red dots(it should be named as ***.jpg), into the directory above

Step3: open N0_RunMeOnly.py and change the string pass to variable "surface_name"

Step4: clik Run

-----------------------------------------
■■■ If we want to visualize the grid in 3d:
we need to put "coordinates_space.json" under the folder "Surface_***" first
and then run the N7_UseCoordTopoDrawGrid_3D.py
