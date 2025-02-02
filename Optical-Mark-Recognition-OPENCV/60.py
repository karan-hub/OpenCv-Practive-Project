boxes = utils.splitBoxes(imgThresh)

myPixelVal = np.zeros((questions, choices))

CountC = 0
CountR = 0

for image in boxes:
	totalPixels = cv2.countNonZero(image)
	myPixelVal[CountR] [CountR] = totalPixels
	CountC +=1
	if (CountC == choices): CountR +=1; CountC = 0
print(myPixelVal)
