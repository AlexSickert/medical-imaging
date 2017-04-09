#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

WHAT THIS PROGRAM DOES:
    

1) All images must be cropped to 256x256
2) There is an Excel file inside. It has the file name of every image as well 
   certain attributes. The goal is to take every image that has the same 
   attribute under the "Mass Shape" column and combine them all into once 
   folder. For example, one type of mass shape is "Oval". 
   Find all the images that have the "Oval" chracterstic and put them 
   all into one folder. 

3) You can get rid of the images that are called masks. They are just black 
   with a white spot. Delete all of those. 


"""

import os
import re
import pandas as pd
import cv2
import matplotlib.image as mpimg
import numpy as np

image_path = "/home/alex/CODE/GliaLabs/Dataset-by-Mass-Shape/Input/JPEG/JPEG"
csv_file_path = "/home/alex/CODE/GliaLabs/Dataset-by-Mass-Shape/Input/JPEG/JPEG/mass_case_description_train_set.csv"
output_path = "/home/alex/CODE/GliaLabs/Dataset-by-Mass-Shape/Output/"
image_size = 256
mask_treshold = 0.2  # percentage value of non-zero pixels

# read the csv
data_table = pd.read_csv(csv_file_path, sep=',')


#get values from table based on folder path data
def get_from_table(patient, side, view, abn_num):
    
    global data_table
    
    print("processing patient " + patient)
    
    patient = "P_" + patient
    
    r = data_table.loc[(data_table.patient_id == patient.upper()) & (data_table.side == side.upper()) & (data_table.view == view.upper()) & (data_table.abn_num == int(abn_num))]

    if(len(r.index) != 1):
        ret = "ERROR"
    else:
        ret = r.iloc[0]['mass_shape']
        
    file_name_fragment = patient.upper() + "_" + side.upper() + "_" + view.upper() + "_" + str(abn_num)
    return ret, file_name_fragment

#for a given path copy images from source to target and resize them
def copy_resize_images(source_file, destination_folder):

    global image_size
    global mask_treshold

    img = mpimg.imread(source_file) 
    image = cv2.resize(img, (image_size, image_size))  
    
    x = np.count_nonzero(image, axis=None)
    nonzero_ration = x / (image_size * image_size)

    if(nonzero_ration > mask_treshold):
        cv2.imwrite(destination_folder,image)


# This is the main function / loop of the program
# loop through all the files and look them up in the table and then decide
# if the file needs to be copied and resized
for subdir, dirs, files in os.walk(image_path):
    for file in files:

        path_str = os.path.join(subdir, file)

        m = re.search('Training_(.+?)\/', path_str)
        if m:
            found = m.group(1)

            arr = found.split("_")
            value_from_table , file_name_fragment = get_from_table(arr[1], arr[2], arr[3], arr[4])
            
            destination_folder = output_path + "/" + str(value_from_table)
            
            #make destination folder if it does not exist
            if not os.path.exists(destination_folder):
                os.makedirs(destination_folder)
                
            # check if file is an image file and only then process it
            m_f = re.search('(.+?)\.jpg', file)            
            
            if m_f:
                file = file_name_fragment + "_" + file
                copy_resize_images(path_str, os.path.join(destination_folder, file))

print("END OF PROGRAM")            