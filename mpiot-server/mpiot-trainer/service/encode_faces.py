from imutils import paths
from time import sleep
import face_recognition
import argparse
import pickle
import redis
import cv2
import os

def train():
	print("[INFO] quantifying faces...")
	imagePaths = list(paths.list_images(args["dataset"]))

	knownEncodings = []
	knownNames = []

	for (i, imagePath) in enumerate(imagePaths):
		# extract the person name from the image path
		print("[INFO] processing image {}/{}".format(i + 1, len(imagePaths)))
		name = imagePath.split(os.path.sep)[-2]

		image = cv2.imread(imagePath)
		rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

		# extract bounding boxes corresponding to each face in the input image
		boxes = face_recognition.face_locations(rgb,
			model=args["detection_method"])

		# compute the facial vector for the face
		encodings = face_recognition.face_encodings(rgb, boxes)

		# loop over the encodings
		for encoding in encodings:
			# add each encoding + name to our set of known names and
			# encodings
			knownEncodings.append(encoding)
			knownNames.append(name)
	# dump the facial encodings + names to disk
	print("[INFO] serializing encodings...")
	data = {"encodings": knownEncodings, "names": knownNames}
	f = open(args["encodings"], "wb")
	f.write(pickle.dumps(data))
	f.close()
	print("[INFO] Done")


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--dataset", required=True,
	help="path to input directory of faces + images")
ap.add_argument("-e", "--encodings", required=True,
	help="path to serialized db of facial encodings")
ap.add_argument("-d", "--detection-method", type=str, default="cnn",
	help="face detection model to use: either `hog` or `cnn`")
args = vars(ap.parse_args())
redisHost = os.environ['MESSENGER_HOST']
redisPort = os.environ['MESSENGER_PORT']
print(" connecting to " + redisHost +":"+str(redisPort))
messenger = redis.StrictRedis(host=redisHost, port=redisPort)
pubsub = messenger.pubsub()
pubsub.subscribe("Uploads")

while True:
	noMessages = True
	while noMessages:
		for message in pubsub.listen():
			newMessage = message["data"]
			print("[INFO] Message Received: " + str(newMessage))
			if (str(newMessage) == "b'ReceivedNewData'"):
				noMessages = False
				newMessage = "";
				break
	print("[INFO] Training on newly received Data...")
	train()