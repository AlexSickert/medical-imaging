#import dicom
#

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
from dicom.tag import Tag


# Consider these sources: 
#    
# http://stackoverflow.com/questions/14350675/create-pydicom-file-from-numpy-array

# using this online viewer http://dicomviewer.booogle.net/ 

#ds = dicom.read_file("/home/alex/CODE/GliaLabs/DICOM-encoder/pydicom-master/tests/test_files/rtplan.dcm")
#
#
#dicom.dataset.


class Dicom_Encoder:
    
    def encode(self, input_image, text, output_file):
        
        print("using file: " + input_image)
        print("analysis result is: " + text)
        
        # first we need to setup some meta data
        # Populate required values for file meta information
        file_meta = Dataset()
        file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.2'  # CT Image Storage .... check here: http://dicom.nema.org/dicom/2013/output/chtml/part04/sect_B.5.html
        file_meta.MediaStorageSOPInstanceUID = "1.2.3"  # !! Need valid UID here for real work
        file_meta.ImplementationClassUID = "1.2.3.4"  # !!! Need valid UIDs here        
        
        
        # Create the FileDataset instance (initially no data elements, but file_meta supplied)
        ds = FileDataset(output_file, {}, file_meta=file_meta, preamble=b"\0" * 128)
        
        # Add the data elements -- not trying to set all required here. Check DICOM standard
#        ds.PatientName = "John Smith2"      
        ds.add_new(Tag(0x10,0x10), "PN", "John 99") # this is the tag for patient's name
       
        ds.PatientID = "123456"
        
        
        # Set the transfer syntax
        ds.is_little_endian = True
        ds.is_implicit_VR = True
        
        # Set creation date/time
        dt = datetime.datetime.now()
        ds.ContentDate = dt.strftime('%Y%m%d')
        timeStr = dt.strftime('%H%M%S.%f')  # long format with micro seconds
        ds.ContentTime = timeStr
        
        # imge file data
#        read this   http://stackoverflow.com/questions/14350675/create-pydicom-file-from-numpy-array  
#        img=mpimg.imread(input_image)
        img = cv2.imread(input_image, 0)   # we read the image monochrome
        print(img.shape)
        plt.imshow(img)
        
        print(img.shape[0])
        
        
        ds.SamplesPerPixel = 1
        ds.PhotometricInterpretation = "MONOCHROME2"
        ds.PixelRepresentation = 0
        ds.HighBit = 15
        ds.BitsStored = 16
        ds.BitsAllocated = 16
        ds.SmallestImagePixelValue = bytes((0,))
        ds.LargestImagePixelValue = bytes((255,))
        
        img = img.astype(np.uint16)
  
        print(np.amin(img))
        print(np.amax(img))
        
        ds.PixelData = img.tostring()
        ds.Rows = img.shape[0]
        ds.Columns = img.shape[1]


        print("Writing test file", output_file)
        ds.save_as(output_file)
        print("File saved.")
        
        return

# =========================================================================
# NOW WE TEST THE CLASS    
    
print("runing a test")

encoder = Dicom_Encoder()

encoder.encode("/home/alex/Pictures/Yes.jpg","this is a benign tumor", "/home/alex/Pictures/Yes.dcm")


# then read what we produced
print("read and output the created file")
dataset = dicom.read_file("/home/alex/Pictures/Yes.dcm")

print(dataset)

