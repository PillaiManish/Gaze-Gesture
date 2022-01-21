from django.http import HttpResponse
from django.shortcuts import render,redirect
import cv2

#imports
import dlib
import numpy as np
from math import hypot
from imutils import face_utils
from .utils import *
# import winsound
import time
 
from accounts.models import Gaze


# Create your views here.
def homepage(request):
    keyboard=np.zeros((300,800,3),np.uint8)
    
    # Abhbi ke liye sirf 5 words rakha hei
    key_set = {
    0: "0",
    1: "1",
    2: "2",
    3: "3",
    4: "4",
    5: "5"
    }
    centre_col_index = []
    
    frame_count_column=0 #this is frame count for column
    frame_count_step=0 #this is frame count for row
    col_index=[]
    col=0
    blink_count=0 #this for couting the blink (used for blink for changing the row and column)
    blink_count_indivisual_key=0 #this is for counting the blink to check whether the key should press or not
    font_letter=cv2.FONT_HERSHEY_PLAIN
    col_select=False #this for selecting the particular column
    step=0 #this is to count the row after particular column is selected
    IMG_SIZE=(34,26)
    ###################
    type_text="" #this is to store the typed character
    ################

    
    
    # Mera trial
    last_col = False
    sec = 0
    gazes = Gaze.objects.get(user=request.user)
    gazePassword = gazes.gazePassword


    password = gazePassword
    # password = ["2","2","3","1"]
    step_chances = 2
    retry_chances = 3
    
    # ek list banake maybe average will work
    selected = -1
    
    
    # Jo selected hei uska list banau ya variable hmmmm sochna hei
    # selected = 0
    
    #user defined class object for blink detection using cnn model
    bd=Blink_detection()
    white_board=np.ones((100,800,3),np.uint8)
    
    
    #######################
    detector=dlib.get_frontal_face_detector()
    predictor=dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
    print(predictor, "predictor")
    cap=cv2.VideoCapture(0)
    #####################
    


    # Ye function range ke according value aane ke liye hei
    def valueByRange(value, key_set):
        if value in range(0,20):
            return key_set[0]
        elif value in range(20,40):
            return key_set[1]
        elif value in range(40, 60):
            return key_set[2]
        elif value in range(60, 80):
            return key_set[3]
        elif value in range(80, 101):
            return key_set[4]
        





    
    # keyboard me jo letter hei woh too show ho gaya
    #FUNCTION TO DRAW KEYBOARD
    def draw_keyboard(letter_index,letter,light):
        x = 250
        y = 100
        font=cv2.FONT_HERSHEY_PLAIN
        letter_thickness=2
        key_space=2
        font_scale=3
        height=50
        width=80
        if light==True:
            cv2.rectangle(keyboard,(x+key_space,y+key_space),(x+width-key_space,y+height-key_space),(0,255,0),-1)
        else:
            cv2.rectangle(keyboard,(x+key_space,y+key_space),(x+width-key_space,y+height-key_space),(0,255,0),key_space)
        letter_size=cv2.getTextSize(letter,font,font_scale,letter_thickness)[0]
        letter_height,letter_width=letter_size[1],letter_size[0]
        letter_x=int((width-letter_width)/2)+x
        letter_y=int((height+letter_height)/2)+y
        cv2.putText(keyboard,letter,(letter_x,letter_y),font,font_scale,(255,255,255),letter_thickness)
        
        # ye index hei alphabet kaha aana chaiyee uska
        col_index = 500,500
    
    next_step = False
    while True:
    
        if next_step:
            key=cv2.waitKey(10)
            if key==ord('c'):
                next_step = False
                pass
            else:
                continue
        main_windows = np.zeros((780,1000,3),np.uint8)
        if col_select==True:  
            frame_count_step=frame_count_step+1
        else:
            frame_count_column=frame_count_column+1
    
    
        if sec % 20 == 0 and sec <= 100:
            
        
        
            print(sec//20)
            keyboard[:]=(0,0,0) #reseting the keyboard
        
            draw_keyboard(sec//20,key_set[sec//20],True)
        elif sec > 100:
        
        
        
            # Agar column select ho gaya too
        
            if col_select:
                col_select = False  


                print("Step", step)

                if password[step] == valueByRange(selected, key_set):
                    main_windows = np.zeros((780,1000,3),np.uint8)
                    cv2.putText(main_windows,"------PRESS C for next step------",(375,325), font_letter,1, (0,0,255),2)
                    step +=1
                    print("Huuray we are close again VAMS")
                
                else:

                    if step >=1:
                        if step_chances > 0:
                            step_chances -=1
                            main_windows = np.zeros((780,1000,3),np.uint8)
                            cv2.putText(main_windows,"------WRONG ENTRY: PRESS C to retry Step" + str(step) + " ------",(375,325), font_letter,1, (0,0,255),2)

                        else:
                                if retry_chances > 0:
                                    step = 0
                                    step_chances = 2
                                    retry_chances -= 1
                                    main_windows = np.zeros((780,1000,3),np.uint8)
                                    cv2.putText(main_windows,"------WRONG ENTRY: PRESS C to retry------",(375,325), font_letter,1, (0,0,255),2)
                                else:
                                    step = -1
                                    main_windows = np.zeros((780,1000,3),np.uint8)
                                    cv2.putText(main_windows,"------No More Chances Left------",(375,325), font_letter,1, (0,0,255),2)
                    else:
                        if retry_chances > 0:
                            step = 0
                            step_chances = 2
                            retry_chances -= 1
                            main_windows = np.zeros((780,1000,3),np.uint8)
                            cv2.putText(main_windows,"------WRONG ENTRY: PRESS C to retry------",(375,325), font_letter,1, (0,0,255),2)
                        else:
                            step = -1
                            main_windows = np.zeros((780,1000,3),np.uint8)
                            cv2.putText(main_windows,"------No More Chances Left------",(375,325), font_letter,1, (0,0,255),2)




                #     # yaha pe ek condition aayega ki tab tak he continue karna hei jab tak 4 step nahi hota
                #    main_windows = np.zeros((780,1000,3),np.uint8)
                #    cv2.putText(main_windows,"------PRESS C for next step------",(375,325), font_letter,1, (0,0,255),2)
                #    print("selected", valueByRange(selected, key_set))
                keyboard[:]=(0,0,0) #reseting the keyboard
                next_step = True
                selected = -1


        
            sec = 0
            keyboard[:]=(0,0,0)
            draw_keyboard(sec//20,key_set[sec//20],True)
        
        
        
        # Agar Last column hei toooo step badhana hei
        #    if last_col == True:
        #        step += 1
        
        
        else:
            frame_count_column=frame_count_column+1
        
        
        
        
        
        
        
        
        
        #    if frame_count_column==10:
        #        col=col+1
        #        if col==10:
        #            col=0 #reseting the column
        #        frame_count_column=0
        #    if frame_count_step==10:
        #        step=step+1
        #        if step==6:
        #            step=0 #resetting the row
        #            col_select=False
        #        frame_count_step=0
        
        # keyboard[:]=(0,0,0) #reseting the keyboard (yee tab use aayega jab apne ko keyboard reset karna rahega)
        
        
        
        
        # if col_select==False:
        #     for i in range(0,6):
                
        #         # todha sleep/gap ke baad aane ke liye
        
        #         if i in col_index:
        #             cv2.putText(white_board,type_text,(10,50),cv2.FONT_HERSHEY_PLAIN,5,(255,255,255),3)
        #             keyboard[:]=(0,0,0) #reseting the keyboard
        #             draw_keyboard(i,key_set[i],True)
        
        #         else:
        #             keyboard[:]=(0,0,0) #reseting the keyboard
        
        #             draw_keyboard(i,key_set[i],False)
        # else:
        #     for i in range(0,60):
        #         if i == col_index[row]:
        #             draw_keyboard(i,key_set[i],True)
                    
        #         else:
        #             draw_keyboard(i,key_set[i],False)
        
        #Blink integration begin
        _,frame=cap.read() #reading the frame form the webcam
        
        
        frame = cv2.flip(frame, flipCode=1 )
        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY) #coverting the bgr frame to gray scale
        faces=detector(gray) #this returns the dlib rectangle
        #now extracting the rectangle which contain the upper and lower cordinates of the face
        for face in faces:
            shapes = predictor(gray, face)
            shapes = face_utils.shape_to_np(shapes)
        
            eye_img_l, eye_rect_l = bd.crop_eye(gray, eye_points=shapes[36:42])
            eye_img_r, eye_rect_r = bd.crop_eye(gray, eye_points=shapes[42:48])
        
            eye_img_l = cv2.resize(eye_img_l, dsize=IMG_SIZE)
            eye_img_r = cv2.resize(eye_img_r, dsize=IMG_SIZE)
            eye_img_r = cv2.flip(eye_img_r, flipCode=1)
        
            
        
        
            eye_input_l = eye_img_l.copy().reshape((1, IMG_SIZE[1], IMG_SIZE[0], 1)).astype(np.float32) / 255.
            eye_input_r = eye_img_r.copy().reshape((1, IMG_SIZE[1], IMG_SIZE[0], 1)).astype(np.float32) / 255.
        
            pred_l,pred_r=bd.model_predict(eye_input_l,eye_input_r)
        
        
            sec +=1
            print(sec)
        
        
        
            # Ye blink condition hei
            if pred_l < 0.1 and pred_r <0.1:
                cv2.putText(main_windows,"------BLINK DETECTED------",(375,325), font_letter,1, (0,0,255),2)
        
                print("blink detected ", blink_count)
                blink_count=blink_count+1
                
        
        
                # Yaha kuch too aise likhna padega jo current view ko store kare
        
        
        
        
        
                # ye too row select karne ke liye tha, kuch aur sochna padega yaha
                if col_select==True:
                    blink_count_indivisual_key=blink_count_indivisual_key+1
                    frame_count_step=frame_count_step-1
                else:
                    frame_count_column=frame_count_column-1
            
            
            # Agar blink nahi hua too
            else:
                blink_count=0
                blink_count_indivisual_key=0
            if blink_count==1:
                col_select=True
                if selected == -1:
                        selected = sec
                # yaha pe vo value (current number) ka ayega
                # then humko ye step aage badhana hei
        
        
        
        
        
            #implementing keyboard typing
            if blink_count_indivisual_key==10 and col_select==True and col_select==False: # last ka condition maine add kiya todha jugaad ke liye
                col_select=False #to disable the active column
                type_text=type_text+key_set[col_index[step]]
                blink_count_indivisual_key=0
                white_board[:]=(0,0,0)
                # winsound.Beep(500,100)
                cv2.putText(white_board,type_text,(10,50),cv2.FONT_HERSHEY_PLAIN,5,(255,255,255),3)
                step=0 #resetting the row
        
        
        
        
        
            # Ispe haat bhi maat lagao
            # visualize
            state_l = 'O %.1f' if pred_l > 0.1 else '- %.1f'
            state_r = 'O %.1f' if pred_r > 0.1 else '- %.1f'
        
            state_l = state_l % pred_l
            state_r = state_r % pred_r
        
            cv2.rectangle(frame, pt1=tuple(eye_rect_l[0:2]), pt2=tuple(eye_rect_l[2:4]), color=(64,224,208), thickness=2)
            cv2.rectangle(frame, pt1=tuple(eye_rect_r[0:2]), pt2=tuple(eye_rect_r[2:4]), color=(255,0,0), thickness=2)
        
            # Combaining all windows into single window:
            main_windows[50:150, 100:200] = cv2.resize(cv2.cvtColor(eye_img_l,cv2.COLOR_BGR2RGB),(100,100))
            cv2.putText(main_windows,"LEFT EYE",(100,170), font_letter,1, (0,255,0),1)
            cv2.putText(main_windows,str(state_l+"%"),(100,200), font_letter,2, (0,0,255),1)
            main_windows[50:150, 800:900] = cv2.resize(cv2.cvtColor(eye_img_r,cv2.COLOR_BGR2RGB),(100,100))
            cv2.putText(main_windows,"RIGHT EYE",(800,170), font_letter,1, (0,255,0),1)
            cv2.putText(main_windows,str(state_r+"%"),(800,200), font_letter,2, (0,0,255),1)
        
            main_windows[0:300, 300:700]= cv2.resize(frame,(400,300))
            main_windows[350:650, 100:900] =  keyboard
            main_windows[670:770, 100:900] = white_board
            cv2.imshow("Main_Windows",main_windows)
        key=cv2.waitKey(10)
        if key==ord('q'):
            break
    cv2.destroyAllWindows()
    

