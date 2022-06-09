import cv2
import mediapipe as mp
import time
import osascript


from pyfirmata2 import Arduino #import library from pyfirmata2 to detect Arduino

board = Arduino(Arduino.AUTODETECT) #detect Arduino with Autodetect

print("...Arduino detected") #print statement #1
print("...Blink test started") #print statement #2
#######################################################

cap = cv2.VideoCapture(0)

##########################################
wCam, hCam = 640, 480
#########################################

cap = cv2.VideoCapture(1)
cap.set(3, wCam)
cap.set(4, hCam)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0
board.digital[2].write(1)
board.digital[3].write(1)
while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                # print(id, lm.z)
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                print(id, cx, cy, lm.z)

                if id==4 and cy>400 and cx<200:
                    cv2.putText(img, ("light1 off"), (90, 190), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
                    board.digital[13].write(0)
                elif id==4 and cy>400 and cx>500:
                    cv2.putText(img, ("light1 on"), (90, 190), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
                    board.digital[13].write(1)
                elif id==4 and cy>400:
                    cv2.putText(img, ("light1"), (90, 190), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
                elif id==4 and cy>300 and cx<200:
                    cv2.putText(img, ("fan off"), (90, 190), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
                    board.digital[4].write(0)
                    board.digital[5].write(0)
                elif id==4 and cy>300 and cx>500:
                    cv2.putText(img, ("fan on"), (90, 190), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
                    board.digital[4].write(1)
                    board.digital[5].write(0)
                elif id==4 and cy>300:
                    cv2.putText(img, ("fan"), (90, 190), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
                elif id==4 and cy>200 and cx<200:
                    cv2.putText(img, ("light2 off"), (90, 190), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
                    board.digital[12].write(0)
                elif id==4 and cy>200 and cx>500:
                    cv2.putText(img, ("light2 on"), (90, 190), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
                    board.digital[12].write(1)
                elif id==4 and cy>200:
                    cv2.putText(img, ("light2"), (90, 190), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)  
                elif id==4 and cy>100:
                    cv2.putText(img, ("sound"), (90, 190), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
                    osascript.osascript("set volume output volume {}".format(cx*100/500))     
                elif id==4 and cy>0:
                    cv2.putText(img, ("all off"), (90, 190), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
                    board.digital[13].write(0)
                    board.digital[12].write(0)
                    board.digital[4].write(0)
                    board.digital[5].write(0)


                if id==4:
                    cv2.circle(img, (cx, cy), 15, (255,0,255), cv2.FILLED)
                #     osascript.osascript("set volume output volume {}".format(cx*100/1200))
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)
