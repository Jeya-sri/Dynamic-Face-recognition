import numpy as np
import face_rec
import glob
import os
import cv2
import datetime
import enroll as e
import shutil 

#start webcam
video = cv2.VideoCapture(0)

#Load and encode data(pictures) from folder
#my_dir = 'faces/' # Folder where all your image files reside
f_encoding = [] # Create an empty list for saving encoded files

print('Loading DataSet...')
failed = 0
kfn = [] # known face names list
cwd = os.getcwd() + '/faces/'
for folder in os.listdir(cwd):
    fold_name = folder
    folder = 'faces/' + folder
    if os.path.isdir(folder):
        print('\tLoading :'+folder)
        for subfolder in os.listdir(folder):
            print('\t\t'+subfolder)
            path = folder + '/' + subfolder + '/*.jpg'
            for img in glob.glob(path): # Add all images to comparison list
                try:
                    print('\t\t\t'+img)
                    kfn += [fold_name]
                    image = face_rec.load_image_file(img) 
                    f_encoding.append(face_rec.face_encodings(image)[0]) # Append the results
                #    print(len(f_encoding))
                except:
                    failed += 1
            else:
                print('\t\t\tNo images found')
print('Loaded ' + str(len(f_encoding)) + ' samples')
print('Failed Loading ' + str(failed) + ' samples')
#Copying Encoded faces from f_encoding to Known Face Encoding(kfe)
kfe = f_encoding.copy()


#Loading known face names(kfn) from image names reside in folder
#kfn = []
#parent_dir = 'faces/'
#results = [os.path.basename(f) for f in glob.glob(os.path.join(parent_dir, '*.jpg'))]   
#for i in range(len(results)):
#    a = results[i]
#    a = a[ : -4]
#    kfn.append(a)

#for name in os.listdir(cwd):
#    dirr = 'faces/' + name
#    if os.path.isdir(dirr):
#        kfn.append(name)
print(*kfn)

names = []
flag = True
floc = []
fe = []
ctr=0
prev_name = " "

print('Press " e " | " r " to enroll..')

width = int(video.get(3))
height = int(video.get(4))
vname  = 'faces/'+str(datetime.date.today())+ '.avi'

out = cv2.VideoWriter(vname,cv2.VideoWriter_fourcc('M','J','P','G'), 10, (width,height))

while(1):
    ret,frame = video.read() #grab frame by frame while(1)

    rframe = cv2.resize(frame,(0,0),fx=0.25,fy=0.25) #not needed ,
                                                    #just to make the process faster 

    rgbrframe = cv2.cvtColor(rframe,cv2.COLOR_BGR2RGB)#cv2 uses BGR color whereas,
                                #face_rec uses RGB , so reverse content

    if flag:
        floc = face_rec.face_locations(rgbrframe) # grab face from frame
        fe   = face_rec.face_encodings(rgbrframe,floc) # grab face encodings from frame 
        
        names = []
        for fenc in fe:
            matched_faces = face_rec.compare_faces(kfe,fenc)

            fdist = face_rec.face_distance(kfe,fenc)
            best_match = np.argmin(fdist)
            if matched_faces[best_match]:
                try:
                    name = kfn[best_match]
                    if prev_name != name:
                        print(name + ' - '+str(datetime.datetime.now()))
                    prev_name = name
                except Exception:
                    pass
            else:
                name = 'Unknown'
                if prev_name != name:
                    print('\t!!! Security Alert !!!\n\t\tDetected ' + name + '- ' + str(datetime.datetime.now()))
                prev_name = name
                gray = cv2.cvtColor(rframe,cv2.COLOR_BGR2GRAY)#converting unknowface frame to gray
                faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")#haarcascade unknown person front face
                faces = faceCascade.detectMultiScale(gray,
                        scaleFactor=1.3,
                        minNeighbors=3,
                        minSize=(50, 50)
                )
                if len(faces):#faces contails multiple unknown faces in single frame 
                    for (x, y, w, h) in faces:
                        roi_color = rframe[y : y + 240 , x : x + 360] #cropping unknown face
                        ctr = ctr + 1
                        path = 'unknownDetected/'
                        cv2.imwrite(os.path.join(path , str(ctr)+'Unknown_Face.jpg'), roi_color) #Saving cropped image of unknown to unknownDetected Folder
                        filename = path + str(ctr)+'Unknown_Face.jpg'
                        f1 = face_rec.load_image_file(filename)      
                        f1_encoding =  face_rec.face_encodings(f1)[0]#Encoding unknown face 
                        kfe.append(f1_encoding)
                        s = 'Suspect'+str(ctr) #Detected Unknown face encoded as Suspect :)
                        kfn.append(s)

            names.append(name)
    flag = not flag

    # Display the results
    #for (top, right, bottom, left), name in zip(floc, names):
    #    top *= 4    # resize image back again by *0.25
    #    right *= 4
    #    bottom *= 4
    #   left *= 4

        #cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)# Draw a box around the face
        #cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
        #font = cv2.FONT_HERSHEY_DUPLEX
        #cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (136, 227, 182), 1) #label the face
         
    cv2.imshow('Video', frame)

    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if cv2.waitKey(1) & 0XFF == ord('e') or cv2.waitKey(1) & 0XFF == ord('r'):
        print('Begin Enrollment....')
        video.release()
        cv2.destroyAllWindows()
        e.enroll()
    out.release()
   

#saving video logs to personal folder.
per_name = ' '
for name in names:
    if per_name != name:
        if name != 'Unknown' or name != 'Suspect'
        dest = 'faces/' + name + str(datetime.date.today()) + '/'
        shutil.copy2('output.avi',dest)
        print('\n\t' + name + ' Logged...')
    per_name = name


video.release()
cv2.destroyAllWindows()
