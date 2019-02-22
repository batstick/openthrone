import random
import numpy

# code plan:
# start the level with a single point in the middle, then build from it.
# this ensures that the level is one contiguous thing so that there arent
# any inaccessible areas. build up, then left, then down, then right.
# then loop a small number of times. us cool shapes to make it not look
# like a weird tree/weed/crab thing. one of these -> * but bigger.
#
# spawning will start by randomly testing all the edge areas, then slowly
# working its way in if need be.
#
# IMPORTANT NOTICE: X AND Y ARE REVERSED IN THE PAINT DEF. IT HAS TO BE
# LIKE THAT OR ELSE IT LOOKS BAD ON THE OUTPUT!!!
#
# this is stretching the limit of my brain, someone please review this
#
# maybe setting different values could be used to determine edges of
# objects that i drew. like 2 could be the edges and would be protected
# from being overwritten by 1s with an if statement...
#
# 1s are where the ground is. everything else is wall. walls are assumed.
# they are considered default. if its not explicitly a floor, its a wall.
# this will make the levels easier to process as theres more wall than
# floor so just calc the floor instead for hitboxes inversely. 

grid_size = 32 # specify size of the grid, 32 is big
level_grid = numpy.empty((grid_size,grid_size)) # this amkes a 32x32 grid
level_grid[:] = 0 # this sets them all to zero!

#print(len(level_grid)) # shows the length of the grid
#print(level_grid[1,1]) # shows whats at pos 1,1 in the grid

brush = [16,16] # this is the start location of the brush

def paint(brush,level_grid):
	level_grid[brush[1],brush[0]] = 1
	return level_grid

paint(brush,level_grid)

#brush = [(brush[0]+1),(brush[1]+0)] #this paints the second point
#paint(brush,level_grid)

def paint_line_h(brush,level_grid,line_size): #paints a line from where the brush is
	brush_start = [(brush[0]),(brush[1])]

	var = 0

	while var < line_size:
		brush[0] = brush[0] + 1
		paint(brush,level_grid)
		var = var + 1

	return level_grid

########################################################################
###PAINT HERE###########################################################
########################################################################

level_grid = paint_line_h(brush,level_grid,3) #draw a line 3 units long from the start point :)

########################################################################
####THIS IS TO BE RUN LAST##############################################
########################################################################

i = 0

while i < 32: # this gives a more readable output than just printing
	list1 = level_grid[i]
	str1 = ''.join(str(e) for e in list1)
	print((str1.replace('0.0','0')).replace('1.0','1')) #fixes doubles
	i = i + 1

# END OF CODE