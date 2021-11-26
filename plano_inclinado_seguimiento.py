# **********************************************************************
#
# PROYECTO CAPSTONE - DIPLOMADO EN IoT de Samsuung Innovation Campus
#
#     - Programa BASE (borrador) para seguimiento de una canica
#       sobre un plano inclinado
#
#       Eduardo Rodriguez
#       Fernando Ramírez
#
#                               26 de noviembre del 2021
#
# ***********************************************************************
# Programa basado en la aplicación:
#   > pymagesearch - Ball Tracking < de Adrian Rosebrock
#   > https://www.pyimagesearch.com/2015/09/14/ball-tracking-with-opencv/
# ***********************************************************************

# -----------------------------------------------------------------------
#        Bibliotecas utilizadas
# -----------------------------------------------------------------------
from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time
import math
import matplotlib.pyplot as plt

# -----------------------------------------------------------------------
# Establecimiento de los rangos de color de la canica de prueba en el
#                       espacio de color HSV
# -----------------------------------------------------------------------
# Se proponen varios grupos para diferentes colores de canicas. En 
#       principio se estará utilizando el color "amarillo"
# -----------------------------------------------------------------------

# ------------
#    VERDE
# ------------
#greenLower = (29, 86, 6)
#greenUpper = (64, 255, 255)
#colorLower = greenLower
#colorUpper = greenUpper

# ------------
#     AZUL
# ------------
#blueLower = (110, 50, 9)
#blueUpper = (120, 255, 255)
#colorLower = blueLower
#colorUpper = blueUpper

# ------------
#     ROJO
# ------------
#redLower = (1, 86, 6)
#redUpper = (10, 255, 255)
#colorLower = redLower
#colorUpper = redUpper

# ------------
# ROJO OSCURO
# ------------
#redLower = (4, 86, 6)
#redUpper = (10, 255, 100)
#colorLower = redLower
#colorUpper = redUpper

# ------------
#   AMARILLO
# ------------
yelowLower = (25, 68, 6)
yelowUpper = (35, 255, 155)
colorLower = yelowLower
colorUpper = yelowUpper

# -----------------------------------------------------------------------
# Definición de una "cola" (array) de dos posiciones para identificar el 
# movimiento de la canica cuando las dos localidades presentan un valor 
#       diferente en las coordenadas de posición de esta
# -----------------------------------------------------------------------
# --- Tamaño de la "cola" (array) ---
buffer = 2
pts = deque(maxlen=buffer)

# -----------------------------------------------------------------------
# Definición de un arreglo de diccionarios de posiciones instantáneas:
# pos = {"xy":(x, y), "center":center}
#        coordenadas      centro de
#         posicion           masa
#          canica
# -----------------------------------------------------------------------
pos = {}

# ----------------------------------------------------------------------
# Definición de un arreglo de diccionarios que contienen información
# completa de posiciones instantáneas, distancia instantánea recorrida
#               y marcas de tiempo correspodnientes:
#
# dic = {"xm0":xm0,"ym0":ym0,"xm1":xm1,"ym1":ym1,"dm":dm,
#        "xn0":xn0,"yn0":yn0,"xn1":xn1,"yn1":yn1,"dn":dn,
#        "frame":cont_frame,"t":t}
# ---------------------------------------------------------------------
# --- Arreglo de diccionarios ---
info = []
# --- Diccionario ---
dic = {}

# -----------------------------------------------------------------------
#       Inicializa la cámara web
# -----------------------------------------------------------------------
vs = cv2.VideoCapture(0)
# --- Delay para estabilizar la cámara ---
time.sleep(2.0) 

# -----------------------------------------------------------------------
#    Variables para manejo de tiempo
# -----------------------------------------------------------------------
cont_frame = 0

# -----------------------------------------------------------------------
#    Inicio de captura de video y su procesamiento
# -----------------------------------------------------------------------
while True:

        # -----------------------
        #   Captura de frames
        # -----------------------
        ret, frame = vs.read()
        if frame is None:
                break
        # ----------------------------------------------------
        # Sin importar el tamaño de los frames, se estandariza
        #   el tamaño del frame a un ancho de 600 pixeles
        # ----------------------------------------------------
        frame = imutils.resize(frame, width=600)
        # --- Filtro para minimizar ruido ---
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        # --- Coversion al espacio de color HSV ---
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        # construct a mask for the color, then perform
        # a series of dilations and erosions to remove any small
        # blobs left in the mask
        # --- Mascara para detección delcolor ---
        mask = cv2.inRange(hsv, colorLower, colorUpper)
        # --- Dilatacion y erosion para limpiar contorno de canica ---
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        # ----------------------------------------------------
        # Encuentra el contorno de la máscara (canica) e
        # inicializa las coordenadas (x,y) del centro de
        #                 de la canica
        # ----------------------------------------------------
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        center = None

        # --- Inicia cronómetro para medir tiempo ---
        to = time.time()

        # --- Si localiza el contorno de la canica ---
        if len(cnts) > 0:
                # -----------------------------------------------
                # Encuentra el contorno mas grande en la máscara
                # -----------------------------------------------
                c = max(cnts, key=cv2.contourArea)
                # -----------------------------------------------
                # Calcula el minimo circulo interior y su
                #       centroide (centro de masa)
                # -----------------------------------------------
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

                # --- Activa una marca "t" en el cronómetro ---
                t = time.time()

                # --- Si la canica tiene un radio mínimo de 10 ---
                if radius > 10:
                        # ---------------------------------------------
                        # Dibuja el circulo amarillo alrededor de la
                        #                 canica
                        # ---------------------------------------------
                        cv2.circle(frame, (int(x), int(y)), int(radius),
                                (0, 255, 255), 2)
                        # ---------------------------------------------
                        # Dibuja un punto rojo en el centro de la canica
                        # ---------------------------------------------
                        cv2.circle(frame, center, 5, (0, 0, 255), -1)

        # -------------------------------------------------------
        # Almacena en el diccionario "pos", las coordenadas de la
        #        posición de la canica y su centro
        # -------------------------------------------------------
        pos = {"xy":(x, y), "center":center}
        # -------------------------------------------------------
        # Almacena en el arreglo "cola" de diccionarios "pts" el
        #               diccionario "pos"
        # -------------------------------------------------------
        pts.appendleft(pos)

        # -------------------------------------------------------
        # Si la canica no ha iniciado su movimiento, las dos
        #   localidades del arreglo "cola" de diccionarios
        #                  están vacias
        # -------------------------------------------------------
        if pts[-1]["center"] is None or pts[0]["center"] is None:
                continue

        # -------------------------------------------------------
        # Captura posiciones instantáneas del movimiento del
        # "centro de masa" de la canica:
        # pts[0]  -> posicion actual
        # pts[-1] -> posicion inmediatamente anterior
        # -------------------------------------------------------
        xm0 = pts[0]["center"][0]
        ym0 = pts[0]["center"][1]
        xm1 = int(pts[-1]["center"][0]*100)/100
        ym1 = int(pts[-1]["center"][1]*100)/100
        # --- Calcula los desplazamientos en "x" y "y" ---
        dxm = xm1 - xm0
        dym = ym1 - ym0
        # --- Calcula la distancia instantánea recorrida ---
        dm = int(np.sqrt(dxm*dxm + dym*dym)*100)/100
 
        # -------------------------------------------------------
        # Captura posiciones instantáneas del movimiento de
        # la canica:
        # pts[0]  -> posicion actual
        # pts[-1] -> posicion inmediatamente anterior
        # -------------------------------------------------------
        xn0 = int(pts[0]["xy"][0]*100)/100
        yn0 = int(pts[0]["xy"][1]*100)/100
        xn1 = int(pts[-1]["xy"][0]*100)/100
        yn1 = int(pts[-1]["xy"][1]*100)/100
        # --- Calcula los desplazamientos en "x" y "y" ---
        dxn = xn1 - xn0
        dyn = yn1 - yn0
        # --- Calcula la distancia instantánea recorrida ---
        dn = int(np.sqrt(dxn*dxn + dyn*dyn)*100)/100

        # --- Activa una marca "t" en el cronómetro ---
        t = time.time()

        # -------------------------------------------------------
        # Comprueba si existe cambio en la posición del centro
        # de la canica, lo cual indicaría que esta inició su
        #                  movimiento
        # -------------------------------------------------------
        if dm > 3:
                dic = {"xm0":xm0,"ym0":ym0,"xm1":xm1,"ym1":ym1,"dm":dm,
                       "xn0":xn0,"yn0":yn0,"xn1":xn1,"yn1":yn1,"dn":dn,
                       "frame":cont_frame,"t":t}
                info.append(dic)
                print("----------------------------------------------")
                print("fr=",cont_frame," | xm0=",xm0," | xn0=",xn0," | ym0=",ym0," | yn0=",yn0)
                print("fr=",cont_frame," | xm1=",xm1," | xn0=",xn1," | ym0=",ym1," | yn0=",yn1)
                print(" | dm=",dm," | dn=",dn," | t=",t)
                print("dic[frame]=",dic["frame"])
                cont_frame +=1  

        # --- Muestra cada frame ---
        cv2.imshow("Frame", frame)
        
        # --- Captura de teclado ---
        key = cv2.waitKey(1) & 0xFF
        # -----------------------------------------------------
        # Si se presiona la tecla "q" el programa termina
        # -----------------------------------------------------
        if key == ord("q"):
                break

vs.release()

# close all windows
cv2.destroyAllWindows()

