import pygame as pg
import pygame_gui
import game_manager as gm

#ui variables storage

manager = pygame_gui.UIManager((gm.screen_width, gm.screen_height), "UI/layout.json")

info_panel_button = pygame_gui.elements.UIButton(relative_rect=pg.Rect((-20, -20), (gm.ui_panel_width, gm.screen_height*1.2)),
                                                 text='', object_id=f"#info_panel",
                                                 manager=manager)
your_cell_text = pygame_gui.elements.UILabel(relative_rect=pg.Rect((0, -10), (gm.ui_panel_width*0.9, gm.screen_height*0.2)),
                                                 text ='YOUR CELL', 
                                                 object_id=f"#label", 
                                                 parent_element = info_panel_button,
                                                 manager=manager)