import math
import time
import os, glob
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from robotarium_abc import *
import re

# Robotarium This object provides routines to interface with the Robotarium.
#
# THIS CLASS SHOULD NEVER BE MODIFIED OR SUBMITTED

class Robotarium(RobotariumABC):

        def __init__(self, number_of_robots=-1, show_figure=True, sim_in_real_time = True, initial_conditions=np.array([])):
            super().__init__(number_of_robots, show_figure, sim_in_real_time, initial_conditions)

            #Initialize some rendering variables
            self.previous_render_time = time.time()
            self.sim_in_real_time = sim_in_real_time

            #Initialize checks for step and get poses calls
            self._called_step_already = True
            self._checked_poses_already = False

            #Initialization of error collection.
            self._errors = {}

            #Initialize steps
            self._iterations = 0 

            dir = './images'
            filelist = glob.glob(os.path.join(dir, "*"))
            for f in filelist:
                os.remove(f)

        def get_poses(self):
            """Returns the states of the agents.

            -> 3xN numpy array (of robot poses)
            """

            assert(not self._checked_poses_already), "Can only call get_poses() once per call of step()."
            # Allow step() to be called again.
            self._called_step_already = False
            self._checked_poses_already = True 

            return self.poses

        def call_at_scripts_end(self):
            """Call this function at the end of scripts to display potentail errors.  
            Even if you don't want to print the errors, calling this function at the
            end of your script will enable execution on the Robotarium testbed.
            """
            image_folder = './images'
            video_name = 'rps/video.mp4'

            images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
            images = sorted(images, key=lambda x: (int(re.sub('\D','',x)),x))
            frame = cv2.imread(os.path.join(image_folder, images[0]))
            height, width, layers = frame.shape

            fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
            video = cv2.VideoWriter(video_name, fourcc, 30, (width,height))

            for image in images:
                video.write(cv2.imread(os.path.join(image_folder, image)))

            cv2.destroyAllWindows()
            video.release()

            dir = './images'
            filelist = glob.glob(os.path.join(dir, "*"))
            for f in filelist:
                os.remove(f)


            print('##### DEBUG OUTPUT #####')
            print('Your simulation will take approximately {0} real seconds when deployed on the Robotarium. \n'.format(math.ceil(self._iterations*0.033)))

            if bool(self._errors):
                if "boundary" in self._errors:
                    print('\t Simulation had {0} {1}\n'.format(self._errors["boundary"], self._errors["boundary_string"]))
                if "collision" in self._errors:
                    print('\t Simulation had {0} {1}\n'.format(self._errors["collision"], self._errors["collision_string"]))
                if "actuator" in self._errors:
                    print('\t Simulation had {0} {1}'.format(self._errors["actuator"], self._errors["actuator_string"]))
            else:
                print('No errors in your simulation! Acceptance of your experiment is likely!')

            return

        def step(self):
            """Increments the simulation by updating the dynamics.
            """
            assert(not self._called_step_already), "Make sure to call get_poses before calling step() again."

            # Allow get_poses function to be called again.
            self._called_step_already = True
            self._checked_poses_already = False

            # Validate before thresholding velocities
            self._errors = self._validate()
            self._iterations += 1


            # Update dynamics of agents
            self.poses[0, :] = self.poses[0, :] + self.time_step*np.cos(self.poses[2,:])*self.velocities[0, :]
            self.poses[1, :] = self.poses[1, :] + self.time_step*np.sin(self.poses[2,:])*self.velocities[0, :]
            self.poses[2, :] = self.poses[2, :] + self.time_step*self.velocities[1, :]
            # Ensure angles are wrapped
            self.poses[2, :] = np.arctan2(np.sin(self.poses[2, :]), np.cos(self.poses[2, :]))

            # Update graphics
            if(self.show_figure):
                if(self.sim_in_real_time):
                    t = time.time()
                    while(t - self.previous_render_time < self.time_step):
                        t=time.time()
                    self.previous_render_time = t

                for i in range(self.number_of_robots):
                    self.chassis_patches[i].center = self.poses[:2, i]
                    self.chassis_patches[i].orientation = self.poses[2, i] + math.pi/4

                    self.right_wheel_patches[i].center = self.poses[:2, i]+self.robot_radius*np.array((np.cos(self.poses[2, i]+math.pi/2), np.sin(self.poses[2, i]+math.pi/2)))+\
                                            0.04*np.array((-np.sin(self.poses[2, i]+math.pi/2), np.cos(self.poses[2, i]+math.pi/2)))
                    self.right_wheel_patches[i].orientation = self.poses[2, i] + math.pi/4

                    self.left_wheel_patches[i].center = self.poses[:2, i]+self.robot_radius*np.array((np.cos(self.poses[2, i]-math.pi/2), np.sin(self.poses[2, i]-math.pi/2)))+\
                                            0.04*np.array((-np.sin(self.poses[2, i]+math.pi/2), np.cos(self.poses[2, i]+math.pi/2)))
                    self.left_wheel_patches[i].orientation = self.poses[2,i] + math.pi/4
                    
                    self.right_led_patches[i].center = self.poses[:2, i]+0.75*self.robot_radius*np.array((np.cos(self.poses[2,i]), np.sin(self.poses[2,i])))-\
                                    0.04*np.array((-np.sin(self.poses[2, i]), np.cos(self.poses[2, i])))
                    self.left_led_patches[i].center = self.poses[:2, i]+0.75*self.robot_radius*np.array((np.cos(self.poses[2,i]), np.sin(self.poses[2,i])))-\
                                    0.015*np.array((-np.sin(self.poses[2, i]), np.cos(self.poses[2, i])))

                self.figure.savefig("./images/{0}".format(self._iterations))
                #self.figure.canvas.flush_events()

