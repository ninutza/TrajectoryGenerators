#! /usr/bin/python
import sys
import random
import math

NO_INTERS_X = 3;
NO_INTERS_Y = 4;

GRAN = 4; #block size (in m)
STEP = 1;

NO_VEH = 2;

RANGE_X = (NO_INTERS_X-1) * GRAN + 1;
RANGE_Y = (NO_INTERS_Y-1) * GRAN + 1;

# initialize all arrays needed for later
x_init=range(0,NO_VEH);
y_init=range(0,NO_VEH);
x_curr=range(0,NO_VEH);
y_curr=range(0,NO_VEH);
x_dest=range(0,NO_VEH);
y_dest=range(0,NO_VEH);
prob_turn=range(0,NO_VEH);
x_dir=range(0,NO_VEH);
y_dir=range(0,NO_VEH);

for i in range(0, NO_VEH):
  x_init[i] = random.randrange(0, NO_INTERS_X) * GRAN;
  y_init[i] = random.randrange(0, NO_INTERS_Y) * GRAN;

TARGET_TIME = max(NO_INTERS_X,NO_INTERS_Y) * GRAN;

#print "Will generate 21x21 grid of traffic (6x6 city blocks)";
#print "Start at ", x_init, ", ", y_init;
#print "Finish at ", x_dest, ", ", y_dest;

for i in range(0, NO_VEH):
  x_curr[i] = x_init[i];
  y_curr[i] = y_init[i];
  x_dest[i] = x_curr[i];
  y_dest[i] = y_curr[i];

# in  city: 0.8 (more often than not, will change direction)
# in rural: 0.4 (change direction at less than half of main road intersections)
# in  hwy : 0.1 (do no change direction unless forced to) 

CITY_PROB = 0.8;
RURAL_PROB = 0.4;
HWY_PROB = 0.1;

DEF_PROB = CITY_PROB;
t_curr = 0;
f = open("multi_traj.txt", "w")


while (t_curr < TARGET_TIME):

  for i in range(0, NO_VEH):
    if (x_dest[i] == x_curr[i]) and (y_dest[i] == y_curr[i]): # if this node has reached destination (or just started), get new destination
      while(x_dest[i] == x_curr[i]) and (y_dest[i] == y_curr[i]):	# to avoid trivial routes
        x_dest[i] = random.randrange(0, NO_INTERS_X) * GRAN;
        y_dest[i] = random.randrange(0, NO_INTERS_Y) * GRAN;

      x_init[i] = x_curr[i];			# reinitialize source of node to current position
      y_init[i] = y_curr[i];
      prob_turn[i] = DEF_PROB;                  # probability of turning depends on scenario initially (becomes 0 when on final stretch)

      print "Node ", i, "reassigned from (", x_init[i], ", ", y_init[i], ") to (", x_dest[i], ", ", y_dest[i], ") at time ", t_curr
  
  #establish initial direction axis along longest distance to destination
  for i in range(0, NO_VEH):
    if( abs(x_dest[i] - x_curr[i]) > abs(y_dest[i] - y_curr[i]) ):
      x_dir[i] = STEP * (x_dest[i] - x_curr[i])/(abs(x_dest[i] - x_curr[i])); 
      y_dir[i] = 0;
    else:
      y_dir[i] = STEP * (y_dest[i] - y_curr[i])/(abs(y_dest[i] - y_curr[i]));
      x_dir[i] = 0;


  #print car positions on one line in output file
  f.write(str(t_curr));
  for i in range(0, NO_VEH):
    f.write(' ' + str(x_curr[i]) + ' ' + str(y_curr[i]));
  f.write('\n');

  for i in range(0, NO_VEH):    # each vehicle decides timestep move independently
    #insert small probability of not moving at all, to vary speed from nominal time increment
    move_prob = random.random()

    if move_prob < 0.1: # stay in place with probability 10%
      x_curr[i] = x_curr[i];
      y_curr[i] = y_curr[i];
    else:		      # with probability 90%, choose to move
      if (x_curr[i] % GRAN == 0) and (y_curr[i] % GRAN == 0):	#at an intersection
        if (x_curr[i] == x_dest[i]):	# arrived on x coordinate of destination, only direction can be y
          y_dir[i] = STEP * (y_dest[i] - y_curr[i])/(abs(y_dest[i] - y_curr[i]));
          x_dir[i] = 0;
          prob_turn[i] = 0;
        else:
          if (y_curr[i] == y_dest[i]):  # arrived on y coordinate of destination, only direction can be x
            x_dir[i] = STEP * (x_dest[i] - x_curr[i])/(abs(x_dest[i] - x_curr[i])); 
            y_dir[i] = 0;
            prob_turn[i] = 0;

        choice = random.random()
        # print choice;
        if choice < prob_turn[i]: 	# change current direction with prob_turn chance
          if x_dir[i] == 0:        # if current direction is along y
            x_dir[i] = STEP * (x_dest[i] - x_curr[i])/(abs(x_dest[i] - x_curr[i]));
            y_dir[i] = 0;
          else:		      # else, current direction must have been x
            y_dir[i] = STEP * (y_dest[i] - y_curr[i])/(abs(y_dest[i] - y_curr[i]));
            x_dir[i] = 0;
      x_curr[i] = x_curr[i] + x_dir[i];
      y_curr[i] = y_curr[i] + y_dir[i];

  # time value only updates after all vehicles have moved (silly omission)
  t_curr = t_curr + 1;
      
# print final position of cars
f.write(str(t_curr));
for i in range(0, NO_VEH):
  f.write(' ' + str(x_curr[i]) + ' ' + str(y_curr[i]));
f.write('\n');

