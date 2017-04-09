#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  9 12:45:28 2017

@author: alex
"""


import sys
import datetime
import os.path
import dicom
from dicom.dataset import Dataset, FileDataset
import dicom.UID

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2

#read a working color example

dataset = dicom.read_file("/home/alex/Pictures/WORKING-OT-PAL-8-face.dcm", force=True)
print(dataset)