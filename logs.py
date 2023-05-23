import os
import dropbox
import shutil

#DROPBOX USER INFORMATION (check official Dropbox API)

app_key = ''
app_secret = ''
refresh_token = '' #https://github.com/dropbox/dropbox-sdk-python/blob/main/example/oauth/commandline-oauth.py

#############################################################

def dropbox_upload(app_key, app_secret, refresh_token, path):
    """
    Upload files from the specified path to Dropbox.

    Args:
        app_key (str): Dropbox app key.
        app_secret (str): Dropbox app secret.
        refresh_token (str): Dropbox refresh token.
        path (str): Path to the folder containing the files to upload.
    """
	for file in os.listdir(path):
        	f=open(os.path.join(path,file), 'rb')
        	try:
           		dbx = dropbox.Dropbox(app_key=app_key, app_secret=app_secret, oauth2_refresh_token=refresh_token)
           		res=dbx.files_upload(f.read(),'/log/' + file, mode=dropbox.files.WriteMode.overwrite)
           		print('log', res.name, 'loaded to Dropbox')
        	except dropbox.exceptions.ApiError as err:
           		print('*** API error', err)
           		return none

def copylogs(path):
    """
    Copy the WittyPi log file to the specified path.

    Args:
        path (str): Destination path for the log file.
    """
	try:
		shutil.copyfile('/home/pi/wittypi/wittyPi.log', os.path.join(path, 'wittyPi.log'))
		print('WittyPi log moved to log folder')
	except:
		print('ERROR: WittyPi log files')
		
# Define the path where the logs will be stored
path = '/home/pi/logs'

# Copy the WittyPi log file to the specified path
copylogs(path)

# Upload the log files to Dropbox
dropbox_upload(app_key, app_secret, refresh_token, path)
