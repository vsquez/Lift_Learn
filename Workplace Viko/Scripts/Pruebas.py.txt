"""
C:\Users\pillo\OneDrive\Escritorio\Lift_Learn
"""

import serial

# Configurar el puerto COM
puerto_com = 'COM3'  # Cambia esto al puerto COM que estes utilizando
velocidad = 115200  # Ajusta la velocidad segun la configuracion de tu dispositivo

#ser = serial.Serial(puerto_com, velocidad, timeout=3)
#ser = serial.Serial(puerto_com, velocidad)
ser = serial.Serial(puerto_com, velocidad,timeout=1)

#print(ser.timeout)
#print(ser)

try:
	while True:
		# Leer datos del puerto COM
		datos = ser.readline()
		#datos2 = ser2.readline()

		datos = datos.decode()
		#print(datos.decode('utf-8').strip())  # Decodificar y mostrar los datos

		#print(datos2)
		
		if datos == "":
			print("Sin cambios")
		else:
			#print(datos)
			datos = datos.split('[')[1].replace(']',"")
			datos = datos.split("\r")[0]
			print(datos)

except KeyboardInterrupt:   # Se interrumpe con Ctrl + C, en el teclado
	# Cerrar el puerto COM al interrumpir el programa
	ser.close()


"""
try:
	while True:
		# Leer datos del puerto COM
		datos = ser.readline()
		print(datos.decode('utf-8').strip())  # Decodificar y mostrar los datos
except KeyboardInterrupt:
	# Cerrar el puerto COM al interrumpir el programa
	ser.close()
"""