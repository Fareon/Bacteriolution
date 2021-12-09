import pygame as pg
import pygame_gui
import game_manager as gm
from color import color

#ui variables storage
class cell_icon:
    w, h = 120, 90
    x, y = gm.ui_panel_width*0.21, gm.screen_height*0.175
   
step = 40
class mutate:
    w, h = +cell_icon.w, -step*6
    x, y = cell_icon.x, cell_icon.y + 200    
    text_surf = None
class split:
    w, h = +cell_icon.w, -step*7.5
    x, y = cell_icon.x, mutate.y + step + 25
    text_surf = None
class radius:
    x, y = (split.x - 75, split.y + 95)
    x2, y2 = (split.x + split.w + 50, split.y + split.h)
    text = 'RADIUS: 2'
    color = color.GRAY
    text_surf = None
class your_cell:
    x1, y1 = (10, -10)
    x2, y2 = (gm.ui_panel_width*0.9, gm.screen_height*0.2)
    x, y = x1 + 35, y1 + 25
    text = 'YOUR CELL'
    color = color.GRAY
    text_surf = None
class population:
    x, y = (radius.x, radius.y + 35)
    text = 'POPULATION: 0'
    color = color.GRAY
    text_surf = None


manager = pygame_gui.UIManager((gm.screen_width, gm.screen_height), "UI/layout.json")

info_panel_button = pygame_gui.elements.UIButton(relative_rect=pg.Rect((-20, -20), (gm.ui_panel_width, gm.screen_height*1.2)),
                                                 text='', object_id=f"#info_panel",
                                                 manager=manager)
#your_cell_text = pygame_gui.elements.UIButton(relative_rect=pg.Rect((your_cell.x1, your_cell.y1), (your_cell.x2, your_cell.y2)),
#                                                 text ='', object_id=f"#label", 
#                                                 parent_element = info_panel_button,
#                                                 manager=manager)
cell_icon_button = pygame_gui.elements.UIButton(relative_rect=pg.Rect((cell_icon.x, cell_icon.y), (cell_icon.x + cell_icon.w, cell_icon.y + cell_icon.h)),
                                                 text='', object_id=f"#cell_icon",
                                                 parent_element = info_panel_button,
                                                 manager=manager)
mutate_button = pygame_gui.elements.UIButton(relative_rect=pg.Rect((mutate.x, mutate.y), (mutate.x + mutate.w, mutate.y + mutate.h)),
                                                 text='', object_id=f"#mutate",
                                                 parent_element = info_panel_button,
                                                 manager=manager)
split_button = pygame_gui.elements.UIButton(relative_rect=pg.Rect((split.x, split.y), (split.x + split.w, split.y + split.h)),
                                                 text='', object_id=f"#mutate",
                                                 parent_element = info_panel_button,
                                                 manager=manager)

#radius_text = pygame_gui.elements.UIButton(relative_rect=pg.Rect((radius.x, radius.y), (radius.x2, radius.y2)),
#                                                 text='', object_id=f"#label2",
#                                                 parent_element = info_panel_button,
#                                                 manager=manager)
pg.font.init()
pg.font.Font('UI/Pixeboy-z8XGD.ttf', 80)
bitfont = {80: pg.font.Font('UI/Pixeboy-z8XGD.ttf', 80), 60: pg.font.Font('UI/Pixeboy-z8XGD.ttf', 60),
           40: pg.font.Font('UI/Pixeboy-z8XGD.ttf', 40)}

text_elements = []
def generate_text():
    generate_sign(your_cell, size = 80)    
    generate_sign(radius, size = 40)    
    generate_sign(population, size = 40)

def generate_sign(obj, size = 40):
    obj.text_surf = bitfont[size].render(obj.text, False, obj.color)
    text_elements.append(obj)

generate_text()
def draw_text(screen):
    for text in text_elements:
        if(text.text_surf is not None): screen.blit(text.text_surf, (text.x, text.y))
    
#pygame_gui can't work with it!
def set_text():
    your_cell_text.set_text('YOUR CELL')
    mutate_button.set_text('MUTATE')
    split_button.set_text('SPLIT')
    radius_text.set_text('REACH FOOD')

if __name__ == "__main__":
    exec(open("main.py").read())