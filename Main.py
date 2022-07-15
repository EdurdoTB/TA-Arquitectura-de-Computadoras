import cv2 
import numpy as np
import time
import os
import csv
import tkinter as tk
from tkinter import *
import ctypes
from threading import Thread
from multiprocessing import Pool, cpu_count,current_process


## PARA QUE PUEDA UTILIZAR EL ARCHIVO AÑADA EN LA VARIABLE "archivo_fotos" la direccion en donde se encuentre este archivo + "/fotos"

#Variables Globales
registro_Negro = []
registro_Amarillo = []
registro_Amarillo_para_c_assembler=[]
area_Yellow=[]
area_Black=[]
i=1
foto = 0
Valido1 = 0
Valido2 = 0
Porcentaje_Amarillo = []
Porcentaje = []

archivo_fotos= "/home/sebastian/ArquitecturaDeComputadora/Prueba/fotos"

if not os.path.exists(archivo_fotos):
    os.makedirs(archivo_fotos)

#Funcion que almacena en la carpeta fotos las capturas realizadas al presionar la letra "a"
#Para terminar la función se usa la letra "s"

def tomar_foto():
    global foto
    cap=cv2.VideoCapture(0)

    while True:
        ret,frame=cap.read()
        if ret==True:
            cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF ==ord('s'):
            print("Se presionó la letra S")
            break
        if cv2.waitKey(1) & 0xFF ==ord('a'):
            cv2.imwrite(archivo_fotos+f'/foto{foto}.jpg',frame)
            print(f"Se almacenó la foto{foto}")
            foto+=1
          
    cap.release()
    cv2.destroyAllWindows()

#Funcion que 

def DetectarColores(imagenes):
    global foto
    global area_amarilla
    global area_negra
    global i
    global Porcentaje_Amarillo
    global Porcentaje
    file_names=os.listdir(archivo_fotos)
    for file_name in file_names:
        image_path=imagenes+"/"+file_name
        image = cv2.imread(image_path)
        image1=image
        # Se convierte la imagen RGB a HSV
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        # Se define un intervalo del color amarillo en HSV dependiendo de la iluminacion en la que se enceuntre el usuario
        yellowBajo=np.array([13,95,20],np.uint8)
        yellowAlto=np.array([45,255,200],np.uint8)

        # Se define un intervalo del color negro en HSV
        blackLow=np.array([0,100,20],np.uint8)
        blackUp=np.array([180,255,142],np.uint8)

        # Se genera las mascaras de los colores amarillo y negro
        maskYellow = cv2.inRange(hsv, yellowBajo, yellowAlto)
        maskBlack = cv2.inRange(hsv, blackLow, blackUp)

        contornos_yellow,_= cv2.findContours(maskYellow, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contornos_black,_=cv2.findContours(maskBlack, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        area1=0
        area2=0
        #Para cada contorno amarillo se halla su área y la suma se almacena en area_amarilla
        for c in contornos_yellow:
            area1=cv2.contourArea(c)
            area1+=area1
        area_amarilla=area1
        print("Area amarilla",area_amarilla)        
        #Para cada contorno negro se halla su área y la suma se almacena en area_negra
        for d in contornos_black:
            area2=cv2.contourArea(d)
            area2+=area2
        area_negra=area2
        print("Area Negra",area_negra)
        Porcentaje_Amarillo.append(f"{lib.registro_area(area_amarilla,area_negra)} %")
        Porcentaje.append(lib.registro_area(area_amarilla,area_negra))
        print("El porcentaje de amarillo es",Porcentaje_Amarillo)
        print("++++++++++++++++")   
        registro_Negro.append(f"{area_negra}")
        registro_Amarillo_para_c_assembler.append(f"{area_amarilla}")
        registro_Amarillo.append(f"Muestra {i} {area_amarilla}")
        i+=1
        # Se muestra en pantalla las mascaras y la imagen con los contornos hallados 
        
        cv2.drawContours(image,contornos_yellow,-1,(0,255,255),5)
        cv2.drawContours(image1,contornos_black,-1,(0,0,0),2)
        cv2.imshow('imagen',image)
        cv2.waitKey(0)
        cv2.imshow('mascara amarilla',maskYellow)
        cv2.waitKey(0)
        cv2.imshow('mascara negra',maskBlack)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


### FUNCIONES QUE SERÁN USADAS AL HACER CLICK EN SUS BOTONES CORRESPONDIENTES ###
# En estos parametros se define también el tipo de letra, tamaño y la posición dondé se imprimirá el resultado


# Funcion para bloquear el acceso a usuarios que no esten dentro de la lista de nombres permitidos.
def Iniciar_sesion():

    global Valido1,Valido2
    answer = tk.Label(ventana, font=("Consolas", 14))
    answer.place(x=300, y=70)
    answer2 = tk.Label(ventana, font=("Consolas", 10))
    answer2.place(x=220,y=70)
    nombres_permitidos=["ricardo","marcelo","eduardo","sebastian"]
    profesores = ["stefano","enrique","jorge","benavides"]
    usuario_ingresado = txtusuario.get()
    usuario_ingresado = usuario_ingresado.encode('utf-8')
    
    for i in range(len(nombres_permitidos)):
        usuario_permitidos = nombres_permitidos[i]
        profesor = profesores[i]

        usuario_permitidos = usuario_permitidos.encode('utf-8')
        profesor = profesor.encode('utf-8')

        Valido1 = lib.validar(usuario_permitidos,usuario_ingresado)
        Valido2 = lib.validar(usuario_ingresado,profesor)
        if (Valido1 == 1):
            answer.config(text= "Hola "+f"{usuario_permitidos.decode('utf-8')}"+" buen día")
            break
        elif (Valido2 ==1):
            answer2.config(text= "Hola "+"profesor "f"{profesor.decode('utf-8')}"+" como está, mucho gusto")
            break
        else:
            answer.config(text = "Usuario incorrecto")   
            
#Funcion para tomar las fotos siempre y cuando se halla ingresado un usuario válido  
def Escanear():
    global usuario_value
    
    if(Valido1==1 or Valido2 ==1) :
        lblEscanear = tk.Label(ventana, text="ESCANEANDO",font=("Consolas", 10)).place(x=10, y=150) 
        tomar_foto()
    else:
        lblEscanear = tk.Label(ventana, text="INGRESE UN USUARIO VALIDO",font=("Consolas", 10)).place(x=10, y=150) 

#Funcion para calcular las áreas que se encuentren almacenadas en el directorio "/fotos" siempre y cuando se halla ingresado un usuario válido
def Calcular_Area():
    global Valido1, Valido2
    
    if(Valido1==1 or Valido2 ==1) :
        lblCalcArea = tk.Label(ventana, text="Calculando el área",font=("Consolas", 14)).place(x=15, y=150)       
        DetectarColores(archivo_fotos)

    else :
        lblEscanear = tk.Label(ventana, text="INGRESE UN USUARIO VALIDO",font=("Consolas", 10)).place(x=10, y=150) 
        
#Funcion para registrar los datos recopilados de la funcion "Calcular_Area()" en un archivo .csv 
def Registro(imagenes):
    global area_negra
    global area_amarilla
    global registro_absoluto
    global i
    global Porcentaje_Amarillo
    file_names=os.listdir(imagenes)
    lblregistro = tk.Label(ventana,text= "Las areas han sido registradas ",font=("Consolas", 14)).place(x=10, y=200) 
    
    print("El registro de areas negras es : ",registro_Negro)
    print("El registro de areas amarillas es : ",registro_Amarillo)
    
    headers = ('Numero de Muestras','Areas Amarillas', 'Areas Negras','Porcentaje de amarillo','Estado de maduracion')
    Maduro = []
    element = 0
    for element in range(len(Porcentaje)):
        if float(Porcentaje[element]) <= 20:
            Maduro.append("Demasiado maduro")
        elif float(Porcentaje[element]) <= 50 and float(Porcentaje[element]) > 20:
            Maduro.append("Muy maduro")
        elif float(Porcentaje[element]) <= 80 and float(Porcentaje[element]) > 50:
            Maduro.append("Maduro")
        else:
            Maduro.append("apenas maduro")

        
    registro_absoluto = zip(registro_Amarillo,registro_Negro,Porcentaje_Amarillo,Maduro)

    with open('tabla.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        for row in registro_absoluto:
            writer.writerow(row)
 
    area_negra = 0 
    area_amarilla = 0

def Reg_IMG():
    Registro(archivo_fotos)

def abrir():
    print ("hiciste clic en abrir")
    venabrir=Tk()
    venabrir.geometry("400x200+200+200")
    venabrir.title("otra ventana")
    venabrir.mainloop()
#Menu de Instrucciones que darán a conocer la secuencia de pasos para poder analizar sus fotos 
def instrucciones():
    print ("hiciste clic en instrucciones")

    txt = "Paso1: Ingresar un usuario válido.\n \nPaso2: Al dar clic en \"Escanear\" se abrirá una ventana que activará su camara automaticamente.\n \nPaso 3: Enfoque su platano en un fondo diferente al color amarillo y negro. \n\n Paso 4: Presione la letra \"a\" para capturar las fotos y la letra \"s\" para apagar su cámara.\n \nPaso 5: Una vez que tenga las fotos que desee analizar haga click en Calcular Area.\n \nPaso 6: Se mostrará en pantalla las áreas halladas(puede cambiar de imagen presionando cualquier tecla), estas dependeran de una buena iluminacion y resolución de su cámara.\n \nPaso 7: Haga click en \"Registrar las áreas\" para poder crear un archivo .csv indicando el porcentaje y el estado de madurez que presenta el plátano."   
    lblregistro = tk.Label(ventana,text=  f"{txt}",font=("Consolas",11)).place(x=0, y=200) # Definir los valores a imprimir cuando se presione el boton de Calcular Area

#Funcion Principal 
if __name__ == "__main__" : 

    #Uso de Ctypes para realizar funciones en lenguaje C 
    
    lib = ctypes.CDLL('./validacion.so')
    lib.validar.argtypes = [ctypes.c_char_p,ctypes.c_char_p]
    lib.validar.restype = ctypes.c_int
    lib.registro_area.argtypes = [ctypes.c_float,ctypes.c_float]
    lib.registro_area.restype = ctypes.c_float

    ventana = tk.Tk()
    ventana.geometry("500x300+100+200") # Geometria de la ventana
    ventana.title("Detector del estado de platanos") # Nombre de la interface

    lblusuario1 = tk.Label(text="Usuario", fg="black", font=("Consolas",14)).place(x=10,y=50) # Ponet la palabra usuario en el formulario
    usuario = tk.StringVar() # Creando cuadro de texto para campo de respuesta
    txtusuario = tk.Entry(ventana)
    txtusuario.place(x=90,y=55) # Tamaña del cuadro de texto
    Fruta = tk.StringVar()

    #Creacion de los botones a utilizar 
    
    btnsaludar = tk.Button(ventana,text="Iniciar Sesión",command=Iniciar_sesion,font=("Agency FB",14)).place(x=270,y=20) # Creación del boton saludar 
    btEscanear = tk.Button(ventana,text="Escanear",command=Escanear,font=("Agency FB",14)).place(x=40,y=100) # Creación del boton saludar 
    btCalcArea = tk.Button(ventana,text="Calcular Area",command=Calcular_Area,font=("Agency FB",14)).place(x=150,y=100) # Creación del boton saludar 
    btnsRegistro= tk.Button(ventana,text="Registrar las áreas",command=Reg_IMG,font=("Agency FB",14),).place(x=290,y=100) # Creación del boton despedir

    ventana.geometry("600x600+100+100")

    #Se crea la barra de menus
    barramenu=Menu(ventana)

    mnuarchivo=Menu(barramenu)

    #Se crean los comandos de los menus

    mnuarchivo.add_command(label="Instrucciones",command=instrucciones)
    mnuarchivo.add_separator() # Hacer una divición en el menú
    mnuarchivo.add_command(label="Salir",command=ventana.destroy)

    #Se agergan los menus a la barra de menus
    barramenu.add_cascade(label="Archivo",menu=mnuarchivo)
    
    #Se posiciona la barra de menus en la ventana
    ventana.config(menu=barramenu)
    ventana.mainloop() # Mostrar ventana
