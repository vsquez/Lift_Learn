











# By: FelipeVsquez & VictoriaGmez

import logging
import serial
import time
import re

#_##_##_##_##_##_##_##_##_##_##_##_##_##_##_##_##_##_##_##_##_##_# Conexion puerto serial y mas
# Configuraciones del puerto COM
puerto_com = 'COM3'  # Cambia esto al puerto COM que estes utilizando
velocidad = 115200  # Ajusta la velocidad segun la configuracion de tu dispositivo

# Patrones regex para respuestas de los sensores
patron_xr = re.compile(ur"XR\[(\w+)\]")  # Para XR[PU003]
patron_x = re.compile(ur"X(\w+)\[(\w+)\]")  # Para X003A[1]

#_##_##_##_##_##_##_##_##_##_##_##_##_##_##_##_##_##_##_##_##_##_# Logger
# Creamos y configuramos "debug_logger"
logger = logging.getLogger("debug_logger")  # Creamos logger
logger.setLevel(logging.DEBUG)  # Asignamos el nivel

# Configuramos el StreamHandler (para consola)
manejador_stream = logging.StreamHandler()
formato = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", "%I:%M:%S%p %d/%m")
manejador_stream.setFormatter(formato)

# Configuramos el FileHandler (para archivo)
#manejador_archivo = logging.FileHandler("C:/Users/pillo/OneDrive/Escritorio/Lift_Learn/Scripts/logs/L&L.log")
manejador_archivo = logging.FileHandler("C:/Users/Felipe/Desktop/Lift_Learn/Scripts/logs/L&L.log")
#manejador_archivo = logging.FileHandler("D:/L&L/logs/L&L.log")
manejador_archivo.setFormatter(formato)  # Usamos el mismo formato

# Aniadimos ambos manejadores al logger
logger.addHandler(manejador_stream)
logger.addHandler(manejador_archivo)

# (solo para __ax_main__) Procesamos las respuestas de tipo XR[ssppp]
def procesar_XRdato(dato):	#XR[ssppp]
	# dato: senial de sensor. eg: XR[PU003]; producto = 003
	producto_completo = patron_xr.match(dato).group(1)
	producto = producto_completo[-3:]  # Solo nos interesa la parte de ppp
	return producto

# (solo para __ax_main__) Procesamos las respuestas de tipo Xaaaa[y]
def procesar_Xdato(dato):	#Xaaaa[y]
	# dato: senial de sensor. eg: X003A[1]; antena = 003A y status = 1
	antena = patron_x.match(dato).group(1)
	status = patron_x.match(dato).group(2)
	return (antena,status)

def mandar_falsosXRdatos(status):
	return u"XR["+status+""


#_##_##_##_##_##_##_##_##_##_##_##_##_##_##_##_##_##_##_##_##_##_# CMD # Run from the command line (for testing).
if __name__ == '__main__':          
	# -*- coding: utf-8 -*-

	# Desde consola
	logger.debug("__main__ Ok!")

#_##_##_##_##_##_##_##_##_##_##_##_##_##_##_##_##_##_##_##_##_##_# SD # Run from Scala. Python 2.7.17
elif __name__ == '__ax_main__':     
	import scalatools as st
	import scalalib as sl

	logger.debug("__ax_main__ Ok!")

	# Importamos las variables que compartimos de SD aqui
	svars = sl.sharedvars()
	logger.info("Variables de SCALA importadas")

	# Abrir conexion con sensores
	try:
		ser = serial.Serial(puerto_com, velocidad,timeout=0.1)
		logger.info("Conexion con sensores: OK!")
	except Exception as e:
		logger.critical("Sin conexion con los sensores!")
		svars.error = True
		svars.log1 = "Sin conexion con los sensores!"
		#exit()

	# status_X: Lo que se encuentra en la antena 1/2/3/4
	# Dar seniales de que todo OK!
	svars.antena_4A = "ok!"
	svars.antena_6A = "ok!"
	svars.antena_3A = "ok!"
	svars.antena_5A = "ok!"

	time.sleep(2)

	svars.antena_4A = "void"
	svars.antena_6A = "void"
	svars.antena_3A = "void"
	svars.antena_5A = "void"

	# LOOP (escuchar sensores en todo momento)
	logger.debug("Entrando en LOOP...")
	try:
		while True:
			#if  ser.in_waiting > 0 and svars.error != True:  # Verifica si hay datos disponibles
			if svars.error != True:   # Verifica si hay datos disponibles
					if ser.in_waiting > 0:
						datos1 = ser.readline().decode('utf-8').strip()  # Lee y decodifica los datos: XR[_____]
						datos2 = ser.readline().decode('utf-8').strip()  # Lee y decodifica los datos: X____[_]
						logger.info("Datos leidos: "+datos1+" - "+datos2)
						logger.debug(datos1)
						logger.debug(datos2)
			if svars.log_status == 0:
				datos1 = mandar_falsosXRdatos("PB",)
			else:
				time.sleep(0.1)
				logger.debug("nada...")
				continue

			(antena,status) = procesar_Xdato(datos2)
			if status == "0":
				producto = procesar_XRdato(datos1)
			else:
				producto = "void"
			logger.debug("Producto: "+producto+" Antena: "+antena+" Status: "+status)


			if antena == "004A":
				svars.log1 = "Movimiento en 4A"
				svars.antena_4A = producto
			elif antena == "006A":
				svars.log1 = "Movimiento en 6A"
				svars.antena_6A = producto
			elif antena == "003A":
				svars.log1 = "Movimiento en 3A"
				svars.antena_3A = producto
			else:
				svars.log1 = "Movimiento en 5A"
				svars.antena_5A = producto

	except Exception as e:
		#logger.error("Error inesperado. Error: "+str(e))
		logger.info("'Esc' presionado, saliendo...")
	except KeyboardInterrupt:   # Se interrumpe con Ctrl + C, en el teclado
		# Cerrar el puerto COM al interrumpir el programa
		logger.info("cerrando conexion...")
		svars.log1 = "reiniciando"
	finally:
		if svars.error != True:
			ser.close()  # Cierra el puerto serial al finalizar
		logger.info("FIN del script")
		svars.interrumpir = True
