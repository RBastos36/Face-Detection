# Sistemas Avançados de Visão Industrial (SAVI 23-24)
# Grupo 6, DEM, UA
# Nome 1
# Nome 2
# Nome 3

import copy
# import csv
# import math
# import time
from random import randint
import face_recognition
import cv2
import numpy as np
from track import Detection, Track, computeIOU
# from colorama import Fore, Back, Style


def main():

    # --------------------------------------
    # Initialization
    # --------------------------------------
    cap = cv2.VideoCapture(0)


# --------------------------------------
    # Load a sample picture and learn how to recognize it
    obama_image = face_recognition.load_image_file("obama.jpg")
    obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

    # Create arrays of known face encodings and their names
    known_face_encodings = [
        obama_face_encoding
    ]

    known_face_names = [
        "Barack Obama"
    ]

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
# --------------------------------------



    # Parameters
    distance_threshold = 100
    deactivate_threshold = 5.0 # secs
    iou_threshold = 0.3

    video_frame_number = 0
    person_count = 0
    tracks = []

    # --------------------------------------
    # Execution
    # --------------------------------------
    while(cap.isOpened()): # iterate video frames

        # Grab a single frame of video
        result, image_rgb = cap.read() # Capture frame-by-frame
        if result is False:
            break

        frame_stamp = round(float(cap.get(cv2.CAP_PROP_POS_MSEC))/1000,2)
        height, width, _ = image_rgb.shape
        image_gui = copy.deepcopy(image_rgb) # good practice to have a gui image for drawing

    
        # ------------------------------------------------------
        # Detect people using Face Recognition
        # ------------------------------------------------------
        # Only process every other frame of video to save time
        if process_this_frame:
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(image_rgb, (0, 0), fx=0.5, fy=0.5)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            # rgb_small_frame = small_frame[:, :, ::-1]
            rgb_small_frame = np.ascontiguousarray(small_frame[:, :, ::-1])

            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                face_names.append(name)

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

        # ------------------------------------------------------
        # Association step. Associate detections with tracks
        # ------------------------------------------------------
        idxs_detections_to_remove = []
        for idx_detection, detection in enumerate(detections):
            for track in tracks:
                if not track.active:
                    continue

                # --------------------------------------
                # Using IOU
                # --------------------------------------
                iou = computeIOU(detection, track.detections[-1])
                print('IOU( ' + detection.detection_id + ' , ' + track.track_id + ') = ' + str(iou))
                if iou > iou_threshold: # This detection belongs to this tracker!!!
                    track.update(detection) # add detection to track
                    idxs_detections_to_remove.append(idx_detection)
                    break # do not test this detection with any other track

        idxs_detections_to_remove.reverse()

        print('idxs_detections_to_remove ' + str(idxs_detections_to_remove))
        for idx in idxs_detections_to_remove:
            print(detections)
            print('deleting detection idx ' + str(idx))
            del detections[idx]

        # --------------------------------------
        # Create new trackers
        # --------------------------------------
        for detection in detections:
            color = (randint(0, 255), randint(0, 255), randint(0, 255))
            track = Track(name, detection, color=color)
            tracks.append(track)
            person_count += 1

        # --------------------------------------
        # Deactivate tracks if last detection has been seen a long time ago
        # --------------------------------------
        for track in tracks:
            time_since_last_detection = frame_stamp - track.detections[-1].stamp
            if time_since_last_detection > deactivate_threshold:
                track.active = False
               
        # --------------------------------------
        # Visualization
        # --------------------------------------

        # Draw list of all detections (including those associated with the tracks)
        for detection in all_detections:
            detection.draw(image_gui, (255,0,0))

        # Draw list of tracks
        for track in tracks:
            if not track.active:
                continue
            track.draw(image_gui)


        if video_frame_number == 0:
            cv2.namedWindow('GUI',cv2.WINDOW_NORMAL)
            cv2.resizeWindow('GUI', int(width), int(height))

        # Add frame number and time to top left corner
        cv2.putText(image_gui, 'Frame ' + str(video_frame_number) + ' Time ' + str(frame_stamp) + ' secs',
                    (10,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2, cv2.LINE_AA)

        # Display the resulting image
        cv2.imshow('GUI',image_gui)
        
        # Hit 'q' on the keyboard to quit
        if cv2.waitKey(1) & 0xFF == ord('q') :
            break

        video_frame_number += 1

    
if __name__ == "__main__":
    main()