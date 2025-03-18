

#By: FVasquez

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
#_##_##_##_##_##_##_##_##_##_##_##_##_##_##_##_##_##_##_##_##_##_# Conexion puerto serial y mas



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
#_##_##_##_##_##_##_##_##_##_##_##_##_##_##_##_##_##_##_##_##_##_# Logger



#_##_##_##_##_##_##_##_##_##_##_##_##_##_##_##_##_##_##_##_##_##_# Funciones
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

def leer_datos():
	antena = ""
	status = ""
	producto = ""
	# Abrir conexion con sensores
	try:
		ser = serial.Serial(puerto_com, velocidad,timeout=None)
		logger.info("Conexion con sensores: OK!")
		logger.info("esperando...")
		datos1 = ser.readline().decode('utf-8').strip()  # Lee y decodifica los datos: XR[_____]
		datos2 = ser.readline().decode('utf-8').strip()  # Lee y decodifica los datos: X____[_]

		(antena,status) = procesar_Xdato(datos2)
		producto = procesar_XRdato(datos1)
		logger.info("datos procesados con exito")
		
	except Exception as e:
		logger.critical("Sin conexion con los sensores!")
		svars.log1 = "Sin conexion con sensores"
		svars.log2 = str(e)
		#exit()

	finally:
		if ser.isOpen():
			ser.close()  # Cierra el puerto serial al finalizar
			logger.info("puerto cerrado")

	return (antena,status,producto)
#_##_##_##_##_##_##_##_##_##_##_##_##_##_##_##_##_##_##_##_##_##_# Funciones

if __name__ == '__main__':

	logger.debug("OK __main__")

elif __name__ == '__ax_main__':     # Run from Scala. Python 2.7.17

	logger.info("...INICIO de Script")

	import scalatools as st
	import scalalib as sl

	# Importamos las variables que compartimos de SD aqui
	svars = sl.sharedvars()

	while  True:
		mat_status = svars.status_pds
		(antena,status,producto) = leer_datos()
		logger.info("Datos leidos!")
		logger.debug(antena)
		logger.debug(producto)
		logger.debug(status)



		if(status == "1"):
			svars.log1 = "UP"
			mat_status[int(producto)-1] = "0"
		else:
			svars.log1 = "UPnot"
			mat_status[int(producto)-1] = antena

		pds_UP = mat_status.count("0")
		svars.log2 = str(pds_UP)

		#svars.log1 = str(type(status))
		#svars.log2 = str(type(producto))
		svars.pds_arriba = pds_UP
		svars.status_pds = mat_status
		logger.info("Fin LooP...")
