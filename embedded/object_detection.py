# import the necessary packages
from torchvision.models import detection
import numpy as np
import pickle
import torch
import cv2


# set the device we will be using to run the model
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# load the list of categories in the COCO dataset and then generate a
# set of bounding box colors for each class
CLASSES = pickle.loads(open("coco_classes.pickle", "rb").read())
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

# initialize a dictionary containing model name and its corresponding 
# torchvision function call
MODELS = {
	"frcnn-resnet": detection.fasterrcnn_resnet50_fpn,
	"frcnn-mobilenet": detection.fasterrcnn_mobilenet_v3_large_320_fpn,
	"retinanet": detection.retinanet_resnet50_fpn
}

# load the model and set it to evaluation mode
model = MODELS["frcnn-resnet"](pretrained=True, progress=True,
	num_classes=len(CLASSES), pretrained_backbone=True).to(DEVICE)
model.eval()

# load the image from disk
def detect(image):
	# image = cv2.imread(photo)
	# orig = image.copy()

	# convert the image from BGR to RGB channel ordering and change the
	# image from channels last to channels first ordering
	image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
	image = image.transpose((2, 0, 1))

	# add the batch dimension, scale the raw pixel intensities to the
	# range [0, 1], and convert the image to a floating point tensor
	image = np.expand_dims(image, axis=0)
	image = image / 255.0
	image = torch.FloatTensor(image)

	# send the input to the device and pass the it through the network to
	# get the detections and predictions
	image = image.to(DEVICE)
	detections = model(image)[0]

	# loop over the detections
 
	labs = []
	for i in range(0, len(detections["boxes"])):
		# extract the confidence (i.e., probability) associated with the
		# prediction
		confidence = detections["scores"][i]
	
		# filter out weak detections by ensuring the confidence is
		# greater than the minimum confidence
		if confidence > 0.5:
			# extract the index of the class label from the detections,
			idx = int(detections["labels"][i])
			
			labs.append(CLASSES[idx])
	
	return labs