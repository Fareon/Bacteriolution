import pygame as pg
import pygame_gui
import game_manager as gm

#ui variables storage

info_panel_button = object
manager = object

manager = pygame_gui.UIManager((gm.screen_width, gm.screen_height), "UI/layout.json")

info_panel_button = pygame_gui.elements.UIButton(relative_rect=pg.Rect((0, -10), (gm.ui_panel_width, gm.screen_height*1.2)),
                                                 text='', object_id=f"#info_panel",
                                                 manager=manager)
info_panel_button2 = pygame_gui.elements.UIButton(relative_rect=pg.Rect((0, -10), (gm.ui_panel_width, gm.screen_height*1.2)),
                                                 text='', object_id=f"#info_panel",
                                                 manager=manager)