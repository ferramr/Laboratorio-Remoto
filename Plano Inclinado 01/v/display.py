# *************************************
#
# Clase: --> Display 
# Modulo: -> display.py
# Ubicacion -> v.display
#
# Descripción:
#   Muestra informacion del sistema sobre la imagen
#
# Fecha:
#   diciembre 31/2021
#
# ************************************

import time
import datetime
import cv2

p_ref = (600, 60)
w_ref = 240
h_ref = 30

class Display:

    # -------------------------------------------------------
    #           CONSTRUCTOR
    # -------------------------------------------------------
    def __init__(self):
        print("----------------------------")
        print(" CONSTRUCTOR: Display")
        print("----------------------------")

    def mostrar_informacion_sistema(self,frame):
        # --------------------------
        # Escribir texto sobre video
        # --------------------------
        # Add data to video (real time and sensor)
        hora = str(datetime.datetime.now())
        #fecha = datetime.datetime.now()
        #amdh = fecha.year
        #print(type(hora))
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, hora,(10,30), font, 0.8,(255,0,0),2,cv2.LINE_AA)

        # mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
        # ----------------------------------------------------------------------
        #           Manejo de la Ventana de DATOS [Display]
        # ----------------------------------------------------------------------
        # --- DISPLAY [fondo azul] ---
        # -----------------------------------------------------------
        #                   ESTADO DEL SISTEMA
        # -----------------------------------------------------------
        topLeft = (10, 25)
        bottomRight = (840, 55)

        topLeft_label = ((topLeft[0]+10), (topLeft[1]+20))
        topLeft_value = ((topLeft[0]+100), (topLeft[1]+20))

        font = cv2.FONT_HERSHEY_SIMPLEX
        color_bg = (255,0,0)        # Color fondo: Azul oscuro 
        color_txt = (255,255,255)   # Color texto: Blanco 
        
        cv2.rectangle(frame, topLeft,bottomRight,color_bg, -1)
        #cv2.line(frame, bottomLeft, topLeft, (0, 255, 0), 2)
        #print("XXXXXXXXXXXXXXXXXXXX")
        #print(estado["SA"])
        # --- TEXTO/DATOS DISPLAY [letras/digitos blancol]
        cv2.putText(frame, "Estado:",topLeft_label,font,0.6, color_txt,2,cv2.LINE_AA)
        cv2.putText(frame, "AAA",topLeft_value,font,0.6,color_txt,1,cv2.LINE_AA)

    def crear_ventana_informativa(self,frame,nv,etiqueta,valor):

        global p_ref
        # -----------------------------------------------------------
        #   Ventana Horizontal de 240 x 30
        # -----------------------------------------------------------
        num_ventana = nv
        dh = (num_ventana-1)*h_ref
        gap = (num_ventana-1)*5
        topLeft = (p_ref[0], (p_ref[1]+dh+gap))
        bottomRight = (p_ref[0]+w_ref, p_ref[1]+dh+gap+h_ref)

        topLeft_label = ((topLeft[0]+10), (topLeft[1]+20))
        topLeft_value = ((topLeft[0]+100), (topLeft[1]+20))

        font = cv2.FONT_HERSHEY_SIMPLEX
        color_bg = (255,0,0)        # Color fondo: Azul oscuro 
        color_txt = (255,255,255)   # Color texto: Blanco 

        cv2.rectangle(frame, topLeft,bottomRight,color_bg, -1)
        
        # --- TEXTO/DATOS DISPLAY [letras/digitos blancol]
##        cv2.putText(frame, "Angulo:         grados",topLeft_label,font,0.6, color_txt,2,cv2.LINE_AA)
##        cv2.putText(frame, "123",topLeft_value,font,0.6,color_txt,1,cv2.LINE_AA)
        cv2.putText(frame, etiqueta[nv],topLeft_label,font,0.6, color_txt,2,cv2.LINE_AA)
        cv2.putText(frame, valor[nv],topLeft_value,font,0.6,color_txt,1,cv2.LINE_AA)
