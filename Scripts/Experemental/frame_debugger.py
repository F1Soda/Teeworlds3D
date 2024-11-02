import Scripts.Source.GUI.Elements.elements as elements
import glm


class FrameDebugger:
    gui = None
    drawing_textures = []

    @staticmethod
    def init(gui):
        FrameDebugger.gui = gui

    @staticmethod
    def draw_texture(texture, center_pos, is_depth_texture=False):
        gui = FrameDebugger.gui
        window = elements.Window(f"Debug texture window", gui.gui,
                                 gui.win_size,
                                 gui, "DEBUG TEXTURE")
        window.position.relative_window.size = glm.vec2(0.3)
        window.position.relative_window.center = center_pos
        window.position.evaluate_values_by_relative_window()
        window.init()

        texture_block = elements.Texture("Debug Texture", window.inner_data_block, gui.win_size, texture, is_depth_texture)
        #texture_block = elements.Block("ASAS", window.inner_data_block, gui.win_size, color=(1, 0, 0, 1))
        texture_block.position.relative.right_top = glm.vec2(1)

        window.update_position()

        gui.windows.append(window)
