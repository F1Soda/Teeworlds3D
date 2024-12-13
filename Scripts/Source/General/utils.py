import struct

import glm
import numpy as np
import pygame as pg


class IndexableProperty:
    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        if doc is None and fget is not None:
            doc = fget.__doc__
        self.__doc__ = doc

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if self.fget is None:
            raise AttributeError("unreadable attribute")
        return self.fget(obj)

    def __set__(self, obj, value):
        if self.fset is None:
            raise AttributeError("can't set attribute")
        self.fset(obj, value)

    def __delete__(self, obj):
        if self.fdel is None:
            raise AttributeError("can't delete attribute")
        self.fdel(obj)

    def getter(self, fget):
        return type(self)(fget, self.fset, self.fdel, self.__doc__)

    def setter(self, fset):
        return type(self)(self.fget, fset, self.fdel, self.__doc__)

    def deleter(self, fdel):
        return type(self)(self.fget, self.fset, fdel, self.__doc__)

    def __getitem__(self, key):
        if hasattr(self.fget, '__getitem__'):
            return self.fget(self.obj)[key]
        raise TypeError("'{}' object is not subscriptable".format(type(self.fget).__name__))

    def __setitem__(self, key, value):
        if hasattr(self.fset, '__setitem__'):
            self.fset(self.obj, key, value)
        else:
            raise TypeError("'{}' object does not support item assignment".format(type(self.fset).__name__))

    def __delitem__(self, key):
        if hasattr(self.fdel, '__delitem__'):
            self.fdel(self.obj, key)
        else:
            raise TypeError("'{}' object does not support item deletion".format(type(self.fdel).__name__))


def bytes_to_normalized_tuple(byte_data):
    '''
    convert from hex to normalized color system(0.0 — 1.0)
    :param byte_data: hex color
    :return: normalized color tuple
    '''
    # Unpack the byte data into integers
    int_values = struct.unpack('BBB', byte_data)
    # Normalize the values to the range [0, 1]
    normalized_values = tuple(value / 255.0 for value in int_values)
    return normalized_values


def get_data_elements_by_indices(vertices, indices) -> np.ndarray:
    '''
    :param vertices: list data for all vertices
    :param indices: list index tuple with sequence vertices data
    :return: one-dimension sequence vertex data based on indices
    '''
    data = [vertices[ind] for triangle in indices for ind in triangle]
    return np.array(data, dtype='f4')


def calculate_width_letters(path):
    '''
    Calculate width of letters in text-tail texture 512 by 512.
    :param path: path to image
    :return: one dimensional list with relative (0.0—1.0) width letter
    '''
    # Load the image
    img = pg.image.load(path)
    width, height = img.get_size()

    num_letters_per_row = 16  # Adjust this based on your texture layout
    num_letters_per_col = 16  # Adjust this based on your texture layout

    letter_width = width // num_letters_per_row
    letter_height = height // num_letters_per_col

    letter_widths = []

    for row in range(num_letters_per_col):
        for col in range(num_letters_per_row):
            max_right_white_pixel = 0
            for y in range(row * letter_height, (row + 1) * letter_height):
                for x in range(col * letter_width, (col + 1) * letter_width):
                    r, g, b, a = img.get_at((x, y))
                    if a != 0:  # White pixel
                        max_right_white_pixel = max(max_right_white_pixel, x)

            # Calculate the real width of the letter
            real_width = max(0, (max_right_white_pixel - col * letter_width)) / letter_width
            letter_widths.append(real_width)

    letter_widths[16 * 2 + 0] = 0.5

    return letter_widths


def rainbow_color(t, out_color):
    """
    Returns an RGB color representing a rainbow shimmering effect based on the time in seconds.

    Parameters:
    t (float): Time in seconds.

    Returns:
    tuple: RGB color as a tuple of three floats in the range [0, 1].
    """
    # Normalize time to a value between 0 and 1
    hue = (t % 6) / 6

    # Convert hue to RGB
    out_color.r = max(0, min(1, abs(hue * 6 - 3) - 1))
    out_color.g = max(0, min(1, 2 - abs(hue * 6 - 2)))
    out_color.b = max(0, min(1, 2 - abs(hue * 6 - 4)))


def get_non_parallel_vector(vec, delta=1e-7):
    res = glm.vec3(-vec.y, vec.x, 0)
    if glm.length(res) != 0 and abs(glm.dot(res, vec)) < delta:
        return res
    res = glm.vec3(-vec.z, 0, -vec.x)
    if glm.length(res) != 0 and abs(glm.dot(res, vec)) < delta:
        return res
    res = glm.vec3(0, -vec.z, -vec.y)
    if glm.length(res) != 0 and abs(glm.dot(res, vec)) < delta:
        return res
    return None


class PriorityEventDelegate:
    def __init__(self):
        self.__event_followers = []

    def __iadd__(self, ehandler):
        self.__event_followers.append(ehandler)
        return self

    def __isub__(self, ehandler):
        if ehandler in self.__event_followers:
            self.__event_followers.remove(ehandler)
        return self

    def __call__(self, *args, **kwargs):
        for follower in self.__event_followers:
            if follower(*args, **kwargs):
                return

    def delete(self):
        self.__event_followers.clear()

    def __str__(self):
        return f"Event Delegate. {len(self.__event_followers)} followers"

    def __repr__(self):
        return str(self)


class EventDelegate:
    def __init__(self):
        self.__event_followers = []

    def __iadd__(self, ehandler):
        self.__event_followers.append(ehandler)
        return self

    def __isub__(self, ehandler):
        self.__event_followers.remove(ehandler)
        return self

    def __call__(self, *args, **kwargs):
        for follower in self.__event_followers:
            follower(*args, **kwargs)

    def delete(self):
        self.__event_followers.clear()

    def __str__(self):
        return f"Event Delegate. {len(self.__event_followers)} followers"

    def __repr__(self):
        return str(self)


def rotation_matrix_to_euler_angles(R):
    '''
    Хз че та не очень работает, хотя вроде все правильно сделал
    :param R:
    :return:
    '''
    delta = 1e-9
    if abs(R[0][2] - 1) > delta and abs(R[0][2] + 1) > delta:
        q_1 = glm.asin(R[0][2])
        q_2 = glm.pi() - q_1
        p_1 = np.atan2(R[1][2] / glm.cos(q_1), R[2][2] / glm.cos(q_1))
        p_2 = np.atan2(R[1][2] / glm.cos(q_2), R[2][2] / glm.cos(q_2))
        r_1 = np.atan2(R[0][1] / glm.cos(q_1), R[0][0] / glm.cos(q_1))
        r_2 = np.atan2(R[0][1] / glm.cos(q_2), R[0][0] / glm.cos(q_2))
    else:
        r_1 = r_2 = 0
        if abs(R[0][2] + 1) < delta:
            q_1 = q_2 = glm.pi() / 2
            p_1 = p_2 = r_1 + np.atan2(R[1][0], R[2][0])
        else:
            q_1 = q_2 = -glm.pi() / 2
            p_1 = p_2 = -r_1 + np.atan2(-R[1][0], -R[2][0])
    return p_1, q_1, r_1


def copy_vec(from_vec, to_vec):
    for i in range(len(from_vec)):
        to_vec[i] = from_vec[i]


def copy_mat(from_mat, to_mat):
    for i in range(len(from_mat)):
        for j in range(len(from_mat[i])):
            to_mat[i][j] = from_mat[i][j]


def reset_mat(mat):
    for i in range(len(mat)):
        for j in range(len(mat[i])):
            if i == j:
                mat[i][j] = 1
            else:
                mat[i][j] = 0

