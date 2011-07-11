#! /usr/bin/python
import sys
import random
import math

NO_INTERS_X = 1;
NO_INTERS_Y = 4;

GRAN = 1608; #block size (in m)
STEP = 3;

RANGE_X = (NO_INTERS_X-1) * GRAN + 1;
RANGE_Y = (NO_INTERS_Y-1) * GRAN + 1;

x_init = random.randrange(0, NO_INTERS_X) * GRAN;
y_init = random.randrange(0, NO_INTERS_Y) * GRAN;

TARGET_TIME = max(NO_INTERS_X,NO_INTERS_Y) * GRAN;

#print "Will generate 21x21 grid of traffic (6x6 city blocks)";
#print "Start at ", x_init, ", ", y_init;
#print "Finish at ", x_dest, ", ", y_dest;

x_curr = x_init;
y_curr = y_init;

# in  city: 0.8 (more often than not, will change direction)
# in rural: 0.4 (change direction at less than half of main road intersections)
# in  hwy : 0.1 (do no change direction unless forced to) 

CITY_PROB = 0.8;
RURAL_PROB = 0.4;
HWY_PROB = 0.1;

DEF_PROB = HWY_PROB;
t_curr = 0;
f = open("traj.txt", "w")


while (t_curr < TARGET_TIME):

  x_dest = x_curr;
  y_dest = y_curr;

  while(x_dest == x_curr) and (y_dest == y_curr):	# to avoid trivial routes
    x_dest = random.randrange(0, NO_INTERS_X) * GRAN;
    y_dest = random.randrange(0, NO_INTERS_Y) * GRAN;
  
  #print " *** Set new destination to ", str(x_dest), " ", str(y_dest)," ***";

  #establish initial direction axis along longest distance to destination
  if( abs(x_dest - x_curr) > abs(y_dest - y_curr) ):
    x_dir = STEP * (x_dest - x_curr)/(abs(x_dest - x_curr)); 
    y_dir = 0;
  else:
    y_dir = STEP * (y_dest - y_curr)/(abs(y_dest - y_curr));
    x_dir = 0;

  prob_turn = DEF_PROB; #higher prob of turning for city, lower for highway

  while (x_curr != x_dest) or (y_curr != y_dest):
    #print "Car at: ", x_curr, ", ", y_curr;
    f.write(str(t_curr) + ' ' + str(x_curr) + ' ' + str(y_curr) + '\n');

    #insert small probability of not moving at all, to vary speed from nominal time increment
    move_prob = random.random()

    if move_prob < 0.1: # stay in place with probability 10%
      x_curr = x_curr;
      y_curr = y_curr;
    else:		      # with probability 90%, choose to move
      if (x_curr % GRAN == 0) and (y_curr % GRAN == 0):	#at an intersection
        if (x_curr == x_dest):	# arrived on x coordinate of destination, only direction can be y
          y_dir = STEP * (y_dest - y_curr)/(abs(y_dest - y_curr));
          x_dir = 0;
          prob_turn = 0;
        else:
          if (y_curr == y_dest):  # arrived on y coordinate of destination, only direction can be x
            x_dir = STEP * (x_dest - x_curr)/(abs(x_dest - x_curr)); 
            y_dir = 0;
            prob_turn = 0;

        choice = random.random()
        # print choice;
        if choice < prob_turn: 	# change current direction with prob_turn chance
          if x_dir == 0:        # if current direction is along y
            x_dir = STEP * (x_dest - x_curr)/(abs(x_dest - x_curr));
            y_dir = 0;
          else:		      # else, current direction must have been x
            y_dir = STEP * (y_dest - y_curr)/(abs(y_dest - y_curr));
            x_dir = 0;
      x_curr = x_curr + x_dir;
      y_curr = y_curr + y_dir;
      t_curr = t_curr + 1;
      
#print "Car at: ", x_curr, ", ", y_curr;
f.write(str(t_curr) + ' ' + str(x_curr) + ' ' + str(y_curr) + '\n');



