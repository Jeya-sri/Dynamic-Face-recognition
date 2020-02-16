import numpy as np
import face_rec
import glob
import os
import cv2
import datetime
import enroll as e
import shutil 
import store  
import random as r


def loader(f_encoding, kfn):

    #TODO : Add Text Log too in addition to video logs.
    #temp vars : failed, fold_name, folder, image
    #params : f_encoding, kfn, kfe
    print('Loading DataSet...')
    failed = 0
    cwd = os.getcwd() + '/faces/'
    #print(cwd)
    for folder in os.listdir(cwd):
        fold_name = folder
        folder = 'faces/' + folder
        if os.path.isdir(folder):
            #print('\tLoading :'+folder)
            for subfolder in os.listdir(folder):
                #print('\t\t'+subfolder)
                path = folder + '/' + subfolder + '/*.jpg'
                for img in glob.glob(path): # Add all images to comparison list
                    try:
                        #print('\t\t\t'+img)
                        kfn += [fold_name]
                        image = face_rec.load_image_file(img) 
                        f_encoding.append(face_rec.face_encodings(image)[0]) # Append the results
                    #    print(len(f_encoding))
                    except:
                        failed += 1
                else:
                    #print('\t\t\tNo images found')
                    pass

    print('Loaded ' + str(len(f_encoding)) + ' samples')
    print('Failed Loading ' + str(failed) + ' samples')

    #Copying Encoded faces from f_encoding to Known Face Encoding(kfe)
    return f_encoding


def init(kfe, kfn):

    #temp vars : names, flag, floc, fe, ctr, prev_name, video, width, height, vname, out,
    #            rframe, rgbrframe, matched_faces, fdist, best_match, name, gray,                   

    print('kfn ', *kfn)
    print('kfe ',len(kfe))
    names = []
    flag = True
    floc = []
    fe = []
    ctr=0
    name = " "
    prev_name = " "

    print('Press " e " | " r " to enroll..')

    video = cv2.VideoCapture(0) #start cam

    width = int(video.get(3))
    height = int(video.get(4))
    vname  = 'output.avi'

    out = cv2.VideoWriter(vname,cv2.VideoWriter_fourcc('M','J','P','G'), 10, (width,height))

    while(1):
        ret,frame = video.read() #grab frame by frame while(1)

        rframe = cv2.resize(frame,(0,0),fx=0.25,fy=0.25) #not needed ,
                                                    #just to make the process faster 

        rgbrframe = cv2.cvtColor(rframe,cv2.COLOR_BGR2RGB)#cv2 uses BGR color whereas,
                                #face_rec uses RGB , so reverse content

        out.write(frame) # write  to videoLog

        if flag:
            floc = face_rec.face_locations(rgbrframe) # grab face from frame
            fe   = face_rec.face_encodings(rgbrframe,floc) # grab face encodings from frame 

            for fenc in fe:
                matched_faces = face_rec.compare_faces(kfe,fenc)

                fdist = face_rec.face_distance(kfe,fenc)
                try:
                    best_match = np.argmin(fdist)
                except:
                    pass
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
                            try:
                                f1_encoding =  face_rec.face_encodings(f1)[0]#Encoding unknown face 
                            except: pass
                            kfe.append(f1_encoding)
                            s = 'Suspect'+str(ctr) #Detected Unknown face encoded as Suspect :)
                            kfn.append(s)
    
        r1 = r.randint(0,100)
        if r1 / 2 == 0:
            store.sframes(name,frame)
        flag = not flag
        names += [name]
        cv2.imshow('Video', frame) #show frames as being processed.

        #print('Here',*names)    
        #No markings are done on live frames so as to reduce the flickering on screen/video feed. Instead, as like on generic systems, results are shown on a terminal/console.

        #TODO : Show on Text Area while adding Flask front-end.

    
        if cv2.waitKey(1) & 0xFF == ord('q'):
            out.release()
            video.release()
            cv2.destroyAllWindows()
            break

        if cv2.waitKey(1) & 0XFF == ord('e') or cv2.waitKey(1) & 0XFF == ord('r'):
            print('Begin Enrollment....')
            video.release()
            cv2.destroyAllWindows()

            e.enroll()
            init(kfe, kfn)
    
    return names



#saving video logs to personal folder.
f_encoding = []  # Face encodings  for each face.
kfn = [] # Known Face Names.
kfe = [] # Known Face Encondings
names = []

kfe = loader(f_encoding, kfn)
names = init(kfe, kfn)
store.store(names)
print('All Videos Logged....')
video.release()
cv2.destroyAllWindows()
