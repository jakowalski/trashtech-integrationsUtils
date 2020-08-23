import cv2
import numpy as np
from PIL import Image
from collections import defaultdict
from collections import Counter



filePath = 'D:\\Projects\\TensorflowModelsRepo\\models-master\\research\\deeplab\\datasets\\ContainerSeg\\dataset\\SegmentationClassRaw\\'

image = cv2.imread(filePath + '0001_08_17_05_06.jpg', 1)

print(image.shape)

mask1 = np.zeros((image.shape[0], image.shape[1],), np.uint8)
mask1[:]=255
i1 = cv2.inRange(image, np.array(2), np.array(2))
mask1 = cv2.bitwise_or(mask1, mask1, mask =i1)
cv2.imshow('sa', mask1)
cv2.waitKey(0)
i1 = cv2.inRange(image,np.array([54,  53, 251]), np.array([54,  53, 251]))

mask1 = cv2.bitwise_or(mask1, mask1, mask =i1)

i1 = cv2.inRange(image,np.array([53,  51, 251]), np.array([53,  51, 251]))
mask1 = cv2.bitwise_or(mask1, mask1, mask =i1)

i1 = cv2.inRange(image,np.array([52,  49, 255]), np.array([52,  49, 255]))
mask1 = cv2.bitwise_or(mask1, mask1, mask =i1)

i1 = cv2.inRange(image,np.array([51,  49, 255]), np.array([51,  49, 255]))
mask1 = cv2.bitwise_or(mask1, mask1, mask =i1)

i1 = cv2.inRange(image,np.array([53,  51, 255]), np.array([53,  51, 255]))
mask1 = cv2.bitwise_or(mask1, mask1, mask =i1)

i1 = cv2.inRange(image,np.array([50,  49, 253]), np.array([50,  49, 253]))
mask1 = cv2.bitwise_or(mask1, mask1, mask =i1)

i1 = cv2.inRange(image,np.array([49,  48, 252]), np.array([49,  48, 252]))
mask1 = cv2.bitwise_or(mask1, mask1, mask =i1)

uniqueColors = np.unique(image, axis=1)
s = np.unique(uniqueColors, axis=1)
for f in uniqueColors:
    print(f)

