''' To execute this code, you need to complete the following steps:
Install the required libraries: Make sure you have installed the necessary libraries, including gphoto2, dropbox, and any other dependencies.
Obtain a Dropbox token: You need to generate a Dropbox token to authorize the script to upload files to your Dropbox account.
You can obtain a token by creating a Dropbox app and following the authentication process. Once you have the token, replace the empty string TOKEN = "" with your actual token.
Configure other parameters: You may need to adjust other parameters such as the number of captures, file paths, and camera settings based on your specific requirements.

Once you have completed these steps, you can run the script, and it will perform the following actions:
1 - Identify the cameras connected to the system.
2 - Create the necessary folders for file transfer and backup.
3 - Capture images using either the Sony or Canon camera (based on the identified camera).
4 - Rename the captured files based on the capture count.
5 - Upload the files to Dropbox using the provided token.
6 - Move the uploaded files to the backup folder.
7 - Delete files older than 2 days from the backup folder.

Please ensure that you have a clear understanding of the code and customize it according to your needs before running it.
Also, remember to handle any potential errors or exceptions that may occur during the execution. '''

from time import sleep
import time
from datetime import datetime
from sh import gphoto2 as gp
import os
import dropbox
import shutil
import subprocess

temps_inicial = time.time()

#########################################################################
#########################################################################

#SYSTEM IDENTIFIER -> IMPORTANT TO CHANGE IT CORRECTLY

ID = "DSLR_"

#DROPBOX USER INFORMATION (check official Dropbox API)

app_key = ''
app_secret = ''
refresh_token = '' #https://github.com/dropbox/dropbox-sdk-python/blob/main/example/oauth/commandline-oauth.py

#CAPTURE NUMBER (NUMBER OF INSTANTANEOUS CAPTURES TO BE ACQUIRED)

captures = 4 

#########################################################################
#########################################################################

print("*********************** UNIVERSITY OF BARCELONA ***********************")
print("******************** FACULTY OF EARTH SCIENCES ******************")
print()
print("************************* XABIER BLANCH GORRIZ *************************")
print("*********** Code developed within the framework of a doctoral thesis ***********")
print("*************************** Multi-camera code ***************************")
print()
print(datetime.now().strftime("Time: %H:%M Date: %d/%m/%Y"))
print("A total of", captures, "photographic captures will be performed.")
print()

path_filetransfer = "/home/pi/" + ID + "_filetransfer"
path_backup = "/home/pi/" + ID

gphoto2_ISO = ["--set-config", "iso=1"]
gphoto2_autodetect = ["--auto-detect"]
date_time = datetime.now().strftime("%Y%m%d_%H%M")
gphoto2_focus_sony = ["--set-config", "/main/actions/autofocus=1"]
gphoto2_capture_download_sony = ["--capture-image-and-download"]
gphoto2_capture_download_canon = ["--capture-image", "-F=" + str(captures), "-I=3="]
gphoto2_SD_Erase = ["--folder", "/store_00020001/DCIM/100CANON", "-R", "--delete-all-files"]
gphoto2_SD = ["--set-config", "capturetarget=1"]
gphoto2_SD_Transfer = ["--get-all-files"]

count=1

# Function to select the camera based on the output of the 'gphoto2 --auto-detect' command
def select_camera():
    """
    Selects the camera based on the output of the 'gphoto2 --auto-detect' command.
    Sets the global variable 'script' according to the identified camera.
    Prints the identification message for the selected camera.
    """
    	global script
    	camera=str(subprocess.check_output(['gphoto2', '--auto-detect']))
    	if camera.find("Sony Alpha-A7r II") > 0:
        	script=1
        	print("The Sony Alpha A7R II camera has been correctly identified")
    	elif camera.find("Canon EOS 600D") > 0:
	        script=2
        	print("Canon EOS 600D camera correctly identified")
    	elif camera.find("Canon EOS 77D") > 0:
        	script=2
        	print("Canon EOS 77D camera correctly identified")

# Function to create necessary folders for file transfer and backup
def folders():
    """
    Creates the necessary folders for file transfer and backup.
    If the folders already exist, it prints a message indicating their existence.
    """
    	try:
        	os.makedirs(path_filetransfer, exist_ok = True)
        	print("Folder " + ID + "_filetransfer created successfully")
        	os.makedirs(path_backup, exist_ok = True)
        	print("Folder " + ID + "created successfully")
    	except:
        	print("Folders " + ID + " and " + ID + "_filetransfer already exist")

    	os.chdir(path_filetransfer)

# Function to capture an image using Sony camera with gphoto2
def capture_gphoto2_sony():
    """
    Captures an image using the Sony camera with the 'gphoto2' command.
    If the capture is successful, it prints a success message.
    If there is an error in the capture acquisition, it prints an error message.
    """
    	try:
        	gp(gphoto2_capture_download_sony)
        	print("GPHOTO2 - Capture completed and downloaded.")
        	sleep(1)
    	except:
	        print("Error GPHOTO2 - Error in the capture adquisition")
	
# Function to activate auto-focus on Sony camera with gphoto2
def focus_gphoto2_sony():
    """
    Activates the auto-focus on the Sony camera with the 'gphoto2' command.
    If the auto-focus activation is successful, it prints a success message.
    If there is an error in focusing the camera, it prints an error message.
    """
	try:
    		gp(gphoto2_focus_sony)
        	print("GPHOTO2 - Camera Sony auto focus activated")
        	sleep(2)
    	except:
	        print("Error GPHOTO2 - Camera not focused")
	
# Function to capture images using Canon camera with gphoto2
def capture_gphoto2_canon():
    """
    Captures images using the Canon camera with the 'gphoto2' command.
    If the internal SD card of the camera is selected successfully, it prints a success message.
    If the capture is successful, it prints the number of captures taken.
    If there is an error in capturing photos or downloading them, it prints an error message.
    """
    	try:
        	gp(gphoto2_SD)
        	print("GPHOTO2 - Internal SD card of the selected camera")
    	except:
	        print("Error GPHOTO2 - Error selecting the internal SD card of the camera")

    	try:
        	gp(gphoto2_capture_download_canon)
        	print("GPHOTO2 - " + str(captures) + " captures successfully taken")
        	sleep(2)
    	except:
        	print("Error GPHOTO2 - Error in capturing photos")

    	try:
	        gp(gphoto2_SD_Transfer)
        	print("GPHOTO2 - " + str(captures) + " captures successfully downloaded")
    	except:
	        print("Error GPHOTO2 - Error in downloading photos")
	
# Function to rename files based on capture count
def file_name(count):
    """
    Renames files in the file transfer folder based on the capture count.
    Each file is renamed using the pattern: "{ID}{data_hora}_{count}.JPG"
    Prints a success message for each file successfully renamed.
    """
     	for file in os.listdir(path_filetransfer):
        	if len(file) < 20:
                	os.rename(os.path.join(path_filetransfer, file), os.path.join(path_filetransfer, ID + date_time + "_" + str(count) + ".JPG"))
                	print("File", file, "successfully modified to " + ID + date_time + "_" + str(count) + ".JPG")
                	count=count+1
		
# Function to upload files to Dropbox
def dropbox_upload():
    """
    Uploads files from the filetransfer folder to Dropbox.
    If there are no files to upload, it prints a message indicating the absence of files.
    For each file, it uploads the file to Dropbox and moves it to the backup folder.
    Prints a success message for each file successfully uploaded and moved.
    If there is an API error during the upload process, it prints an error message.
    Args:
	app_key (str): Dropbox app key.
	app_secret (str): Dropbox app secret.
	refresh_token (str): Dropbox refresh token.  
    """
	if os.listdir(path_filetransfer) == []:
		print("There are no files in the " + ID + "Puigcercos_filetransfer folder to upload to Dropbox.")
 	else:
    		for file in os.listdir(path_filetransfer):
        	f=open(os.path.join(path_filetransfer, file), 'rb')
        	try:
           		dbx = dropbox.Dropbox(app_key=app_key, app_secret=app_secret, oauth2_refresh_token=refresh_token)
           		res=dbx.files_upload(f.read(),'/' + file, mode=dropbox.files.WriteMode.overwrite)
           		shutil.move(os.path.join(path_filetransfer, file), os.path.join(path_backup, file))
           		print('File ', res.name, 'uploaded successfully and moved to the folder ' + ID + 'Puigcercos.')
        	except dropbox.exceptions.ApiError as err:
           		print('*** API error', err)			
			
# Function to delete files older than 2 days from the backup folder
def clear_files():
    """
    Deletes files older than 2 days from the backup folder.
    Prints a success message for each file successfully deleted.
    """
        date_time = time.time()
        count=0
        for file in os.listdir(path_backup):
        	date_file = os.path.getmtime(os.path.join(path_backup, file))
            	if ((date_time - date_file)/(24*3600))>=2:
                	os.unlink(os.path.join(path_backup, file))
                	count = count + 1
                	print("File " + file + " deleted successfully.")
		
# Function to clear error images from file transfer folder
def clear_error_img():
    """
    Clears error images from the file transfer folder.
    Identifies error images based on the file name starting with "DSLR_".
    Deletes the error images and prints a message for each deleted file.
    """
	for file in os.listdir(path_filetransfer):
		if file[0:5] == "DSLR_":
			print("File " + file + " pending to send.")
		else:
			os.unlink(os.path.join(path_backup, file))
			print("File " + file + " corrupted. It has been deleted.")

# Main code
print("** Start of photographic sequence **")
clear_error_img()
sleep(2)
print()
folders()
print()
clear_files()
print()
sleep(2)
print("** Camera identification **")
print()
script=0
select_camera()
print()
sleep(1)
print("** Start of the photographic sequence **")
print()
if script == 1:
	for count in range(1, captures+1):
        	try:
                    focus_gphoto2_sony()
                    sleep(2)
                    capture_gphoto2_sony()
                    sleep(1)
                    file_name(count)
                    sleep(1)
                except:
                    print("ERROR - Camera disconnected")

elif script == 2:
	try:
                gp(gphoto2_SD_Erase)
                capture_gphoto2_canon()
                for count in range (1, captures+1):
                    file_name(count)
                    sleep(1)
        except:
        	print("ERROR - Camera disconnected")
sleep(1)
print()
print("** Photographic capture sequence completed **")
print()
try:
	print("** Start of the Dropbox upload sequence **")
    	print()
    	dropbox_upload()
    	sleep(1)
except:
	print("DROPBOX Error - Error uploading files to Dropbox")
    	print()
	
print("** Code executed successfully **")
print()
print("******************************************************************")
