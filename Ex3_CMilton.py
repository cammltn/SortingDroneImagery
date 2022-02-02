# Camille Milton
# GEOG 666
# Exercise 3 - Metadata
# 11 July 2021

import os
import exifread
from datetime import datetime
import shutil



# Take directory path from user
user_input = raw_input("Enter directory path: ")

# Check if directory path exists
assert os.path.exists(user_input), "Could not find the path: " + str(user_input)

# Set and confirm directory path with user
os.chdir(user_input)
print("Current working directory: ", os.getcwd())


# Set permissions to allow new folders to be made in the directory
os.chmod(user_input, 0o777)


# Iterate through the images in the input directory
f = []
for subdir, dirs, files in os.walk(user_input):
    f.extend(files)

print(f)


# Read image metadata and check when images were captured
def image_date(user_input):
    # Read file
    open_file = open(user_input, 'rb')

    # Check exif Image Datetime for each file
    exif = exifread.process_file(open_file, stop_tag='Image DateTime')

    try:
        # Get the date taken
        datetaken_string = exif['Image DateTime']
        datetaken_object = datetime.datetime.strptime(datetaken_string.values, '%Y:%m:%d %H:%M:%S')

        # Date
        day = str(datetaken_object.day).zfill(2)
        month = str(datetaken_object.month).zfill(2)
        year = str(datetaken_object.year)
        # Time
        second = str(datetaken_object.second).zfill(2)
        minute = str(datetaken_object.minute).zfill(2)
        hour = str(datetaken_object.hour).zfill(2)

        # New Filename
        output = [day,month,year,day + month + year + '-' + hour + minute + second]
        return output

    except:
        return None

# Compare images and put into new folders

# Process all images in the directory and put into new folders for each test flight based on the threshold of
# the time (hour/min) the image was captured based on image datetime returned
for file in os.listdir(user_input):
    if file.endswith('.jpg'):
        filename = user_input + os.sep + file
        dateinfo = date_taken_info(filename)
        try:
            out_filepath = user_input + os.sep + 'Flight_on_' + dateinfo[3] + dateinfo[2] + dateinfo[1] + dateinfo[4] + dateinfo[5]
            out_filename = out_filepath  + os.sep + dateinfo[4] + dateinfo[5] + dateinfo[6] '.jpg'

            # check if destination path
            if not os.path.exists(out_filepath):
                os.makedirs(out_filepath)

            # copy the images to the new destination folder
            shutil.copy2(filename, out_filename)

            # check that the images are the same then remove the image from the old folder
            if hash_file(filename) == hash_file(out_filename):
                print 'File copied with success to ' + out_filename
                os.remove(filename)
            else:
                print 'File failed to copy :( ' + filename

        except:
            print 'File has no exif data skipped ' + filename

