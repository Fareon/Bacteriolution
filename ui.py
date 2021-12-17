from pygame import font, Rect
from pygame_gui import UIManager
from pygame_gui.elements import UIButton, UIHorizontalScrollBar
from game_manager import ui_panel_width, screen_height, screen_width
from color import INIT_PLAYER_COLOR, rgb_to_hex, UI, UI2
from json import load, dump

step = 45


def change_cell_icon_color(new_color):
    new_color_hex = rgb_to_hex(new_color)
    with open("UI/layout.json", 'r') as json_file:
        json_object = load(json_file)
        colours = json_object['#CellIcon']['colours']
    with open("UI/layout.json", 'w') as json_file:
        colours['normal_bg'] = new_color_hex  
        colours['hovered_bg'] = new_color_hex  
        colours['disabled_bg'] = new_color_hex  
        colours['selected_bg'] = new_color_hex  
        colours['active_bg'] = new_color_hex  
        dump(json_object, json_file)


change_cell_icon_color(INIT_PLAYER_COLOR)


# User interface variables storage
class CellIcon:
    w, h = 120, 90
    x, y = ui_panel_width*0.21, screen_height*0.175


class Mutate:
    w, h = 50, -500
    x, y = CellIcon.x + CellIcon.w * 0.5, CellIcon.y + CellIcon.h + 130
    x1, x2 = 93, 200
    y1, y2 = 310, 47
    text = 'MUTATE'
    color = UI2
    text_surf = None


class GameSpeedText:
    w, h = Mutate.w, Mutate.h
    x, y = Mutate.x + 5, Mutate.y + step
    x1, x2 = Mutate.x1 - 100, Mutate.x2
    y1, y2 = Mutate.y1 + step + 0, Mutate.y2 + step - 45
    text = 'Game Speed'
    color = UI2
    text_surf = None


class ScrollBar:
    w, h = Mutate.w, Mutate.h / 2
    x, y = Mutate.x + 5, Mutate.y + step
    x1, x2 = Mutate.x1, Mutate.x2
    y1, y2 = Mutate.y1 + step + 0, Mutate.y2 + step - 45
    text = 'GameSpeedText'
    color = UI2
    text_surf = None


class Radius:
    x, y = (GameSpeedText.x - 130, GameSpeedText.y + 95)
    x2, y2 = (GameSpeedText.x + GameSpeedText.w + 50, GameSpeedText.y + GameSpeedText.h)
    text = 'MAX RADIUS: 2'
    color = UI
    text_surf = None


class YourCell:
    x1, y1 = (10, -10)
    x2, y2 = (ui_panel_width*0.9, screen_height*0.2)
    x, y = x1 + 35, y1 + 25
    text = 'YOUR CELL'
    color = UI
    text_surf = None


class Population:
    x, y = (Radius.x, Radius.y + 35)
    text = 'POPULATION: 0'
    color = UI
    text_surf = None


class Speed:
    x, y = (ui_panel_width * 0.49, Radius.y)
    text = 'MAX SPEED: 0'
    color = UI
    text_surf = None


class Hunger:
    x, y = (Speed.x, Population.y)
    text = 'SELFISHNESS: 0'
    color = UI
    text_surf = None 


manager = UIManager((screen_width, screen_height), "UI/layout.json")

mutate_button = UIButton(
    relative_rect=Rect((Mutate.x1, Mutate.y1), (Mutate.x2, Mutate.y2)),
    text='', object_id=f"#Mutate",
    manager=manager
)
info_panel_button = UIButton(
    relative_rect=Rect((-20, -20), (ui_panel_width, screen_height*1.2)),
    text='', object_id=f"#info_panel",
    manager=manager
)
cell_icon_button = UIButton(
    relative_rect=Rect((CellIcon.x, CellIcon.y), (CellIcon.x + CellIcon.w, CellIcon.y + CellIcon.h)),
    text='', object_id=f"#CellIcon",
    parent_element=info_panel_button,
    manager=manager
)
game_speed_scroll_bar = UIHorizontalScrollBar(
    relative_rect=Rect((ScrollBar.x1, ScrollBar.y1), (ScrollBar.x2, ScrollBar.y2)),
    visible_percentage=0.3, object_id=f"#scroll_bar",
    parent_element=info_panel_button,
    manager=manager
)

info_panel_button.change_layer(0)
font.init()
font.Font('UI/Pixeboy-z8XGD.ttf', 80)
bitfont = {80: font.Font('UI/Pixeboy-z8XGD.ttf', 80), 20: font.Font('UI/Pixeboy-z8XGD.ttf', 20),
           40: font.Font('UI/Pixeboy-z8XGD.ttf', 40), 30: font.Font('UI/Pixeboy-z8XGD.ttf', 30)}

text_elements = []


def generate_text():
    generate_sign(YourCell, size=80)
    generate_sign(Radius, size=30)
    generate_sign(Population, size=30)
    generate_sign(Hunger, size=30)
    generate_sign(Speed, size=30)
    generate_sign(Mutate, size=30)
    generate_sign(GameSpeedText, size=20)


def generate_sign(obj, size=30):
    obj.text_surf = bitfont[size].render(obj.text, False, obj.color)
    text_elements.append(obj)


generate_text()


def draw_text(screen):
    for text in text_elements:
        if text.text_surf is not None:
            screen.blit(text.text_surf, (text.x, text.y))


if __name__ == "__main__":
    exec(open("main.py").read())
