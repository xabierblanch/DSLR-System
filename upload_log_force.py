import os
import dropbox

#########################################################################
#########################################################################

#IDENTIFICADOR DEL SISTEMA -> IMPORTANT CANVIAR-HO CORRECTAMENT

ID = "DSLR4_"

#########################################################################
#########################################################################

if ID == "DSLR1_":
    TOKEN = "PxYI5GpMD2AAAAAAAAAAC_Irv5v9nzqH-yZGiooAvB3fXCi2vnU99m0FsiLugqSr"
elif ID == "DSLR2_":
    TOKEN = "PxYI5GpMD2AAAAAAAAAADBloxEwqqZcUrKCiApOU0ryUnNvpkqdqEO8C5AYWeELC"
elif ID == "DSLR3_":
    TOKEN = "PxYI5GpMD2AAAAAAAAAADzIq3myXVj61QtmjBhbTugAQdRv2loSpBJ1nD5lRjrjr"
elif ID == "DSLR4_":
    TOKEN = "PxYI5GpMD2AAAAAAAAAADcZ4K-7-jssfEQUK5QX_gQY0bflC1KVsxhJ-gOPlfpWn"
elif ID == "DSLR5_":
    TOKEN = "PxYI5GpMD2AAAAAAAAAADlJQoaG68X7IO8I5q5doN4scX6B6sEpDf7oH4GbaiHGS"

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
    
