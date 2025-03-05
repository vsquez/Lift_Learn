# -*- coding: UTF-8 -*-











# By: FelipeVsquez & VictoriaGmez

import serial
import re
import time

# Patrones regex
patron_xr = re.compile(ur"XR\[(\w+)\]")  # Para XR[PU003]
patron_x = re.compile(ur"X(\w+)\[(\w+)\]")  # Para X003A[1]

# Funcion para procesar los datos
def procesar_dato(dato):
	producto = u""
	antena = u""
	status = u""
	if patron_xr.match(dato):  # Si coincide con XR[...]
		producto = patron_xr.match(dato).group(1)
		#print(u"Producto: {}".format(producto))
	elif patron_x.match(dato):  # Si coincide con XAAAA[...]
		antena = patron_x.match(dato).group(1)
		status = patron_x.match(dato).group(2)
		#print(u"Antena: {}, Status: {}".format(antena, status))
	else:
		print(u"Formato no válido: {}".format(dato))

	print(u"Antena: {}\nProducto: {}\nStatus: {}\n".format(antena, producto, status))
	 

puerto_com = 'COM3'  # Cambia esto al puerto COM que estes utilizando
velocidad = 115200   # Ajusta la velocidad segun la configuracion de tu dispositivo


# Abrir conexion con sensores
try:
	ser = serial.Serial(puerto_com, velocidad,timeout=None)
except Exception as e:
	logger.critical("Sin conexion con los sensores!")
	svars.error = True
	exit()

try:
	while True:
		###!!! (sig 2 line)Se esperara infinitamente para solo seguir cuando haya un cambio en los sensores !!!###
		if ser.in_waiting > 0:  # Verifica si hay datos disponibles
			datos1 = ser.readline().decode('utf-8').strip()  # Lee y decodifica los datos: XR[_____]
			datos2 = ser.readline().decode('utf-8').strip()  # Lee y decodifica los datos: X____[_]
			print(datos1)
			print(datos2)
		else:
			time.sleep(0.1)  # Pequenia pausa para no saturar la CPU
			continue
		#procesar_dato(datos)
		#print("Dato recibido: "+(datos))
		#print(str(type(datos)))
except UnicodeDecodeError:
	print("Error: No se pudo decodificar los datos. Prueba con otra codificacion.")
except KeyboardInterrupt:   # Se interrumpe con Ctrl + C, en el teclado
	# Cerrar el puerto COM al interrumpir el programa
	print("cerrando...")
	#ser.close()
finally:
	ser.close()  # Cierra el puerto serial al finalizar

