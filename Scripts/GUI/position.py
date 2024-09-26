import glm
import copy


class Position:
    class PositionInSpace:

        class Copy:
            def __init__(self, pos_in_space):
                self._pos_in_space = pos_in_space

            @property
            def left_bottom(self):
                return copy.copy(self._pos_in_space.left_bottom)

            @property
            def right_top(self):
                return copy.copy(self._pos_in_space.right_top)

            @property
            def size(self):
                return copy.copy(self._pos_in_space.size)

            @property
            def center(self):
                return copy.copy(self._pos_in_space.center)

        def __init__(self, left_bottom, right_top):
            self._left_bottom = left_bottom
            self._right_top = right_top
            self._size = self._right_top - self._left_bottom
            self._center = self._left_bottom + self.size / 2
            self._copy = Position.PositionInSpace.Copy(self)

        @property
        def copy(self):
            return self._copy

        @property
        def left_bottom(self):
            return self._left_bottom

        @left_bottom.setter
        def left_bottom(self, value):
            self._left_bottom = value
            self._size = self._right_top - self._left_bottom
            self._center = self._left_bottom + self.size / 2

        @property
        def right_top(self):
            return self._right_top

        @right_top.setter
        def right_top(self, value):
            self._right_top = value
            self._size = self._right_top - self._left_bottom
            self._center = self._left_bottom + self.size / 2

        @property
        def size(self):
            return self._size

        @size.setter
        def size(self, value):
            self._size = value
            self.right_top = self.left_bottom + value

        @property
        def center(self):
            return self._center

        @center.setter
        def center(self, value):
            self._center = value
            self._left_bottom = value - self.size / 2
            self._right_top = value + self.size / 2

        def transform(self, vec: glm.vec2):
            self._left_bottom += vec
            self.right_top += vec

        def __str__(self):
            return (f'LB=({(self._left_bottom.x, self._left_bottom.y)}, RT=({(self._right_top.x, self._right_top.y)}), '
                    f'Size=({(self.size.x, self.size.y)}), Center=({(self.center.x, self.center.y)})')

        def __repr__(self):
            return str(self)

    def __init__(self,
                 win_size,
                 rely_element_position=None,
                 rw_lb=glm.vec2(),
                 rw_rt=glm.vec2(),
                 r_lb=glm.vec2(),
                 r_rt=glm.vec2(),
                 a_lb=glm.vec2(),
                 a_rt=glm.vec2()
                 ):
        self.rely_element_position = rely_element_position

        self.relative_window = Position.PositionInSpace(rw_lb, rw_rt)
        self.relative = Position.PositionInSpace(r_lb, r_rt)
        self.absolute = Position.PositionInSpace(a_lb, a_rt)

        self._win_size = win_size

        self.m_gui = glm.mat4()

    @property
    def win_size(self):
        return self._win_size

    def evaluate_values_by_relative(self):
        rely_pos = self.rely_element_position  # type: Position
        if rely_pos is None:
            rely_pos = self
        # Abs
        self.absolute._left_bottom = (
                rely_pos.absolute.left_bottom + rely_pos.absolute.size * self.relative.left_bottom)
        self.absolute.right_top = (
                rely_pos.absolute.left_bottom + rely_pos.absolute.size * self.relative.right_top)

        # Relative Window
        self.relative_window._left_bottom = self.absolute.left_bottom / self.win_size
        self.relative_window.right_top = self.absolute.right_top / self.win_size

        self.m_gui = self.get_m_gui()

    def evaluate_values_by_relative_window(self):
        # Abs
        self.absolute._left_bottom = self.win_size * self.relative_window.left_bottom
        self.absolute.right_top = self.win_size * self.relative_window.right_top

        # Relative
        rely_pos = self.rely_element_position
        if rely_pos:
            self.relative._left_bottom = (
                                                     self.absolute.left_bottom - rely_pos.absolute.left_bottom) / rely_pos.absolute.size
            self.relative.right_top = (self.absolute.right_top - rely_pos.absolute.left_bottom) / rely_pos.absolute.size

        self.m_gui = self.get_m_gui()

    def evaluate_values_by_absolute(self):
        # Relative
        rely_pos = self.rely_element_position  # type: Position
        if rely_pos:
            self.relative._left_bottom = (
                    (self.absolute.left_bottom - rely_pos.absolute.left_bottom) / rely_pos.absolute.size
            )
            self.relative.right_top = (
                    (self.absolute.right_top - rely_pos.absolute.left_bottom) / rely_pos.absolute.size
            )
        # Relative Window
        self.relative_window._left_bottom = self.absolute.left_bottom / self.win_size
        self.relative_window.right_top = self.absolute.right_top / self.win_size

        self.m_gui = self.get_m_gui()

    def recalculate(self, win_size):
        self._win_size = win_size
        if self.rely_element_position:
            self.absolute._left_bottom = (
                    self.rely_element_position.absolute.left_bottom +
                    self.rely_element_position.absolute.size * self.relative.left_bottom
            )
            self.absolute.right_top = (
                    self.rely_element_position.absolute.left_bottom +
                    self.rely_element_position.absolute.size * self.relative.right_top
            )
        else:
            self.absolute.right_top = win_size

    def get_m_gui(self):
        vec4 = glm.vec4
        size = self.absolute.size
        abs_left_bottom = self.absolute.left_bottom
        rely_element_position = self.rely_element_position
        if rely_element_position is None:
            rely_element_position = self
            rely_element_m_gui = glm.mat4()
        else:
            rely_element_m_gui = rely_element_position.m_gui
        rely_element_abs_left_bottom = rely_element_position.absolute.left_bottom

        win_size = self.win_size

        c0 = vec4(size.x / win_size.x,
                  0,
                  0,
                  0)

        c1 = vec4(0,
                  size.y / win_size.y,
                  0,
                  0)

        c2 = vec4(0,
                  0,
                  0,
                  0)

        c3 = vec4((abs_left_bottom.x - rely_element_abs_left_bottom.x) / win_size.x + rely_element_m_gui[3][0],
                  (abs_left_bottom.y - rely_element_abs_left_bottom.y) / win_size.y + rely_element_m_gui[3][1],
                  0,
                  1)

        m_gui = glm.mat4x4(c0, c1, c2, c3)
        return m_gui

    def check_if_clicked(self, mouse_pos):
        return (self.absolute.left_bottom.x <= mouse_pos.x <= self.absolute.right_top.x and
                self.absolute.left_bottom.y <= mouse_pos.y <= self.absolute.right_top.y)

    def __str__(self):
        return (f'Position abs:LB={(self.absolute.left_bottom.x, self.absolute.left_bottom.y)},'
                f' RT={(self.absolute.right_top.x, self.absolute.right_top.y)}')

    def __repr__(self):
        return str(self)
