__author__ = 'travi_000'

# Node class to help build a tree


class Node:
    def __init__(self, value):
        self.element = value
        self.nextEl = None

    def get_el(self):
        return self.element

    def get_next(self):
        return self.nextEl

