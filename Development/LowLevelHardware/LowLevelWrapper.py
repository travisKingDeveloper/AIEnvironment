__author__ = 'travi_000'

print("Low Level Wrapper")


class LowLevel(object):
    def __init__(self):
        self.Localization = Localization()
        self.WheelManagement = WheelManagement()


class Localization(object):
    def __init__(self):
        # constructor object
        self.placeholder = False


class WheelManagement(object):
    def __init__(self):
        # constructor object
        self.placeholder = False


class ArmManagement(object):
    def __init__(self):
        # constructor object for the control of the arm
        self.placeholder = False