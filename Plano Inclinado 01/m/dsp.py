# *************************************
#
# Clase: --> DSP 
# Modulo: -> dsp.py
# Ubicacion -> m.dsp
#
# Descripción:
#   Procesamiento digital de señales
#   Actualiza el diccionario:
#
# Fecha:
#   diciembre 29/2021
#
# ************************************

import numpy as np

global t                # t - tiempo de la muestra "n"
global d                # d - distancia de la muestra "n"
global posicion         # posicion = (d, t)

global D                # D - Lonigtud del plano inclinado en "pixeles"
global angulo           # angulo - Angulo del plano inclinado
global plano_inclinado  # plano_inclinado = (D, angulo)

global model_d          # model_d - Ecuacion de la Distancia(t)
global model_v          # model_v - Ecuacion de la Velocidad(t)
global model_a          # model_a - Ecuacion de la Aceleracion(t)
global modelos          # modelos = (model_d, model_v, model_a)

global u                # u - coeficiente de friccion dinamica

global texto            # texto - texto informativo a desplegar
global valor            # valor - valor a desplegar
global num_display      # num_display - numero de ventanas informativas

class DSP:

    # -------------------------------------------------------
    #           CONSTRUCTOR
    # -------------------------------------------------------
    def __init__(self):
        print("----------------------------")
        print(" CONSTRUCTOR: DSP")
        print("----------------------------")

        global t
        global d
        global plano_inclinado 

        t = []
        d = []
        plano_inclinado = []

    def procesar_muestras_capturadas(self,muestras,plano_inc):
        print("-------------------------------------")
        print(" CLASE: DSP")
        print(" procesar_muestras_capturadas")
        print("--------------------------------------")

        # ---------------------------------------------------------
        # plano_inclinado = (D, angulo) -> Vector de dos valores:
        #
        #  D = Lonigtud de la hipotenusa en "pixeles"
        #       Se toma como referencia esta longitud en "pixeles" para
        #       relacionarla con la longitud de 38.0 cm medidos
        #       entre los marcadores
        #
        #  angulo = Angulo de inclinacion en grados
        # ---------------------------------------------------------

        global t
        global d
        global posicion # <- posicion (d, t)

        global D
        global angulo
        global plano_inclinado

        global model_d
        global model_v
        global model_a

        global modelos # <- modelos (model_d, model_v, model_a)

        global u

        tmpo = []
        dpix = []
        posicion = []

        # ---------------------------------------------------
        # Captura de los valores de Longitud y Angulo del
        # Plano Inclinado
        # ---------------------------------------------------
        plano_inclinado = plano_inc
        D = plano_inclinado[0]
        angulo = plano_inclinado[1]
        print("D [pixeles] = ",plano_inclinado[0])

        # --- Formato del arreglo de diciionarios: "muestras: m" ---
        #
        # m = {"n":contador_muestras,
        #      "p1":(x1,y1,t1),
        #      "p0":(x0,y0,t0),
        #      "dx":dx,"dy":dy,"dm":dm}
        #
        # n -> numero de muestra
        # p1 -> coordenada instantanea anterior: (x1,y1,t1)
        # p0 -> coordenada instantanea actual: (x0,y0,t0)
        # dx -> desplazamiento en "x"
        # dy -> desplazamiento en "y"
        # dm -> distancia recorrida en pixeles del punto
        #       p1 al punto p0
        # 
        # -----------------------------------------------------------

        # ---- o: <- Origen ---
        xo, yo, to = muestras[0]["p1"]
        # --- Vectores de tiempo y distancia en t = 0 ---
        tmpo.append(0)
        dpix.append(0)

        # --- Calculo de "distancias" al origen "o" ---             
        for i in range(len(muestras)):
            # --- i: <- Valores "instantáneos" refereidos al origen "o" ---
            xi, yi, ti = muestras[i]["p0"]
            x = xi - xo
            y = yo - yi
            # --- Tiempo "tro" y distancia "dro" referidos al origen ---
            tro = round((ti - to),2)
            dro = round(np.sqrt(x*x + y*y),2)
            # --- Vectores de tiempo y distancia ---
            tmpo.append(tro)
            dpix.append(dro)
 
        # --- Acondicionar datos de tiempo (tmpo) para graficación t[seg] ---
        tmin = tmpo[0]
        tmax = tmpo[len(tmpo)-1]
        t = np.linspace(tmin, tmax, len(tmpo))        

        # --- Acondicionar datos de distancia (dpix) para graficación d[cm] ---
        Dref_pix = plano_inclinado[0]
        d = [round(dp*38.0/Dref_pix,3) for dp in dpix]

        # --- Posicion ---
        for i in range(len(t)):
            posicion.append([d[i], round(t[i],3)])

        # --------------------------------------------------------------------
        # Modelado matemático mediante un polinomio de 2ndo. Orden de la
        # relación entre distancia recorrida y tiempo:
        # Distancia = F(t) = ad^2 +bd + c
        # --------------------------------------------------------------------
        #   Calculo de los coeficientes: a, b y c de: F(t) = ax^2 +bx + c
        # --------------------------------------------------------------------
        #d_t = np.polyfit(t, d, 2)
        d_t = np.polyfit(tmpo, d, 2)

        # --------------------------------------------------------------------
        # --- Modelos matemáticos en formato de polinomio: F(t) = ax^2 +bx + c
        # --------------------------------------------------------------------
        # --------------------------------------------------------------------
        #     Distancia(t) = ax^2 +bx + c
        # --------------------------------------------------------------------
        model_d = np.poly1d(d_t)
        # --------------------------------------------------------------------
        #     Velocidad(t) = d(Distancia)/dt = 2ax +b <- 1era. DERIVADA
        # --------------------------------------------------------------------
        model_v = model_d.deriv()
        # --------------------------------------------------------------------
        #     Aceleracion(t) = d2(Distancia)/dt = 2a <- 2nda. DERIVADA
        # --------------------------------------------------------------------
        model_a = model_v.deriv()

        # --- Modelos ---
        modelos = (model_d, model_v, model_a)

        # --------------------------------------------------------------------
        #     Calculo del Coeficiente de Fricción Dinámica "u"
        # --------------------------------------------------------------------
        angulo_rad = angulo*np.pi/180
        am = model_a[0]/100
        agtc = 9.8*(np.cos(angulo_rad))*np.tan(angulo_rad)
        agc = 9.8*np.cos(angulo_rad)
        u = round(((am - agtc)/agc),4)
    
    @property
    def t(self):
        return t

    @property
    def d(self):
        return d

    @property
    def posicion(self):
        return posicion

    @property
    def D(self):
        return D

    @property
    def angulo(self):
        return angulo

    @property
    def plano_inclinado(self):
        return plano_inclinado

    @property
    def model_d(self):
        return model_d

    @property
    def model_v(self):
        return model_v

    @property
    def model_a(self):
        return model_a

    @property
    def modelos(self):
        return modelos

    @property
    def u(self):
        return u

    def vector_informacion_display(self):

        global texto
        global valor
        global num_display

        texto = []
        valor = []
        
        texto.append("angulo:          grados")
        texto.append("muestras:")
        texto.append("distancia:       cm")
        texto.append("tiempo:          seg")
        texto.append("aceleracion:     m/s^2")
        texto.append("co.fricc. u:")

        valor.append(str(angulo))
        valor.append(str(len(posicion)))
        valor.append("38")
        valor.append(str(posicion[len(posicion)-1][1]))
        valor.append(str(round(model_a(0),3)))
        valor.append(str(u))

        num_display = len(texto)

    @property
    def texto(self):
        return texto
    
    @property
    def valor(self):
        return valor

    @property
    def num_display(self):
        return num_display
    
    def imprimir_informacion_sistema(self):

        global t
        global d
        global posicion
        global D
        global angulo
        global u

        print()
        print(" -----------------------------------------------")
        print("  Clase: DSP ::")
        print("     Imprime Posicion ('distancia[cm]' y 'tiempo[seg]') ")
        print(" -----------------------------------------------")
        print(" Longitud del plano inclinado: ",D," pixeles")
        print(" Longitud del plano inclinado: ",38.0," cm")
        print(" Angulo del plano inclinado:   ",angulo," grados")
        print(" Coeficiente de Friccion Dinamica:   ",u)
        print()
        print("n,  d[cm],  t[seg],   d(t),   v(t),   a(t)")
        for i in range(len(posicion)):
            t_t = posicion[i][1]
            d_t = round(model_d(t_t),3)
            v_t = round(model_v(t_t),3)
            a_t = round(model_a(t_t),3)
            print(i,"  ",posicion[i][0],"  ",posicion[i][1],
                  "  ",d_t,"  ",v_t,"  ",a_t)
        print(" -----------------------------------------------")
