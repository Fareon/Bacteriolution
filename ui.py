import pygame as pg
import pygame_gui
import game_manager as gm

#ui variables storage
class cell_icon:
    w, h = 120, 90
    x, y = gm.ui_panel_width*0.21, gm.screen_height*0.175
   
step = 40
class mutate:
    w, h = +cell_icon.w, -step*6
    x, y = cell_icon.x, cell_icon.y + 200
    
class split:
    w, h = +cell_icon.w, -step*7.5
    x, y = cell_icon.x, mutate.y + step + 25
    


manager = pygame_gui.UIManager((gm.screen_width, gm.screen_height), "UI/layout.json")

info_panel_button = pygame_gui.elements.UIButton(relative_rect=pg.Rect((-20, -20), (gm.ui_panel_width, gm.screen_height*1.2)),
                                                 text='', object_id=f"#info_panel",
                                                 manager=manager)
your_cell_text = pygame_gui.elements.UIButton(relative_rect=pg.Rect((10, -10), (gm.ui_panel_width*0.9, gm.screen_height*0.2)),
                                                 text ='', object_id=f"#label", 
                                                 parent_element = info_panel_button,
                                                 manager=manager)
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

radius_text = pygame_gui.elements.UIButton(relative_rect=pg.Rect((split.x, split.y + 50), (split.x + split.w, split.y + split.h)),
                                                 text='', object_id=f"#label2",
                                                 parent_element = info_panel_button,
                                                 manager=manager)


def set_text():
    your_cell_text.set_text('YOUR CELL')
    mutate_button.set_text('MUTATE')
    split_button.set_text('SPLIT')

if __name__ == "__main__":
    exec(open("main.py").read())