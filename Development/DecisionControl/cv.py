#import necessary packages
import numpy as np
import argparse
import time
import cv2

class CV:

    def __init__(self):
		print('init!')

		self.hue = 0
		self.huehigh = 255
		self.saturation = 0
		self.saturationhigh = 255
		self.value = 0
		self.valuehigh = 255

		self.camera = cv2.VideoCapture(0);
		self.saved_image_dir = "/home/pi/cv/images/"
		self.image = None

		#define the list of color boundaries
		self.boundaries = [
			([0, 0, 0], [42, 34, 32]), #black
			([59, 219, 48], [82, 255, 255]), #green
			([0, 151, 171], [10, 255, 255]), #orange
			([0, 75, 77], [0, 138, 139]) #yellow (block)
		]

		## debug green
		#self.hue = self.boundaries[1][0][0]
		#self.huehigh = self.boundaries[1][1][0]
		#self.saturation = self.boundaries[1][0][1]
		#self.saturationhigh = self.boundaries[1][1][1]
		#self.value = self.boundaries[1][0][2]
		#self.valuehigh = self.boundaries[1][1][2]

		## debug orange
		self.hue = self.boundaries[2][0][0]
		self.huehigh = self.boundaries[2][1][0]
		self.saturation = self.boundaries[2][0][1]
		self.saturationhigh = self.boundaries[2][1][1]
		self.value = self.boundaries[2][0][2]
		self.valuehigh = self.boundaries[2][1][2]

	def get_all_objects(self):
		green_objects = self.get_green_objects()
		orange_objects = self.get_orange_objects()

		return green_objects + orange_objects

	def get_orange_objects(self):
		return self.get_objects(self.boundaries[2][0], self.boundaries[2][1], 'orange')


	def get_green_objects(self):
		return self.get_objects(self.boundaries[1][0], self.boundaries[1][1], 'green')

	def get_objects(self, lower, upper, color):

		lower = np.array(lower, dtype="uint8")
		upper = np.array(upper, dtype="uint8")

		self.load_image()

		# convert to HSV
		hsv_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)

		#find the colors within the specified boundaries and apply
		#the mask
		mask = cv2.inRange(hsv_image, lower, upper)
		hsv_output = cv2.bitwise_and(hsv_image, hsv_image, mask = mask)

		gray_output = cv2.cvtColor(hsv_output, cv2.COLOR_BGR2GRAY)

		ret, thresh = cv2.threshold(gray_output, 127, 255, 0)

		contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

		objects = []
		for cnt in contours:
			M = cv2.moments(cnt)
			area = cv2.contourArea(cnt)
			if area > 60:
				(x,y), radius = cv2.minEnclosingCircle(cnt)
				center = (int(x), int(y))

				distance = 1 / (radius / 37)


				centroid = (int(M['m10']/M['m00']), int(M['m01']/M['m00']))

				objects.append([color, distance, centroid])

		return objects

	def take_picture(self):

		# Take the image from the camera
		retval, im = self.camera.read()

		image_path = self.saved_image_dir + str(time.time()) + ".png"
		cv2.imwrite(image_path, im)
		return im

	def load_image(self):

		#load the image
		#if self.image is None:
		self.image = self.take_picture()

		if self.image is None:
			print "Image not found..."
			print "Is the camera plugged in and available?"
			exit()

	def show_output(self):

		self.load_image()

		# convert to HSV
		hsv_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)

		#create NumPy arrays from the boundaries
		lower = [self.hue, self.saturation, self.value]
		upper = [self.huehigh, self.saturationhigh, self.valuehigh]

		lower = np.array(lower, dtype="uint8")
		upper = np.array(upper, dtype="uint8")

		#find the colors within the specified boundaries and apply
		#the mask
		mask = cv2.inRange(hsv_image, lower, upper)
		hsv_output = cv2.bitwise_and(hsv_image, hsv_image, mask = mask)

		#cv2.imshow("BotBall", hsv_output)
		cv2.imshow("BotBall", self.image)


	def hue_callback(self, position):
		self.hue = position
		self.show_output()

	def huehigh_callback(self, position):
		self.huehigh = position
		self.show_output()

	def saturation_callback(self, position):
		self.saturation = position
		self.show_output()

	def saturationhigh_callback(self, position):
		self.saturationhigh = position
		self.show_output()

	def value_callback(self, position):
		self.value = position
		self.show_output()

	def valuehigh_callback(self, position):
		self.valuehigh = position
		self.show_output()

	def canny_callback(self, position):
		self.canny = position
		self.show_output()

	def cannyhigh_callback(self, position):
		self.cannyhigh = position
		self.show_output()

	def debug(self):
		#create window
		cv2.namedWindow("BotBall")



		#construct the argument parser and parse arguments
		ap = argparse.ArgumentParser()
		ap.add_argument("-i", "--image", help="path to the image")
		args = vars(ap.parse_args())

		#print image
		cv2.createTrackbar("Hue", "BotBall", 0, 179, self.hue_callback)
		cv2.createTrackbar("HueHigh", "BotBall", 170, 179, self.huehigh_callback)
		cv2.createTrackbar("Saturation", "BotBall", 0, 255, self.saturation_callback)
		cv2.createTrackbar("SaturationHigh", "BotBall", 255, 255, self.saturationhigh_callback)
		cv2.createTrackbar("Value", "BotBall", 0, 255, self.value_callback)
		cv2.createTrackbar("ValueHigh", "BotBall", 255, 255, self.valuehigh_callback)

		self.show_output()
		cv2.waitKey(0)


		# You'll want to release the camera, otherwise you won't be able to create a new
		# capture object until your script exits
		del(self.camera)

#cv = CV()
#objects = cv.get_all_objects()
#for object in objects:
#	print object
#cv.debug()
