import xml.etree.ElementTree as ET
import serial
import scalalib
import scala5
import time
import os
import threading


val = False
val_line = False



svars = scalalib.sharedvars()


status_producto = ""

id_producto = ""

productos_up = 0


producto_nombre = ["","","","",""]
producto_caracticas = ["","","","",""]
producto_precio = ["","","","",""]
producto_imagen = ["","","","",""]
producto_COMPimagen = ["","","","",""]
producto_pos = ["","","","",""]

p_COM = 'COM3'

t_out = 20


def on_timeout():

	global val

	val = True






t = threading.Timer(t_out, on_timeout)

t.start()






svars.show_welcome_text = "Lift and Learn MMC - Scala"




while True:

	if val == True:

		svars.TriggerSS = svars.TriggerSS + 1
		val = False

	else:


		with (serial.Serial(p_COM,115200,timeout=2)) as ser:



			id_producto = ser.readline()

			if id_producto:
				val_line = True
				id_producto = id_producto.decode()
				id_producto = id_producto.split('[')[1].replace(']',"")
				id_producto = id_producto.split("\r")[0]

			else: 

				val_line = False

		if val_line == True:

			if 'PU' in  id_producto:

				productos_up = productos_up + 1

				t.cancel()

				val = False


				print "Productos arriba: " + str(productos_up)

				if "1" in id_producto[4]: 

					producto_nombre[productos_up] = "Bui Tetra Pak"
					#producto_precio[productos_up] = "428.08"
					producto_caracticas[productos_up] = "Nuestra Infusion de Tonic es una excelente opcion que ofrece un sabor fresco y que se puede disfrutar tanto solo como acompaniada de alguna otra bebida. infuciones con cero calorias, sin endulzantes y sin calorias"
					#producto_imagen[productos_up] = svars.img_Productos[0]
					producto_imagen[productos_up] = svars.img_Productos[0]
					producto_COMPimagen[productos_up] = svars.img_prodcomp[0]
					producto_pos[productos_up] = id_producto





				if "2" in id_producto[4]:

					
					producto_nombre[productos_up] = "Bui Natural"
					#producto_precio[productos_up] = "344.31"
					producto_caracticas[productos_up] = "Agua surgida de la region del Nevado de Toluca, con propiedades que la hacen una excelente opcion para las mejores experiencias culinarias"
					producto_imagen[productos_up] = svars.img_Productos[1]
					producto_COMPimagen[productos_up] = svars.img_prodcomp[1]
					producto_pos[productos_up] = id_producto


				if "3" in id_producto[4]:


					producto_nombre[productos_up] = "Bui Gasificada"
					#producto_precio[productos_up] = "555.16"
					producto_caracticas[productos_up] = "Nuestra Infusion de pepino es una excelente opcion que ofrece un sabor fresco y que se puede disfrutar tanto solo como acompaniada de alguna otra bebida. infuciones con cero calorias, sin endulzantes y sin calorias"
					producto_imagen[productos_up] = svars.img_Productos[2]
					producto_COMPimagen[productos_up] = svars.img_prodcomp[2]
					producto_pos[productos_up] = id_producto




				if "4" in id_producto[4]:

					producto_nombre[productos_up] = "Bui Tonica"
					#producto_precio[productos_up] = "344.31"
					producto_caracticas[productos_up] = "Agua surgida de la region del Nevado de Toluca, con propiedades que la hacen una excelente opcion para las mejores experiencias culinarias"
					producto_imagen[productos_up] = svars.img_Productos[3]
					producto_COMPimagen[productos_up] = svars.img_prodcomp[3]
					producto_pos[productos_up] = id_producto

				print "Id Producto actual:" + producto_pos[productos_up]




			if 'PB' in id_producto:

				productos_up = productos_up - 1

				t.cancel()

				val = False


				for productodown in range(1,len(producto_pos)):

					if id_producto[4] in producto_pos[productodown]:

						producto_nombre[productodown] = ""
						producto_caracticas[productodown] = ""
						producto_precio[productodown] = ""
						producto_pos[productodown] = "PB"

			print "Productos arriba: " + str(productos_up)




			if productos_up == 0:

				t.cancel()

				t = threading.Timer(t_out, on_timeout)

				t.start()

				val = False


				svars.putdown = svars.putdown + 1


			if productos_up == 1:

				for num in range(1,len(producto_pos)):

					if "PU" in producto_pos[num]:

						svars.nom_item = producto_nombre[num]
						svars.img_producto = producto_imagen[num]
						svars.precio_producto = producto_precio[num]
						svars.Carac_Producto = producto_caracticas[num]

				svars.TriggerMMC_ = svars.TriggerMMC_ +  1

			elif productos_up == 2:

				i = 0

				svars.productos_names[1] = "Hola"

				for num in range(1,len(producto_pos)):

					if "PU" in producto_pos[num]:

						i = i + 1

					if i == 1:

						svars.ProdComp1 = producto_nombre[num]
						svars.PrecioComp1 = producto_precio[num]
						svars.ImgComp1= producto_COMPimagen[num]
						svars.CaracComp1= producto_caracticas[num]

					if i >= 2:


						svars.ProdComp2 = producto_nombre[num]
						svars.PrecioComp2 = producto_precio[num]
						svars.ImgComp2 = producto_COMPimagen[num]
						svars.CaracComp2 = producto_caracticas[num]



						break

				svars.Trigger_Comp = svars.Trigger_Comp + 1

			elif productos_up >= 3:

				producto_nombre[productos_up] = ""
				producto_caracticas[productos_up] = ""
				producto_precio[productos_up] = ""
				producto_pos[productos_up] = ""



			elif productos_up < 0:

				productos_up = 0