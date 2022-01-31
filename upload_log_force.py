import os
import dropbox

#########################################################################
#########################################################################

#IDENTIFICADOR DEL SISTEMA -> IMPORTANT CANVIAR-HO CORRECTAMENT

ID = "DSLR4_"

#########################################################################
#########################################################################

if ID == "DSLR1_":
    TOKEN = "TOKEN"
elif ID == "DSLR2_":
    TOKEN = "TOKEN"
elif ID == "DSLR3_":
    TOKEN = "TOKEN"
elif ID == "DSLR4_":
    TOKEN = "TOKEN"
elif ID == "DSLR5_":
    TOKEN = "TOKEN"

arrel_directori = '/home/pi/log_force/'

def dropbox_upload():
    
    for file in os.listdir('/home/pi/log_force'):
        f=open(arrel_directori + file, 'rb')
        try:
           dbx = dropbox.Dropbox(TOKEN)
           res=dbx.files_upload(f.read(),'/log/' + file, mode=dropbox.files.WriteMode.overwrite)
           print('log', res.name, 'penjat correctament')
        except dropbox.exceptions.ApiError as err:
           print('*** API error', err)
           return none
    
dropbox_upload()
    
