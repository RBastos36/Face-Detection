#!/usr/bin/env python3
# Sistemas Avançados de Visão Industrial (SAVI 23-24)
# Grupo 6, DEM, UA
# Afonso Miranda, nMec100090
# João Nogueiro, nMec111807
# Ricardo Bastos, nMec103983


import copy
# import csv
# import math
# import time
from random import randint
import face_recognition
import cv2
import numpy as np
from track import Detection, Track, computeIOU
from gui import ImageApp
# from colorama import Fore, Back, Style
import os, sys
import pyttsx3
from matplotlib import pyplot as plot
from threading import Thread    # Threading library for parallel tasks


def main():

    # --------------------------------------
    # Initialization
    # --------------------------------------
    cap = cv2.VideoCapture(0)

    # Create arrays of known face encodings and their names
    known_face_encodings = []
    known_face_names = []
    database_photos = []

    # Read database of saved images
    if len(os.listdir("Database")) != 0:
        for file in os.listdir("Database"):
            if len(os.listdir("Database")) == 0:
                break

            if file.endswith(".jpg"):
                image = face_recognition.load_image_file("Database/" + file)
                image_encoding = face_recognition.face_encodings(image)[0]
                known_face_encodings.append(image_encoding)
                known_face_names.append(file.rsplit('.', 1)[0].capitalize())
                database_photos.append(image)

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    len_old_database = 0
    hellos = []
    engine = pyttsx3.init()

    # Parameters
    distance_threshold = 100
    deactivate_threshold = 5.0 # secs
    iou_threshold = 0.3

    video_frame_number = 0


    # --------------------------------------
    # Execution
    # --------------------------------------
    while(cap.isOpened()): # iterate video frames
        
        # Grab a single frame of video
        result, image_rgb = cap.read() # Capture frame-by-frame
        if result is False:
            break

        image_rgb = cv2.flip(image_rgb, 1)
        frame_stamp = round(float(cap.get(cv2.CAP_PROP_POS_MSEC))/1000,2)
        height, width, _ = image_rgb.shape
        image_gui = copy.deepcopy(image_rgb)    # good practice to have a gui image for drawing
    
        # ------------------------------------------------------
        # Detect people using Face Recognition
        # ------------------------------------------------------

        # Only process every other frame of video to save time
        if process_this_frame:
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(image_rgb, (0, 0), fx=0.5, fy=0.5)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = np.ascontiguousarray(small_frame[:, :, ::-1])

            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            
            # Loop to check if faces are known
            for idx, face_encoding in enumerate(face_encodings):
                # See if the face is a match for the known face(s)
                if len(known_face_encodings) != 0:
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                # Find the known face with the smallest distance to the new face
                if len(known_face_encodings) != 0:
                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]
                        if name not in hellos:
                            engine.say("Hello " + name)
                            engine.runAndWait()
                            hellos.append(name)
                face_names.append(name)

                # Ask for Unknown detection and Save it
                if name.lower() == "unknown":
                    name = input("What is your name? ")
                    engine.say("Hello " + name)
                    engine.runAndWait()
                    hellos.append(name)
                    cv2.imwrite("Database/" + name.lower() + ".jpg", small_frame[face_locations[idx][0]-30:face_locations[idx][2]+30,
                                                                                 face_locations[idx][3]-30:face_locations[idx][1]+30])
                    image = face_recognition.load_image_file("Database/" + name.lower() + ".jpg")
                    
                    # Exception handling for when the saved detection is "corrupted" and saves image without recognisable face
                    try:
                        image_encoding = face_recognition.face_encodings(image)[0]
                        known_face_encodings.append(image_encoding)
                        known_face_names.append(name)
                        database_photos.append(image)
                        face_names.append(name)

                    except IndexError:
                        print("Database loading ERROR! Deleting corrupted file!")
                        os.remove("Database/" + name.lower() + ".jpg")      # Delete "corrupted" file
                

        process_this_frame = not process_this_frame

        # ------------------------------------------------------
        # Create list of detections
        # ------------------------------------------------------
        detections = []
        detection_idx = 0
        for top, right, bottom, left in face_locations:
            name = face_names[detection_idx]
            detection_id = str(video_frame_number) + '_' +  str(detection_idx)
            detection = Detection(left, right, top, bottom, detection_id, frame_stamp, name)
            detections.append(detection)
            detection_idx += 1

        all_detections = copy.deepcopy(detections)
               
        # --------------------------------------
        # Visualization
        # --------------------------------------
        
        # Draw list of all detections (including those associated with the tracks)
        for detection in all_detections:
            detection.draw(image_gui, (255,0,0))


        # Show database and update it in real time when new face is added
        if len(database_photos) > len_old_database:
            cv2.namedWindow('Database',cv2.WINDOW_NORMAL)   # Initializing new window for the Database

            images = copy.deepcopy(database_photos)
            max_height = max(image.shape[0] for image in database_photos)

            # Resizing image to the height of the tallest one
            for i, image in enumerate(images):
                if image.shape[0] < max_height:
                    scale_factor = max_height / image.shape[0]
                    images[i] = cv2.resize(image, (int(image.shape[1] * scale_factor), max_height))
            
            # 
            combined_width = sum(image.shape[1] for image in images)
            combined_image = np.zeros((max_height, combined_width, 3), dtype=np.uint8)

            current_width = 0
            for image in images:
                combined_image[:image.shape[0], current_width:current_width + image.shape[1]] = image
                current_width += image.shape[1]

            data_show = np.ascontiguousarray(combined_image[:, :, ::-1])

            cv2.imshow('Database', data_show)
            len_old_database = len(database_photos)

        # Initializing FaceTracker window and resizing it 
        if video_frame_number == 0:
            cv2.namedWindow('FaceTracker',cv2.WINDOW_NORMAL)
            cv2.resizeWindow('FaceTracker', int(width), int(height))

        # Add frame number and time to top left corner
        cv2.putText(image_gui, 'Frame ' + str(video_frame_number) + ' Time ' + str(frame_stamp) + ' secs',
                    (10,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2, cv2.LINE_AA)

        # Display the resulting image
        cv2.imshow('FaceTracker',image_gui)
        
        # Hit 'q' on the keyboard to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        video_frame_number += 1



if __name__ == "__main__":

    # Creting Threads for the face detector and interface, respectively
    thread_1 = Thread(target=main)
    thread_2 = Thread(target=ImageApp().run)

    # Setting Thread as Daemon to not block the main code
    thread_1.setDaemon(True)
    thread_2.setDaemon(True)

    # Starting Threads
    thread_1.start()
    thread_2.start()

    # Joining Thread to the main block after finishing
    thread_1.join()
    thread_2.join()
