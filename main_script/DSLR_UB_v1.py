from time import sleep
import time
from datetime import datetime
from sh import gphoto2 as gp
import os
import dropbox
import shutil
import subprocess
from subprocess import call

temps_inicial = time.time()

#########################################################################
#########################################################################

#IDENTIFICADOR DEL SISTEMA -> IMPORTANT CANVIAR-HO CORRECTAMENT

ID = "DSLR4_"

#PARÀMETRE CAPTURA (NUMERO DE CAPTURES A FER INSTANTANEAMENT)

captures = 3

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

print()
print("*********************** UNIVERSITAT DE BARCELONA ***********************")
print("******************** FACULTAT DE CIÈNCIES DE LA TERRA ******************")
print("************************* XABIER BLANCH GORRIZ *************************")
print("*********** Codi desenvolupat en el marc d'una tesi doctoral ***********")
print()
print(datetime.now().strftime("Hora: %H:%M Data: %d/%m/%Y"))
print("Es realitzaran", captures, "captures fotogràfiques")
print()

arrel_directori_directe = "/home/pi/" + ID + "Alhambra_filetransfer/"
path_directe = "/home/pi/" + ID + "Alhambra_filetransfer"
arrel_directori_final = "/home/pi/" + ID + "Alhambra/"
path_final = "/home/pi/" + ID + "Alhambra"

gphoto2_ISO = ["--set-config", "iso=1"]
gphoto2_autodetect = ["--auto-detect"]
data_hora = datetime.now().strftime("%Y%m%d_%H%M")
gphoto2_capture_download_nikon = ["--capture-image", "-F=" + str(captures), "-I=1="]
gphoto2_borrarSD = ["--folder", "/store_00010001/DCIM/100ND610", "-R", "--delete-all-files"]
gphoto2_SD = ["--set-config", "capturetarget=1"]
gphoto2_descarregarSD = ["--get-all-files"]

count=1

def directori():
    try:
        os.makedirs(arrel_directori_directe)
        os.makedirs(arrel_directori_final)
    except:
        print("Les carpetes " + ID + "Alhambra i " + ID + "Alhambra_filetransfer ja existeixen")

    os.chdir(arrel_directori_directe)

def captura_imatge_gphoto2():
	try:
		gp(gphoto2_SD)
		print("GPHOTO2 - SD Interna de la càmera seleccionada")
	except:
		print("Error GPHOTO2 - Error seleccionant la SD Interna de la càmera")

	try:
		sleep(1)
		gp(gphoto2_capture_download_nikon)
		sleep(1)
		print("GPHOTO2 - " + str(captures) + " captures realitzades correctament")
	except:
		print("Error GPHOTO2 - Error en la captura de fotografies")

	try:
		sleep(1)
		gp(gphoto2_descarregarSD)
		sleep(1)
		print("GPHOTO2 - " + str(captures) + " captures descarregades correctament")
	except:
		print("Error GPHOTO2 - Error en la descarrega de fotografies")

def canvi_nom(count):
     for file in os.listdir(path_directe):
            if len(file) < 20:
                os.rename(arrel_directori_directe + file, arrel_directori_directe + ID + data_hora + "_" + str(count) + ".JPG")
                print("Nom del fitxer", file, "canviat correctament a " + ID + data_hora + "_" + str(count) + ".JPG")
                count=count+1

def dropbox_upload():
	if os.listdir(path_directe) == []:
		print("No hi ha fitxers a la carpeta " + ID + "Alhambra_filetransfer per pujar al Dropbox")
	else:
		for file in os.listdir(path_directe):
			f=open(arrel_directori_directe + file, 'rb')
			try:
				dbx = dropbox.Dropbox(TOKEN)
				res=dbx.files_upload(f.read(),'/' + file, mode=dropbox.files.WriteMode.overwrite)
				shutil.move(arrel_directori_directe + file, arrel_directori_final + file)
				print('fitxer', res.name, 'penjat correctament i mogut a la carpeta ' + ID + 'Alhambra')
			except dropbox.exceptions.ApiError as err:
				print('*** API error', err)
				return none
		return res

def borrar_fitxers():
	data_actual = time.time()
	eliminats=0
	for fitxer in os.listdir(path_final):
		data_fitxer = os.path.getmtime(arrel_directori_final + fitxer)
		if ((data_actual - data_fitxer)/(24*3600))>=15:
			os.unlink(arrel_directori_final + fitxer)
			eliminats = eliminats + 1
	print("S'han eliminat " + str(eliminats) + " fitxers per alliberar espai a la targeta de memòria")

# SEQUENCIA DE FUNCIONS - PROGRAMA PRINCIPAL

directori()
print()
borrar_fitxers()
print()
sleep(2)
try:
	gp(gphoto2_borrarSD)
	captura_imatge_gphoto2()
	for count in range (1, captures+1):
		canvi_nom(count)
except:
        print("ERROR - Conexió càmera")
sleep(2)
gp(gphoto2_borrarSD)
sleep(2)
print()
sleep(5)
try:
	print()
	dropbox_upload()
except:
	print("Error DROPBOX - Error en la càrrega de fitxers a Dropbox")
	print("En 30 segons es tornarà a intentar carregar els fitxers")
	sleep(30)
	print("Provant de carregar de nou")
	dropbox_upload()
print()
print("Codi finalitzat correctament")
print()
temps_final = time.time()
temps_execucio = temps_final - temps_inicial
print("Temps d'execució: " + str(round(temps_execucio)) + " segons")
print()
print("__________________________________________________________________________")
