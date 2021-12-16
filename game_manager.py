def screen_to_scene(self, screen_point):
    camera_shift = [self.last_clicked_camera_pos[0], -self.last_clicked_camera_pos[1]]
    screen_point = list(screen_point)
    scene_point = [(screen_point[0] - self.screen_width / 2) / self.zoom + camera_shift[0],
                   (screen_point[1] - self.screen_height / 2) / self.zoom + camera_shift[1]]
    scene_point[1] = -scene_point[1]   # Axes origin is left-top angle
    return scene_point


def move_camera(direction):
    """
    Function for moving the camera accordingly to a given direction
    :param direction: given direction
    """
    camera_pos[0] = camera_pos[0] + direction[0] * camera_speed * dt
    camera_pos[1] = camera_pos[1] + direction[1] * camera_speed * dt


def do_zoom(self, direction):
    """
    Function for zooming
    :param self: zoom owner
    :param direction: zoom direction
    """
    self.zoom = self.zoom + direction * self.zoom_speed * self.dt


click_pos = None

zoom = 4
screen_width = 1280
screen_height = 600
scene_width = screen_width//zoom
scene_height = screen_height//zoom
ui_panel_width = screen_width // 3
borders_width = 2  # Map visual borders

ui_click = 0
click_delay = 10

FPS = 200
Game_FPS = 60
frame = 0
dt = 0.01

camera_pos = [scene_width/2, scene_height/2]
last_clicked_camera_pos = camera_pos
camera_speed = 50 * 1.5  # Vector magnitude
zoom_speed = 3
