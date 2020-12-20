import csv
import numpy as np
import pandas as pd 

rallyframe = []
csvlist = []
#csvlist.append("set1.csv")
csvlist.append("set2.csv")

class rally:
    def __init__(self,frame, player, aroundhand, backhand):
        self.frame = frame
        self.player = player
        self.aroundhand = aroundhand
        self.backhand = backhand
        if backhand == "0":
            self.fronthand = "1"
        else:
            self.fronthand = "0"

def search_rally(list, platform):
    for i in range(len(list)):
        if str(list[i].frame) == str(platform):
            return list[i]
    return 0

def strip0(str):
    if(str[-2:]) == ".0":
        str = str[:-2]
    return str

if __name__ == '__main__':

    for csvfile in csvlist:
        with open(csvfile, 'r') as f:
            reader = csv.reader(f, delimiter=',')
            line = 1
            for row in reader:
                if line == 1:
                    line+=1
                    continue
                if strip0(row[9]) != "1":
                    row[9] = "0"
                if strip0(row[10]) != "1":
                    row[10] = "0"
                #print(strip0(row[3]))
                r = rally(strip0(row[3]),strip0(row[6]),strip0(row[9]),strip0(row[10]))
                rallyframe.append(r)
                line+=1
    c3 = []

    with open("final.csv","r") as f:

        reader = csv.reader(f, delimiter=',')

        for row in reader:
            line = strip0(row[0])
	
            if len(row)<38:            
                row = (row + [""] * (38 - len(row)))
            
            row = row[ :38]
            
            decision = search_rally(rallyframe,line)
            if decision != 0:
                #print(line)
                if decision.player == "A" and str(strip0(row[1])) == "2":
                    if decision.aroundhand == "1":
                        row.append("aroundhand")
                    elif decision.backhand == "1":
                        row.append("backhand")
                    else:
                        row.append("fronthand")
                    c3.append(row)

                elif decision.player == "B" and str(strip0(row[1])) == "1":
                    if decision.aroundhand == "1":
                        row.append("aroundhand")
                    elif decision.backhand == "1":
                        row.append("backhand")
                    else:
                        row.append("fronthand")
                    c3.append(row)

    
    with open('label2.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['frame','PLAYER_ID','Nose_X','Nose_Y','Neck_X','Neck_Y','RShoulder_X','RShoulder_Y','RElbow_X','RElbow_Y',
                             'RWrist_X','RWrist_Y','LShoulder_x','LShoulder_y','LElbow_x','LElbow_y','LWrist_X','LWrist_Y',
                             'RHip_X','RHip_Y','RKnee_X','RKnee_Y','RAnkle_X','RAnkle_Y','LHip_X','LHip_Y','LKnee_X','LKnee_Y',
                             'LAnkle_X','LAnkle_Y','REye_X','REye_Y','LEye_X','LEye_Y','REar_X','REar_Y','LEar_X','LEar_Y',
                        'class'])
        for row in c3:
            writer.writerow(row)
     
