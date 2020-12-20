import argparse
import logging
import time

import cv2
import numpy as np
import csv
import math
import sys, time

from progressbar import *
from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path, model_wh


logger = logging.getLogger('TfPoseEstimator-Video')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

fps_time = 0

global front_frame_1_x, front_frame_1_y, front_frame_2_x, front_frame_2_y, now_frame_x, now_frame_y
front_frame_1_x=[]
front_frame_2_x=[]
front_frame_1_y=[]
front_frame_2_y=[]
now_frame_x=[]
now_frame_y=[]


if __name__ == '__main__':
    with open('output.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['frame','PLAYER_ID','Nose_X','Nose_Y','Neck_X','Neck_Y','RShoulder_X','RShoulder_Y','RElbow_X','RElbow_Y',
                             'RWrist_X','RWrist_Y','LShoulder_x','LShoulder_y','LElbow_x','LElbow_y','LWrist_X','LWrist_Y',
                             'RHip_X','RHip_Y','RKnee_X','RKnee_Y','RAnkle_X','RAnkle_Y','LHip_X','LHip_Y','LKnee_X','LKnee_Y',
                             'LAnkle_X','LAnkle_Y','REye_X','REye_Y','LEye_X','LEye_Y','REar_X','REar_Y','LEar_X','LEar_Y',
                             'class'])

    parser = argparse.ArgumentParser(description='tf-pose-estimation Video')
    parser.add_argument('--video', type=str, default='')
    parser.add_argument('--write_video', type=str, default='')
    parser.add_argument('--resolution', type=str, default='432x368', help='network input resolution.default=432x368')
    parser.add_argument('--model', type=str, default='mobilenet_thin', help='cmu / mobilenet_thin')
    parser.add_argument('--show-process', type=bool, default=False,
                        help='for debug purpose, if enabled, speed for inference is dropped.')
    parser.add_argument('--showBG', type=str, default='', help='Use it with any non-empty string to show skeleton only.')
    args = parser.parse_args()

    logger.debug('initialization %s : %s' %(args.model, get_graph_path(args.model)))
    w, h = model_wh(args.resolution)
    if w > 0 and h > 0:
        e = TfPoseEstimator(get_graph_path(args.model), target_size=(w, h))
    else:
        e = TfPoseEstimator(get_graph_path(args.model), target_size=(432, 368))
    logger.debug('video read+')
    cap = cv2.VideoCapture(args.video)

    # total frame of a video
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    #print( "total frame of",args.video, length )

    #---------------------------------
    #frame_width = int(cap.get(3))
    #frame_height = int(cap.get(4))
    frame_width = 675
    frame_height = 550
    #---------------------------------

    if args.write_video:
        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    #---------------------------------
        out = cv2.VideoWriter(args.write_video, fourcc, 20.0, (frame_width,frame_height)) # LOOK AT THIS
    #---------------------------------

    #ret_val, image = cap.read()
    #logger.info('cap image=%dx%d' % (image.shape[1], image.shape[0]))

    if cap.isOpened() is False:
        print("Error opening video stream or file")

    backSub = cv2.createBackgroundSubtractorMOG2()
    
    #record frame number
    frame_num = 0

    # progress bar
    pbar = ProgressBar().start()

    while cap.isOpened():
        
        frame_num += 1

        print("now frame : ",frame_num, "total frame : ",length," ")
        #pbar.update(int((frame_num / length) * 100))

        ret_val, image = cap.read()
        
        if(image is None):
            break
        
        image = image[140:140+frame_height, 300:300+frame_width]

        humans = e.inference(image, resize_to_default=True, upsample_size=4.0)
        
        if args.showBG:
            image = np.zeros(image.shape, dtype=np.uint8)
        image = TfPoseEstimator.draw_humans(image, humans, frame_num, imgcopy=False)
        
        #cv2.putText(image, "FPS: %f" % (1.0 / (time.time() - fps_time)),
        #            (10, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        cv2.putText(image, "Frame number: %f" % (frame_num),
                    (10, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        if args.write_video:
            cv2.imshow('tf-pose-estimation result', image)
            out.write(image)
            #print("video output..")
        else:
            cv2.imshow('tf-pose-estimation result', image)
            print(",,,")

        fps_time = time.time()
        if cv2.waitKey(1) == 27:
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

c1 = []
c2 = []
# split output into to csv by player id 
with open('output.csv', 'r') as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        #if len(row)>=2:
        if row[1] == "1":
            c1.append(row)
        elif row[1] == "2":
            c2.append(row)

import pandas as pd 
data1 = pd.read_csv("output.csv")
df1 = pd.DataFrame(data=data1)
df1 = df1.interpolate(method ='linear', axis=0)
df1 = df1[df1.PLAYER_ID == 1]
df1.to_csv("output_player1_after_interpolate.csv", index = False)

data2 = pd.read_csv("output.csv")
df2 = pd.DataFrame(data=data2)
df2 = df2.interpolate(method ='linear', axis=0)
df2 = df2[df2.PLAYER_ID == 2]
df2.to_csv("output_player2_after_interpolate.csv", index = False)

print( "total frame of",length )
logger.debug('finished+')
