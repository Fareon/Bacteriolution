import pygame as pg
import pygame_gui
import game_manager as gm
import color
import json


def change_cell_icon_color(new_color):
    new_color_hex = color.rgb_to_hex(new_color)
    with open("UI/layout.json", 'r') as json_file:
        json_object = json.load(json_file)        
        colours = json_object['#cell_icon']['colours']
    with open("UI/layout.json", 'w') as json_file:
        colours['normal_bg'] = new_color_hex  
        colours['hovered_bg'] = new_color_hex  
        colours['disabled_bg'] = new_color_hex  
        colours['selected_bg'] = new_color_hex  
        colours['active_bg'] = new_color_hex  
        json.dump(json_object, json_file)
change_cell_icon_color(color.INIT_PLAYER_COLOR)
#ui variables storage
class cell_icon:
    w, h = 120, 90
    x, y = gm.ui_panel_width*0.21, gm.screen_height*0.175
   
step = 45
class mutate:
    w, h = 50, -500
    x, y = cell_icon.x + cell_icon.w*0.5, cell_icon.y + cell_icon.h + 130 
    x1, x2 = 93, 200
    y1, y2 = 310, 47
    text = 'MUTATE'
    color = color.UI2
    text_surf = None
class gamespeed_text:
    w, h = mutate.w, mutate.h
    x, y = mutate.x + 5, mutate.y + step
    x1, x2 = mutate.x1 - 100, mutate.x2
    y1, y2 = mutate.y1 + step + 0, mutate.y2 + step - 45
    text = 'Game Speed'
    color = color.UI2
    text_surf = None
class scrollbar:
    w, h = mutate.w, mutate.h/2
    x, y = mutate.x + 5, mutate.y + step
    x1, x2 = mutate.x1, mutate.x2
    y1, y2 = mutate.y1 + step + 0, mutate.y2 + step - 45
    text = 'gamespeed_text'
    color = color.UI2
    text_surf = None
class radius:
    x, y = (gamespeed_text.x - 120, gamespeed_text.y + 95)
    x2, y2 = (gamespeed_text.x + gamespeed_text.w + 50, gamespeed_text.y + gamespeed_text.h)
    text = 'MAX RADIUS: 2'
    color = color.UI
    text_surf = None
class your_cell:
    x1, y1 = (10, -10)
    x2, y2 = (gm.ui_panel_width*0.9, gm.screen_height*0.2)
    x, y = x1 + 35, y1 + 25
    text = 'YOUR CELL'
    color = color.UI
    text_surf = None
class population:
    x, y = (radius.x, radius.y + 35)
    text = 'POPULATION: 0'
    color = color.UI
    text_surf = None
class speed:
    x, y = (gm.ui_panel_width*0.6, radius.y)
    text = 'SPEED: 0'
    color = color.UI
    text_surf = None 
class hunger:
    x, y = (speed.x, population.y)
    text = 'HUNGER: 0'
    color = color.UI
    text_surf = None 



manager = pygame_gui.UIManager((gm.screen_width, gm.screen_height), "UI/layout.json")
mutate_button = pygame_gui.elements.UIButton(relative_rect=pg.Rect((mutate.x1, mutate.y1),
                                                                   (mutate.x2, mutate.y2)),
                                                 text='', object_id=f"#mutate",
                                                 #parent_element = info_panel_button,
                                                 manager=manager)

info_panel_button = pygame_gui.elements.UIButton(relative_rect=pg.Rect((-20, -20), (gm.ui_panel_width, gm.screen_height*1.2)),
                                                 text='', object_id=f"#info_panel",
                                                 manager=manager)
cell_icon_button = pygame_gui.elements.UIButton(relative_rect=pg.Rect((cell_icon.x, cell_icon.y), (cell_icon.x + cell_icon.w, cell_icon.y + cell_icon.h)),
                                                 text='', object_id=f"#cell_icon",
                                                 parent_element = info_panel_button,
                                                 manager=manager)

'''gamespeed_text_button = pygame_gui.elements.UIButton(relative_rect=pg.Rect((gamespeed_text.x1, gamespeed_text.y1), 
                                                                  (gamespeed_text.x2, gamespeed_text.y2)),
                                                 text='', object_id=f"#mutate",
                                                 parent_element = info_panel_button,
                                                 manager=manager)'''

game_speed_scrbar = pygame_gui.elements.UIHorizontalScrollBar(relative_rect=pg.Rect((scrollbar.x1, scrollbar.y1), 
                                                                  (scrollbar.x2, scrollbar.y2)),
                                                 visible_percentage  = 0.3, object_id=f"#scroll_bar",
                                                 parent_element = info_panel_button,
                                                 manager=manager)
info_panel_button.change_layer(0)
pg.font.init()
pg.font.Font('UI/Pixeboy-z8XGD.ttf', 80)
bitfont = {80: pg.font.Font('UI/Pixeboy-z8XGD.ttf', 80), 20: pg.font.Font('UI/Pixeboy-z8XGD.ttf', 20),
           40: pg.font.Font('UI/Pixeboy-z8XGD.ttf', 40), 30: pg.font.Font('UI/Pixeboy-z8XGD.ttf', 30)}

text_elements = []
def generate_text():
    generate_sign(your_cell, size = 80)    
    generate_sign(radius, size = 30)    
    generate_sign(population, size = 30)
    generate_sign(hunger, size = 30)
    generate_sign(speed, size = 30)
    
    generate_sign(mutate, size = 30)
    generate_sign(gamespeed_text, size = 20)

def generate_sign(obj, size = 30):
    obj.text_surf = bitfont[size].render(obj.text, False, obj.color)
    text_elements.append(obj)

generate_text()
def draw_text(screen):
    for text in text_elements:
        if(text.text_surf is not None): screen.blit(text.text_surf, (text.x, text.y))

if __name__ == "__main__":
    exec(open("main.py").read())