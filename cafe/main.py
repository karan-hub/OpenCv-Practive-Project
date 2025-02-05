import os
import cv2
from cvzone.HandTrackingModule import HandDetector

# Initialize webcam
cap = cv2.VideoCapture(1)
cap.set(3, 640)
cap.set(4, 480)

# Load background image
imgBackground = cv2.imread("Resources/Background.png")

# Load mode images
folderPathModes = "Resources/Modes"
listImgModesPath = os.listdir(folderPathModes)
listImgModes = [cv2.imread(os.path.join(folderPathModes, img)) for img in listImgModesPath]

# Load icon images
folderPathIcons = "Resources/Icons"
listImgIconsPath = os.listdir(folderPathIcons)
listImgIcons = [cv2.imread(os.path.join(folderPathIcons, img)) for img in listImgIconsPath]

# Hand detector
detector = HandDetector(detectionCon=0.8, maxHands=1)

# Variables
modeType = 0  # Selection mode index
selection = -1
counter = 0
selectionSpeed = 7
modePositions = [(1136, 196), (1000, 384), (1136, 581)]
counterPause = 0
selectionList = [-1, -1, -1]

while True:
    success, img = cap.read()
    if not success:
        continue
    
    # Find hand landmarks
    hands, img = detector.findHands(img)
    
    # Overlay webcam feed on the background image
    imgBackground[139:139 + 480, 50:50 + 640] = img
    imgBackground[0:720, 847:1280] = listImgModes[modeType]
    
    if hands and counterPause == 0 and modeType < 3:
        hand1 = hands[0]
        fingers1 = detector.fingersUp(hand1)
        
        # Selection logic
        if fingers1 == [0, 1, 0, 0, 0]:
            selection = 1
        elif fingers1 == [0, 1, 1, 0, 0]:
            selection = 2
        elif fingers1 == [0, 1, 1, 1, 0]:
            selection = 3
        else:
            selection = -1
            counter = 0
        
        if selection != -1:
            counter += 1
            cv2.ellipse(imgBackground, modePositions[selection - 1], (103, 103), 0, 0,
                        counter * selectionSpeed, (0, 255, 0), 20)
            if counter * selectionSpeed > 360:
                selectionList[modeType] = selection
                modeType += 1
                counter = 0
                selection = -1
                counterPause = 1
    
    # Pause counter to prevent instant mode switch
    if counterPause > 0:
        counterPause += 1
        if counterPause > 60:
            counterPause = 0
    
    # Display selected icons at the bottom
    if selectionList[0] != -1:
        imgBackground[636:701, 133:198] = listImgIcons[selectionList[0] - 1]
    if selectionList[1] != -1 and (2 + selectionList[1]) < len(listImgIcons):
        imgBackground[636:701, 340:405] = listImgIcons[2 + selectionList[1]]
    if selectionList[2] != -1 and (5 + selectionList[2]) < len(listImgIcons):
        imgBackground[636:701, 542:607] = listImgIcons[5 + selectionList[2]]
    
    # Display the result
    cv2.imshow("Background", imgBackground)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
