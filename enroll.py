import cv2
import os
import datetime

def enroll():
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')#face_cascade

    name = input("Person's Name : ")
    try:
        os.mkdir('faces')
    except:
        pass

    try:
        os.mkdir('faces/' +name)
        subdir = 'faces/'+ name+'/' + str(datetime.date.today())
        os.mkdir(subdir)
        os.mkdir('faces/' + name+'/Enrollment_data')
    except FileExistsError:
        print("Error !, Person Already Exists...")
        print('Might be a camera glitch... \n\t\tTrying again....')
        return
    else:
        print("Starting Camera.... \nGet Ready...")

    cap = cv2.VideoCapture(0)  #webcam_feed
    
    width = int(cap.get(3))
    height = int(cap.get(4))
    vname  = 'faces/' + name +'/Enrollment_data/'+str(datetime.datetime.now())+ '.avi'
    
    out = cv2.VideoWriter(vname,cv2.VideoWriter_fourcc('M','J','P','G'), 10, (width,height))
    
    # cap = cv2.VideoCapture('filename.mp4') #file_feed
    
    print('press "s" to stop enrolling/camera')
    ctr = 0
    
    while True:
        ret, frame = cap.read() #read_frames
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #grayscale_coversion
        faces = face_cascade.detectMultiScale(gray, 1.1, 4) #face_detection

        out.write(frame)
        
        for (x, y, w, h) in faces:
            fname = subdir + '/' + name + '_' + str(ctr) + '.jpg'
            cv2.imwrite(fname,frame)
            ctr += 1
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2) #mark with a rectangle
        cv2.imshow('Make Sure You Look Good', frame) #show the faces
        
        
        if cv2.waitKey(1) & 0XFF == ord('s') :
            print('Gained'+str(ctr)+'frames of '+name)
            out.release()
            cap.release()
            cv2.destroyAllWindows()
            return

def lister():
    print(*[name for name in os.listdir('.') if os.path.isdir(name)], sep = '\n')


#enroll()
#lister()
