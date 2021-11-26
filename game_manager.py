import numpy as np

def ScreenToScene(self, screen_point):
    camera_shift = np.array([self.last_clicked_camera_pos[0], -self.last_clicked_camera_pos[1]])
    scene_point = (np.array(list(screen_point)) - np.array([self.screen_width/2, self.screen_height/2]) )/self.zoom + camera_shift
    scene_point[1] = -scene_point[1]   #axes origin is left-top angle
    return scene_point

def move_camera(self, direction):
    self.camera_pos = self.camera_pos + np.array(list(direction) )*self.camera_speed*self.dt

clickpos = None

zoom = 10
screen_width = 1280
screen_height = 650
scene_width = screen_width/zoom
scene_height = screen_height/zoom

FPS = 200
Game_FPS = 60
frame = 0
dt = 0.01

camera_pos = np.array([scene_width/2, scene_height/2])
last_clicked_camera_pos = camera_pos
camera_speed = 50       #vector magnitude