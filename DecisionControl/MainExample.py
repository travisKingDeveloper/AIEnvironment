from HighLevelHardwareCode.ExampleHighLevel import *
from LowLevelHardwareCode.ExampleLowLevel import *
__author__ = 'travi_000'


print("Simulating Calling functions in different directory's")

function_low_level()
function_high_level()

lowLevel = LowLevel()

lowLevel.add_degree(20)

lowLevel.add_degree(300)

print("this is the degree " + str(lowLevel.wheelDegrees))

lowLevel.add_degree(300)

print("this is the degree " + str(lowLevel.wheelDegrees))

print("I am concluding the test")

print("I am Michael")
