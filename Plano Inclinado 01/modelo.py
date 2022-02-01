#******************************************************
#
#  PLANO INCLINADO - Proyecto IoT
#
#
#     Algoritmo:
#
#  1.
#  2. 
#  3. El proceso se repite ciclicamente
#
#                                   31 / diciembre / 2021
#
#  Requiere tener conectado ARDUINO corriendo el programa:
#
#   Arduino/Plano Inclinado IoT/
#   plano_inclinado_05.ino
#
# Manejo de OpenCV + SerialPort desde las ESP32CAM
# https://stackoverflow.com/questions/67051192/get-data-from-esp32-over-video-in-opencv-python-freezing-video
#
#******************************************************
#******************************************************************************************
#https://pyserial.readthedocs.io/en/latest/tools.html#serial.tools.list_ports.ListPortInfo
#******************************************************************************************

##import time
##import datetime
import imutils
import cv2

from c.comunicacion import Comunicacion
from m.dsp import DSP
from v.graficador import Graficador
from v.display import Display
from m.marcadores import Marcadores
from m.esfera import Esfera


# -----------------------------------------------------------------------
#       Inicializa la cámara web
# -----------------------------------------------------------------------
vs = cv2.VideoCapture(0)

# ------------
#   AMARILLO
# ------------
amarilloLower = (25, 68, 6)
amarilloUpper = (35, 255, 155)
rangoAmarillo = ((25, 68, 6),(35, 255, 155))

# ------------
#  AZUL CLARO
# ------------
azulClaroLower = (80, 100, 60)
azulClaroUpper = (120, 180, 255)
rangoAzulClaro = ((80, 100, 60), (120, 180, 255))

# ----------------------------------------
# Creacion de objetos
# ----------------------------------------
com = Comunicacion()
serialConnection = com.inicializar_comunicacion_serial()
dsp = DSP()
graficas = Graficador()
marcador = Marcadores(rangoAzulClaro)
esfera = Esfera(rangoAmarillo)
info = Display()

secuencia = []
secuencia.append('Sistema Activado')
secuencia.append('Solicitud Recibida')
secuencia.append('Inicializa Esfera')
secuencia.append('Angulo CERO')
secuencia.append('Angulo SOLICITADO')
secuencia.append('Libera Esfera')
secuencia.append('Finaliza Experimento')

sel = None

while True:
       
        # ----------------------------------
        # Lectura de comandos recibidos
        # desde arduino
        # ----------------------------------
        comando = com.leer_comando_serial(serialConnection)
        if comando != None:
                sel = comando
                print("-------------------------------------------------")
                print("   ",secuencia[sel])
                print("-------------------------------------------------")
                      
        # -----------------------
        #   Captura de frames
        # -----------------------
        ret, frame = vs.read()
        if frame is None:
                break

        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # procesamiento_imagen(frame)
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # ----------------------------------------------------
        # Sin importar el tamaño de los frames, se estandariza
        #   el tamaño del frame a un ancho de 850 pixeles
        # ----------------------------------------------------
        frame = imutils.resize(frame, width=850)

        # --- Filtro para minimizar ruido ---
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        # --- Coversion al espacio de color HSV ---
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

##        info.mostrar_informacion_sistema(frame)
##        etiqueta = "Angulo:         grados"
##        marcador.distancia_entre_marcadores(frame,hsv)
##        marcador.dibujar_triangulo_rectangulo(frame)
##        valor = str(marcador.angulo)
##        info.crear_ventana_informativa(frame,1,etiqueta,valor)


        if sel == 2: # --- Inicializa Esfera ---
                esfera.inicializar_variables_muestreo()

        elif sel == 3: # --- Angulo CERO ---
                marcador.distancia_entre_marcadores(frame,hsv)
                marcador.dibujar_linea_horizontal(frame)

        elif sel == 4:  # --- Angulo Solicitado ---
                marcador.distancia_entre_marcadores(frame,hsv)
                marcador.dibujar_triangulo_rectangulo(frame)
                esfera.seguir_trayectoria_esfera(frame,hsv)

        elif sel == 5: # --- Libera Esfera
                marcador.distancia_entre_marcadores(frame,hsv)
                marcador.dibujar_triangulo_rectangulo(frame)
                
                esfera.seguir_trayectoria_esfera(frame,hsv)
                esfera.muestrear_posiciones_esfera(frame,esfera.center)

        elif sel == 6: # --- Finaliza Experimento ---
                if comando == 6:
                        esfera.imprimir_muestras_capturadas()
                        muestras = esfera.muestras
                        dsp.procesar_muestras_capturadas(muestras,
                                                         marcador.plano_inclinado)
                        dsp.imprimir_informacion_sistema()
                        dsp.vector_informacion_display()
                        
                marcador.distancia_entre_marcadores(frame,hsv)
                marcador.dibujar_triangulo_rectangulo(frame)
                graficas.graficar_curvas_resultantes1(frame,
                                                     dsp.t,dsp.d,dsp.modelos)
                for i in range(len(dsp.texto)):
                                info.crear_ventana_informativa(frame,i,
                                                               dsp.texto,
                                                               dsp.valor)

                #info.crear_ventana_informativa(frame,1,etiqueta,valor)
               

##            graficas.graficar_curvas_resultantes(frame,muestras_procesadas)
##        
##        # ----------------------------------------------------------
##        #            Calculo del ANGULO del Plano Inclinado
##        # ----------------------------------------------------------
##        # PLANO INCLINADO:   0      0 <- Punto "0"
##        #                     \     1 <- Punto "1"
##        #                      \    2 <- Punto "2"
##        #                    2--1
##        # ----------------------------------------------------------
##        altura = pty0 - pty2
##        dy = altura
##        dx = ptx2 - ptx1
##        hipotenusa = np.sqrt(dx*dx + dy*dy)
##        angulo = 0
##        if hipotenusa == 0:
##            sin_angulo = 0
##        else:
##            sin_angulo = -dy/hipotenusa
##            angulo = np.arcsin(sin_angulo)* 180 / np.pi  # Angulo en grados
##            angulo = int(angulo*10)/10
                
##        # --------------------------
##        # Escribir texto sobre video
##        # --------------------------
##        # Add data to video (real time and sensor)
##        hora = str(datetime.datetime.now())
##        #fecha = datetime.datetime.now()
##        #amdh = fecha.year
##        #print(type(hora))
##        font = cv2.FONT_HERSHEY_SIMPLEX
##        cv2.putText(frame, hora,(10,30), font, 0.8,(255,0,0),2,cv2.LINE_AA)
        #cv2.putText(frame, fecha,(10,50), font, 0.8,(255,0,0),2,cv2.LINE_AA)
        #cv2.putText(frame, estado,(10,60), font, 0.8,(255,0,0),2,cv2.LINE_AA)
        
        # mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
        # ----------------------------------------------------------------------
        #           Manejo de la Ventana de DATOS [Display]
        # ----------------------------------------------------------------------
        # --- DISPLAY [fondo azul] ---
        # -----------------------------------------------------------
        #                   ESTADO DEL SISTEMA
        # -----------------------------------------------------------
##        topLeft = (10, 25)
##        bottomRight = (840, 55)
##
##        topLeft_label = ((topLeft[0]+10), (topLeft[1]+20))
##        topLeft_value = ((topLeft[0]+100), (topLeft[1]+20))
##
##        font = cv2.FONT_HERSHEY_SIMPLEX
##        color_bg = (255,0,0)        # Color fondo: Azul oscuro 
##        color_txt = (255,255,255)   # Color texto: Blanco 
##        
##        cv2.rectangle(frame, topLeft,bottomRight,color_bg, -1)
##        #cv2.line(frame, bottomLeft, topLeft, (0, 255, 0), 2)
##        print("XXXXXXXXXXXXXXXXXXXX")
##        print(estado["SA"])
##        # --- TEXTO/DATOS DISPLAY [letras/digitos blancol]
##        cv2.putText(frame, "Estado:",topLeft_label,font,0.6, color_txt,2,cv2.LINE_AA)
##        cv2.putText(frame, estado["SA"],topLeft_value,font,0.6,color_txt,1,cv2.LINE_AA)
##        
##        # -----------------------------------------------------------
##        #                   ANGULO DEL PLANO INCLINADO
##        # -----------------------------------------------------------
##        topLeft = (600, 60)
##        topRight = (840, 60)
##        bottomLeft =(600, 90)
##        bottomRight = (840, 90)
##
##        topLeft_label = ((topLeft[0]+10), (topLeft[1]+20))
##        topLeft_value = ((topLeft[0]+110), (topLeft[1]+20))
##
##        font = cv2.FONT_HERSHEY_SIMPLEX
##        color_bg = (255,0,0)        # Color fondo: Azul oscuro 
##        color_txt = (255,255,255)   # Color texto: Blanco 
##        
##        cv2.rectangle(frame, topLeft,bottomRight,color_bg, -1)
##
##        if flag_global == 6:
##            teta = angulo
##        else:
##            teta = 0
##         
##        # --- TEXTO/DATOS DISPLAY [letras/digitos blancol]
##        cv2.putText(frame, "Angulo:         grados",topLeft_label,font,0.6, color_txt,2,cv2.LINE_AA)
##        cv2.putText(frame, str(teta),topLeft_value,font,0.6,color_txt,1,cv2.LINE_AA)
##
##        # -----------------------------------------------------------
##        #                   DISTANCIA RECORRIDA
##        # -----------------------------------------------------------
##        topLeft = (600, 95)
##        bottomRight = (840, 125)
##
##        topLeft_label = ((topLeft[0]+10), (topLeft[1]+20))
##        topLeft_value = ((topLeft[0]+110), (topLeft[1]+20))
##
##        font = cv2.FONT_HERSHEY_SIMPLEX
##        color_bg = (255,0,0)        # Color fondo: Azul oscuro 
##        color_txt = (255,255,255)   # Color texto: Blanco 
##        
##        cv2.rectangle(frame, topLeft,bottomRight,color_bg, -1)
##
##        if flag_global == 6:
##            dist = 38.0
##        else:
##            dist = 0
##        
##        # --- TEXTO/DATOS DISPLAY [letras/digitos blancol]
##        cv2.putText(frame, "Distancia:       cm",topLeft_label,font,0.6, color_txt,2,cv2.LINE_AA)
##        cv2.putText(frame, str(dist),topLeft_value,font,0.6,color_txt,1,cv2.LINE_AA)
##
##        # -----------------------------------------------------------
##        #                   TIEMPO TRANSCURRIDO
##        # -----------------------------------------------------------
##        topLeft = (600, 130)
##        bottomRight = (840, 160)
##
##        topLeft_label = ((topLeft[0]+10), (topLeft[1]+20))
##        topLeft_value = ((topLeft[0]+110), (topLeft[1]+20))
##
##        font = cv2.FONT_HERSHEY_SIMPLEX
##        color_bg = (255,0,0)        # Color fondo: Azul oscuro 
##        color_txt = (255,255,255)   # Color texto: Blanco 
##        
##        cv2.rectangle(frame, topLeft,bottomRight,color_bg, -1)
##
##        if flag_global == 6:
##            to = muestras[0]["t"]
##            tf = muestras[len(muestras)-1]["t"]
##            dt = int((tf-to)*100)/100
##        else:
##            dt = 0
##        
##        # --- TEXTO/DATOS DISPLAY [letras/digitos blancol]
##        cv2.putText(frame, "Tiempo:         seg",topLeft_label,font,0.6, color_txt,2,cv2.LINE_AA)
##        cv2.putText(frame, str(dt),topLeft_value,font,0.6,color_txt,1,cv2.LINE_AA)
##
##        # -----------------------------------------------------------
##        #                   MASA DE LA ESFERA
##        # -----------------------------------------------------------
##        topLeft = (600, 165)
##        bottomRight = (840, 195)
##
##        topLeft_label = ((topLeft[0]+10), (topLeft[1]+20))
##        topLeft_value = ((topLeft[0]+110), (topLeft[1]+20))
##
##        font = cv2.FONT_HERSHEY_SIMPLEX
##        color_bg = (255,0,0)        # Color fondo: Azul oscuro 
##        color_txt = (255,255,255)   # Color texto: Blanco 
##        
##        cv2.rectangle(frame, topLeft,bottomRight,color_bg, -1)
##
##        if flag_global == 6:
##            masa = 10
##        else:
##            masa = 0
##        
##        # --- TEXTO/DATOS DISPLAY [letras/digitos blancol]
##        cv2.putText(frame, "Masa:     15   gr",topLeft_label,font,0.6, color_txt,2,cv2.LINE_AA)
##        #cv2.putText(frame, str(masa),topLeft_value,font,0.6,color_txt,1,cv2.LINE_AA)
##
##        # -----------------------------------------------------------
##        #                   GRAVEDAD
##        # -----------------------------------------------------------
##        topLeft = (600, 200)
##        bottomRight = (840, 230)
##
##        topLeft_label = ((topLeft[0]+10), (topLeft[1]+20))
##        topLeft_value = ((topLeft[0]+110), (topLeft[1]+20))
##
##        font = cv2.FONT_HERSHEY_SIMPLEX
##        color_bg = (255,0,0)        # Color fondo: Azul oscuro 
##        color_txt = (255,255,255)   # Color texto: Blanco 
##        
##        cv2.rectangle(frame, topLeft,bottomRight,color_bg, -1)
##
##        if flag_global == 6:
##            masa = 10
##        else:
##            masa = 0
##        
##        # --- TEXTO/DATOS DISPLAY [letras/digitos blancol]
##        cv2.putText(frame, "Gravedad: 9.8  m/s2",topLeft_label,font,0.6, color_txt,2,cv2.LINE_AA)
##        #cv2.putText(frame, str(masa),topLeft_value,font,0.6,color_txt,1,cv2.LINE_AA)
##
##        # -----------------------------------------------------------
##        #                   COEFICIENTE DE FRICCION
##        # -----------------------------------------------------------
##        topLeft = (600, 235)
##        bottomRight = (840, 290)
##
##        topLeft_label = ((topLeft[0]+10), (topLeft[1]+20))
##        topLeft_value = ((topLeft[0]+110), (topLeft[1]+20))
##
##        font = cv2.FONT_HERSHEY_SIMPLEX
##        color_bg = (255,0,0)        # Color fondo: Azul oscuro 
##        color_txt = (255,255,255)   # Color texto: Blanco 
##        
##        cv2.rectangle(frame, topLeft,bottomRight,color_bg, -1)
##
##        if flag_global == 6:
##            masa = 10
##        else:
##            masa = 0
##        
##        # --- TEXTO/DATOS DISPLAY [letras/digitos blancol]
##        #                  "                   "
##        cv2.putText(frame, "Coeficiente de Friccion",topLeft_label,font,0.6, color_txt,2,cv2.LINE_AA)
##        cv2.putText(frame, "Dinamica: 0.4   N/m  ",((topLeft[0]+10), (topLeft[1]+45)),
##                    font,0.6,color_txt,2,cv2.LINE_AA)



        #mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm

        # --- Muestra cada frame ---
        cv2.imshow("Frame", frame)
    
        # --- Captura de teclado ---
        key = cv2.waitKey(1) & 0xFF
        # -----------------------------------------------------
        # Si se presiona la tecla "q" el programa termina
        # -----------------------------------------------------
        if key == ord("q"):
                 break

com.ecribir_comando_serial(serialConnection,"9")      
serialConnection.write(9) # Coloca el plano inclinado en inclinacion de 1 grado
serialConnection.close()
vs.release()

# close all windows
cv2.destroyAllWindows()

#*************************************************************
# https://matplotlib.org/2.1.1/api/_as_gen/matplotlib.pyplot.plot.html

##      character	description
##      '-'	solid line style
##      '--'	dashed line style
##      '-.'	dash-dot line style
##      ':'	dotted line style
##      '.'	point marker
##      ','	pixel marker
##      'o'	circle marker
##      'v'	triangle_down marker
##      '^'	triangle_up marker
##      '<'	triangle_left marker
##      '>'	triangle_right marker
##      '1'	tri_down marker
##      '2'	tri_up marker
##      '3'	tri_left marker
##      '4'	tri_right marker
##      's'	square marker
##      'p'	pentagon marker
##      '*'	star marker
##      'h'	hexagon1 marker
##      'H'	hexagon2 marker
##      '+'	plus marker
##      'x'	x marker
##      'D'	diamond marker
##      'd'	thin_diamond marker
##      '|'	vline marker
##      '_'	hline marker


##      character	color
##      ‘b’	blue
##      ‘g’	green
##      ‘r’	red
##      ‘c’	cyan
##      ‘m’	magenta
##      ‘y’	yellow
##      ‘k’	black
##      ‘w’	white




    
    


