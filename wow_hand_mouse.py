import cv2
import mediapipe as mp
import time
import math
import pyautogui


cap=cv2.VideoCapture(0,cv2.CAP_DSHOW)
pyautogui.PAUSE = 0
mpHands=mp.solutions.hands
hands=mpHands.Hands(max_num_hands =1,min_tracking_confidence=0.9)
mpDraw=mp.solutions.drawing_utils

pTime=0
cTime=0
hand_down = 0
while True:
  
  success, img = cap.read()
  imgRGB = cv2.cvtColor(img , cv2.COLOR_BGR2RGB)
  results = hands.process(imgRGB)
  # print(results.multi_hand_landmarks)
  if results.multi_hand_landmarks:
    for handLms in results.multi_hand_landmarks:
      hand_position=[]
      for id, lm in enumerate(handLms.landmark):
        h,w,c = img.shape
        cx, cy = int(lm.x*w),int(lm.y*h)
        hand_position.append((cx,cy))
      mpDraw.draw_landmarks(img,handLms,mpHands.HAND_CONNECTIONS)
      ###
      ###
      distance = (handLms.landmark[5].y-handLms.landmark[8].y)*100
      mirrorx = abs(round((handLms.landmark[0].x*-1*1920))+1920)+50#因為是右手
      y = abs(round(handLms.landmark[0].y*1404))-400
      print(mirrorx,y)
      pyautogui.moveTo(mirrorx,y)
      
      if(distance<=2 and hand_down==0):
        hand_down = 1
        pyautogui.moveRel(5,0)
        pyautogui.click(clicks=2)
        pyautogui.mouseDown()
      elif(distance>=2 and hand_down==1):#不能直接else不然所有條件都會觸發hand_down
          print(hand_down)
          hand_down =0
          pyautogui.mouseUp()
      
    
     

      
  cTime = time.time()
  fps = 1/(cTime-pTime)
  pTime=cTime
  cv2.putText(img, str(int(fps)),(10,70), cv2.FONT_HERSHEY_PLAIN,
              3,(255,0,255),3)
  cv2.imshow("image", img)
  if cv2.waitKey(1) & 0xFF == 27:
    cv2.destroyWindow('image')
    break
cap.release()