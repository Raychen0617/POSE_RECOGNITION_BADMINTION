import csv
import numpy as np
import pandas as pd 
import math

if __name__ == '__main__':

    data1 = pd.read_csv("label.csv")
    df1 = pd.DataFrame(data=data1)
    data2 = pd.read_csv("label2.csv")
    df3 = pd.DataFrame(data=data2)
    df1 = df1.append(df3,ignore_index=True)


    df1 = df1.interpolate(method ='linear', axis=0)
    df2 = df1
    df1 = df1[df1.PLAYER_ID == 1]
    df2 = df2[df2.PLAYER_ID == 2]

    df2 = df2.sort_values(by=['class'])
    df1 = df1.sort_values(by=['class'])
    df1.to_csv("output_player1_after_interpolate.csv", index = False)
    df2.to_csv("output_player2_after_interpolate.csv", index = False)

'''
    data1 = pd.read_csv("output.csv")
    df1 = pd.DataFrame(data=data1)
    #df1 = df1.interpolate(method ='linear', axis=0)

    data2 = pd.read_csv("output2.csv")
    df2 = pd.DataFrame(data=data2)
    df2 = df2.drop(df2.index[0:107880])
    #df2 = df2[df2.frame > 52248]
    
    #print(df2)

    df3 = df1.append(df2)
    df3.to_csv("final.csv", index = False)
''' 

