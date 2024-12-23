# import Scripts.Source.GUI.Elements.element as element_m
# import Scripts.Source.GUI.library as library_m
# import glm
#
# # Settings
# DEV_MODE = True
#
# Pivot = element_m.Pivot
# import Scripts.Source.GUI.Elements.elements as elements
#
#
# class GameGUI:
#
#     def __init__(self, game, win_size, gui):
#         self.game = game
#         self.win_size = glm.vec2(win_size)
#         self.aspect_ratio = win_size[0] / win_size[1]
#
#         self.gui = gui
#
#         self.debug_window = elements.Window(f"debug_window_{len(self.gui.windows)}", gui.canvas,
#                                             gui.win_size,
#                                             gui, "DEBUG_GLOBAL")
#
#         self.debug_window.position.relative_window.size = glm.vec2(0.2, 0.1) / 1.25
#         self.debug_window.position.relative_window.center = glm.vec2(0.1, 0.9)
#         self.debug_window.position.evaluate_values_by_relative_window()
#         self.debug_window.init()
#         self.debug_window.update_position()
#         self.debug_global_text = elements.Text(f"DEBUG", self.debug_window.inner_data_block, self.win_size,
#                                                f"(0,0,1)",
#                                                font_size=1)
#         self.debug_global_text.color = glm.vec4(0.1, 0.1, 0.1, 1)
#         self.debug_global_text.pivot = Pivot.Center
#         self.debug_global_text.position.relative.center = glm.vec2(0.3, 0.5)
#         self.debug_global_text.update_position()
#
#         self.debug_window.update_position()
#         self.gui.windows.append(self.debug_window)
#
#         window = elements.Window(f"debug_window_{len(self.gui.windows)}", gui.canvas,
#                                  gui.win_size,
#                                  gui, "DEBUG_LOCAL")
#
#         window.position.relative_window.size = glm.vec2(0.2, 0.1) / 1.25
#         window.position.relative_window.center = glm.vec2(0.1, 0.8)
#         window.position.evaluate_values_by_relative_window()
#         window.init()
#         window.update_position()
#         self.debug_LOCAL_text = elements.Text(f"DEBUG", window.inner_data_block, self.win_size,
#                                               f"(0,0,1)",
#                                               font_size=1)
#         self.debug_LOCAL_text.color = glm.vec4(0.1, 0.1, 0.1, 1)
#         self.debug_LOCAL_text.pivot = Pivot.Center
#         self.debug_LOCAL_text.position.relative.center = glm.vec2(0.3, 0.5)
#         self.debug_LOCAL_text.update_position()
#
#         window.update_position()
#         self.gui.windows.append(window)
#
#         self.fps_text = elements.Text("Header Text", gui.canvas, self.win_size,
#                                       "FPS: ",
#                                       font_size=1,
#                                       space_between=0.1,
#                                       pivot=element_m.Pivot.LeftBottom
#                                       )
#         self.fps_text.position.relative.left_bottom = glm.vec2(0)
#         self.fps_text.update_position()
#
#         self.crosshair_texture = elements.Texture("Crosshair", gui.canvas, gui.win_size,
#                                                   library_m.textures["crosshair"], False)
#         self.crosshair_texture.pivot = Pivot.Center
#         self.crosshair_size = 0.025
#         self.crosshair_texture.position.relative.left_bottom = glm.vec2(0.5 - self.crosshair_size / 2,
#                                                                         0.5 - self.aspect_ratio * self.crosshair_size / 2)
#
#         self.crosshair_texture.position.relative.size = glm.vec2(self.crosshair_size,
#                                                                  self.aspect_ratio * self.crosshair_size)
#
#         self.crosshair_texture.update_position()
#
#     @property
#     def windows(self):
#         return self.gui.windows
#
#     def process_window_resize(self, new_size):
#         self.win_size = new_size
#
#     def delete(self):
#         self.game = None
#         if self.gui:
#             self.gui.clear()
#             self.gui = None
#
