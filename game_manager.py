import numpy as np

def ScreenToScene(screen_point):
    scene_point = (np.array(list(screen_point)) - np.array([width/2, height/2]) )/zoom - camera_pos
    scene_point[1] = -scene_point[1]   #axes origin is left-top angle
    return scene_point

clickpos = None
zoom = 10
width = 1280
height = 650
FPS = 60
camera_pos = np.array([0, 0])