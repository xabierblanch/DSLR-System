from time import sleep
import time
from datetime import datetime
from sh import gphoto2 as gp
import os
import dropbox
import RPi.GPIO as GPIO
import shutil
import subprocess

temps_inicial = time.time()

#########################################################################
#########################################################################

#IDENTIFICADOR DEL SISTEMA -> IMPORTANT CANVIAR-HO CORRECTAMENT

ID = "HRCam4_"

#PARÀMETRE CAPTURA (NUMERO DE CAPTURES A FER INSTANTANEAMENT)

captures = 4 

#########################################################################
#########################################################################

if ID == "HRCam1_":
    TOKEN = "TOKEN"
elif ID == "HRCam2_":
    TOKEN = "TOKEN"
elif ID == "HRCam3_":
    TOKEN = "TOKEN"
elif ID == "HRCam4_":
    TOKEN = "TOKEN"
elif ID == "HRCam5_":
    TOKEN = "TOKEN"

#print()
#print("*********************** UNIVERSITAT DE BARCELONA ***********************")
#print("******************** FACULTAT DE CIÈNCIES DE LA TERRA ******************")
#print()
#print("************************* XABIER BLANCH GORRIZ *************************")
#print("*********** Codi desenvolupat en el marc d'una tesi doctoral ***********")
#print("*************************** Codi multicàmera ***************************")
print()
print(datetime.now().strftime("Hora: %H:%M Data: %d/%m/%Y"))
print("Es realitzaran", captures, "captures fotogràfiques")
print()

arrel_directori_directe = "/home/pi/" + ID + "Puigcercos_filetransfer/"
path_directe = "/home/pi/" + ID + "Puigcercos_filetransfer"
arrel_directori_final = "/home/pi/" + ID + "Puigcercos/"
path_final = "/home/pi/" + ID + "Puigcercos"

gphoto2_ISO = ["--set-config", "iso=1"]
gphoto2_autodetect = ["--auto-detect"]
data_hora = datetime.now().strftime("%Y%m%d_%H%M")
gphoto2_focus_sony = ["--set-config", "/main/actions/autofocus=1"]
gphoto2_capture_download_sony = ["--capture-image-and-download"]
gphoto2_capture_download_canon = ["--capture-image", "-F=" + str(captures), "-I=3="]
gphoto2_borrarSD = ["--folder", "/store_00020001/DCIM/100CANON", "-R", "--delete-all-files"]
gphoto2_SD = ["--set-config", "capturetarget=1"]
gphoto2_descarregarSD = ["--get-all-files"]

count=1

def seleccio_camera():
    global script
    camera=str(subprocess.check_output(['gphoto2', '--auto-detect']))
    if camera.find("Sony Alpha-A7r II") > 0:
        script=1
        print("Càmera Sony Alpha-A7r II identificada correctament")
    elif camera.find("Canon EOS 600D") > 0:
        script=2
        print("Càmera Canon EOS 600D identificada correctament")
    elif camera.find("Canon EOS 77D") > 0:
        script=2
        print("Càmera Canon EOS 77D identificada correctament")

def directori():
    try:
        os.makedirs(arrel_directori_directe)
        print("Carpeta " + ID + "Puigcercos_filetransfer creada correctament")
        os.makedirs(arrel_directori_final)
        print("Carpeta " + ID + "Puigcercos creada correctament")
    except:
        print("Les carpetes " + ID + "Puigcercos i " + ID + "Puigcercos_filetransfer ja existeixen")

    os.chdir(arrel_directori_directe)

def captura_imatge_gphoto2_sony():
    try:
        gp(gphoto2_capture_download_sony)
        print("GPHOTO2 - Captura realitzada i descarregada")
        sleep(1)
    except:
        print("Error GPHOTO2 - Error en la captura de fotografies")

def focus_gphoto2_sony():
    try:
        gp(gphoto2_focus_sony)
        print("GPHOTO2 - Camera Sony enfocada correctament")
        sleep(2)
    except:
        print("Error GPHOTO2 - Camera no enfocada correctament")

def captura_imatge_gphoto2_canon():
    try:
        gp(gphoto2_SD)
        print("GPHOTO2 - SD Interna de la càmera seleccionada")
    except:
        print("Error GPHOTO2 - Error seleccionant la SD Interna de la càmera")

    try:
        gp(gphoto2_capture_download_canon)
        print("GPHOTO2 - " + str(captures) + " captures realitzades correctament")
        sleep(2)
    except:
        print("Error GPHOTO2 - Error en la captura de fotografies")

    try:
        gp(gphoto2_descarregarSD)
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
    print("No hi ha fitxers a la carpeta " + ID + "Puigcercos_filetransfer per pujar al Dropbox")
 else:
    for file in os.listdir(path_directe):
        f=open(arrel_directori_directe + file, 'rb')
        try:
           dbx = dropbox.Dropbox(TOKEN)
           res=dbx.files_upload(f.read(),'/' + file, mode=dropbox.files.WriteMode.overwrite)
           shutil.move(arrel_directori_directe + file, arrel_directori_final + file)
           print('fitxer', res.name, 'penjat correctament i mogut a la carpeta ' + ID + 'Puigcercos')
        except dropbox.exceptions.ApiError as err:
           print('*** API error', err)
           return none
    return res

def borrar_fitxers():
        data_actual = time.time()
        eliminats=0
        for fitxer in os.listdir(path_final):
            data_fitxer = os.path.getmtime(arrel_directori_final + fitxer)
            if ((data_actual - data_fitxer)/(24*3600))>=2:
                os.unlink(arrel_directori_final + fitxer)
                eliminats = eliminats + 1
                print("Fitxer " + fitxer + " eliminat correctament")

def borrar_error():
	for file in os.listdir(path_directe):
		if file[0:5] == "HRCam":
			print("Fitxer " + file + " pendent d'enviar")
		else:
			os.unlink(arrel_directori_directe + file)
			print("Fitxer " + file + " corrupte. Ha estat eliminat")

# SEQUENCIA DE FUNCIONS - PROGRAMA PRINCIPAL

data = time.localtime()
hora = data.tm_hour

if  hora > 6:
    print("** Inici seqüència fotogràfica **")
    borrar_error()
    sleep(2)
    print()
    directori()
    print()
    borrar_fitxers()
    print()
    sleep(2)
    print("** Identificació de la càmera **")
    print()
    script=0
    seleccio_camera()
    print()
    sleep(1)
    print("** Inici de la seqüència fotogràfica **")
    print()
    if script == 1:
        for count in range(1, captures+1):
                try:
                    focus_gphoto2_sony()
                    sleep(2)
                    captura_imatge_gphoto2_sony()
                    sleep(1)
                    canvi_nom(count)
                    sleep(1)
                except:
                    print("ERROR - Desconexió càmera")

    elif script == 2:
        try:
                gp(gphoto2_borrarSD)
                captura_imatge_gphoto2_canon()
                for count in range (1, captures+1):
                    canvi_nom(count)
                    sleep(1)
        except:
            print("ERROR - Desconexió càmera")
    sleep(1)
    print()
    print("** Seqüencia de captura fotogràfica finalitzada **")
    print()
    print("** Codi finalitzat correctament **")
    print()
    temps_final = time.time()
    temps_execucio = temps_final - temps_inicial
    print("Temps d'execució: " + str(round(temps_execucio)) + " segons")
    print("******************************************************************")
else:
    sleep(30)
    print('** Inici seqüència de càrrega **')
    borrar_error()
    try:
        print("** Inici de la seqüència de càrrega al Dropbox **")
        print()
        dropbox_upload()
        sleep(1)
    except:
        print("Error DROPBOX - Error en la càrrega de fitxers a Dropbox")
        print()
    print("** Codi finalitzat correctament **")
    print()
    temps_final = time.time()
    temps_execucio = temps_final - temps_inicial
    print("Temps d'execució: " + str(round(temps_execucio)) + " segons")
    print("******************************************************************")

