# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
    
import csv

lista_database = [] #Para almacenar toda la info del archivo

with open("synergy_logistics_database.csv", "r") as archivo_csv:
    lector = csv.DictReader(archivo_csv)
    
    for linea in lector: 
        lista_database.append(linea)

total_exportaciones = []

#OPCION 1: Contar el número de exportaciones e importaciones por ruta 
def rutas_export_import(direccion): #Funcion para contar cuántas exportaciones o importaciones hubieron
    contador = 0
    rutas_ya_contadas = [] #Almaceno las rutas ya contadas para evitar contar dos veces la misma ruta
    rutas_con_conteo = []
    
    for ruta in lista_database:
        if ruta["direction"] == direccion:
            ruta_actual = [ruta["origin"], ruta["destination"]]

        
            if ruta_actual not in rutas_ya_contadas: #Checo que no la haya contado antes
                for ruta_enlistada in lista_database:
                    if ruta_actual == [ruta_enlistada["origin"], ruta_enlistada["destination"]] and ruta_enlistada["direction"]==direccion: #Vuelvo a verificar la direccion
                        contador +=1 #Voy sumando uno cada vez que sale la ruta
                rutas_ya_contadas.append(ruta_actual)
                rutas_con_conteo.append([ruta["origin"], ruta["destination"], contador]) #Agrego la ruta con formato 
                contador = 0
    
    rutas_con_conteo.sort(reverse = True, key = lambda x:x[2]) #ORdeno de mayor a menor
    
    totales = []
    for valor in rutas_con_conteo:
        totales.append(valor[2]) #Argego solo el numero de veces
    
    return rutas_con_conteo[0:10],sum(totales), len(rutas_con_conteo) #Solo mando las primeras 10 las más demandadas

rutas_exp, total_exp, total_de_rutas_exp = rutas_export_import("Exports") #Asigno a una variabla cada valor que me regresa la función para poder usarlo después
rutas_imp, total_imp, total_de_rutas_imp = rutas_export_import("Imports")

rutas_imp_exp_totales = total_de_rutas_exp + total_de_rutas_imp

#Para contar tomando en cuenta valores
def rutas_export_import_value(direccion): #Funcion igual a la anterior pero en vez de sumar 1 al contador, va sumando los valores 
    contador_values = 0
    rutas_ya_contadas = []
    rutas_con_conteo = []
    
    for ruta in lista_database:
        if ruta["direction"] == direccion:
            ruta_actual = [ruta["origin"], ruta["destination"]]

        
            if ruta_actual not in rutas_ya_contadas:
                for ruta_enlistada in lista_database:
                    if ruta_actual == [ruta_enlistada["origin"], ruta_enlistada["destination"]] and ruta_enlistada["direction"]==direccion:
                        contador_values += int(ruta_enlistada["total_value"])
                rutas_ya_contadas.append(ruta_actual)
                rutas_con_conteo.append([ruta["origin"], ruta["destination"], contador_values])
                contador_values = 0
    
    rutas_con_conteo.sort(reverse = True, key = lambda x:x[2])
           
    totales = []
    for valor in rutas_con_conteo:
        totales.append(valor[2])
           
    return rutas_con_conteo[0:10], sum(totales)
    

rutas_value_exp, total_value_exp = rutas_export_import_value("Exports")
rutas_value_imp, total_value_imp = rutas_export_import_value("Imports")


#Comparar si las rutas más demandadas fueron de las que más valor aportaron a la empresa:
#Para exportación: 
lista_sin_num = [] 
for ruta in rutas_exp:
    lista_sin_num.append((ruta[0],ruta[1])) #Le quito el valor del índice 2 para poder comparar solo las rutas

lista_sin_num_value = []
for ruta in rutas_value_exp:
    lista_sin_num_value.append((ruta[0],ruta[1])) #Le quito el valor del índice 2 para poder comparar solo las rutas


#Para importación (lo mismo que antes): 
lista_imp_sin_num = []
for ruta in rutas_imp:
    lista_imp_sin_num.append((ruta[0],ruta[1]))

lista_imp_sin_num_value = []
for ruta in rutas_value_imp:
    lista_imp_sin_num_value.append((ruta[0],ruta[1]))


#OPCION 2: Transportes más usados
transportes = [] 

for lista in lista_database: #Para sacar los diferentes transportes en la lista
    transporte = lista["transport_mode"]
    if transporte not in transportes:
        transportes.append(transporte)

def f_transporte(modo_de_transporte): 
    
    contador = 0
    contador_valores = 0
    
    for linea in lista_database:
        transporte = linea["transport_mode"]
        if transporte == modo_de_transporte:
            contador += 1 #Contar cuántas veces se usó cada transporte
            contador_valores += int(linea["total_value"]) #Sumar el valor aportado por transporte
    transporte_en_lista = (modo_de_transporte, contador, contador_valores) #Formato con tipo de transporte, # de veces y valor

    return transporte_en_lista

lista_transportes = [] #Lista para agregar todos los diferentes transportes y sus valores

for transporte in transportes:
    lista_transportes.append(f_transporte(transporte)) #Llamo a la función

lista_transportes.sort(reverse = True, key = lambda x:x[1]) #Ordeno según las veces que se usó cada transporte
    
productos = [] 

for lista in lista_database: #Sacar los diferentes productos en la lista
    producto = lista["product"]
    if producto not in productos: #Evita agregar productos repetidos
        productos.append(producto)

#Ahora sabemos que "air" y "road" son los transportes menos usados, para ver si se podría eliminar uno vemos los productos que transportan:
#Función para ver qué productos transporta cada uno de estos dos medios:
def producto_transportado(producto,transporte_enviado):
    contador = 0
    
    for transporte in lista_database:
        if transporte["transport_mode"] == transporte_enviado:
            if transporte ["product"] == producto:
                contador += 1 #Cuenta los productos transportados
    producto_enlistado = [transporte_enviado, producto, contador]

    return producto_enlistado
    
lista_productos_transportados_air = [] #Sacamos los transportados por aire/air
for producto in productos:
    lista_productos_transportados_air.append(producto_transportado(producto, "Air"))

lista_productos_transportados_road = [] #Sacamos los transportados por tierra/road
for producto in productos:
    lista_productos_transportados_road.append(producto_transportado(producto, "Road"))

lista_productos_transportados_air.sort(reverse = True, key = lambda x:x[2]) #Ordeno según el número de transportados
lista_productos_transportados_road.sort(reverse = True, key = lambda x:x[2])


#OPCION 3: Valor total de las importaciones y exportaciones, tomando en cuenta el 80%
lista_paises = []

for lista in lista_database: #Busco los países que hay en la lista
    if lista["direction"] == "Exports": #Si es exportacion me importa el pais de origen
        if lista["origin"] not in lista_paises: #Evito repetir paises
            lista_paises.append(lista["origin"])
    else: #Si es importacion me importa el pais de destino
        if lista["destination"] not in lista_paises: #Evito repetir paises
            lista_paises.append(lista["destination"])
 
def conteo_paises(pais): #Funcion para sumar el valor que aportó cada país
    contador = 0
    
    for lista in lista_database:
        if lista["direction"] == "Exports" and lista["origin"] == pais: #Verifico direccion y pais
            contador += int(lista["total_value"]) #Le agrego el valor por pais
        elif lista["direction"] == "Imports" and lista["destination"] == pais: 
            contador += int(lista["total_value"])
    
    pais_contado = [pais, contador] #Formato: pais, valor que aportó
    return pais_contado

lista_paises_con_valores = [] #Para almacenar todos los países con su respectivo valor

for pais in lista_paises:
    lista_paises_con_valores.append(conteo_paises(pais)) #Llamo a la función

lista_paises_con_valores.sort(reverse = True, key = lambda x:x[1]) #Ordeno la lista

#Saco el total de todos los países
total_de_totales = []

for dato in lista_paises_con_valores:
    total_de_totales.append(int(dato[1])) #Agrego a la lista solo el valor por país

total_final = (sum(total_de_totales)) #Saco el total del valor 
 
limite_porcentaje = round(total_final*0.8,0) #El límite será el 80% del total del valor

suma = 0
paises_ochenta_p = [] #Lista para agregar solo los países que formen parte del 80%

for lista in lista_paises_con_valores:
    if suma <= limite_porcentaje: #Verifica que no se haya pasado del límite de 80%
        suma += lista[1] #Suma el valor del pais
        paises_ochenta_p.append(lista[0]) #Agrega el país que sí entra en el 80% a la lista

                        
#Extra: para sacar el porcentaje que representa cada pais:
def porcentaje_pais(pais):
    for pais_enlistado in lista_paises_con_valores:
        if pais == pais_enlistado[0]: #Verifica correspondencia del país recibido con la lista
            porcentaje = round(100*pais_enlistado[1]/total_final,3) #Saca el % por país
            pais_formato = (pais, porcentaje)
    
    return pais_formato

lista_paises_porcentaje = [] #Para tener todos los países con sus respectivos porcentajes

for pais in lista_paises:
    lista_paises_porcentaje.append(porcentaje_pais(pais))

lista_paises_porcentaje.sort(reverse = True, key = lambda x:x[1]) #Ordena según el %

#MENU
print("Hola, bienvenido\n")

opcion_elegida = 0

while opcion_elegida != "s":
    print("\n¿Qué deseas hacer?\n\n1. Mostrar las 10 rutas más demandadas\n2. Mostrar el análisis de los medios de transporte\n3. Mostrar los países que generan el 80% del valor de importaciones y exportaciones")
    opcion_elegida = input("\nElige una opción (1/2/3 o s para salir) ")
    if opcion_elegida == "1":
        while opcion_elegida != "r":
            print("\nEl número total de rutas de importación y exportación fue de ", rutas_imp_exp_totales)
            print("\nDe las ", total_de_rutas_exp, " rutas de exportación,\n")
            print("Las 10 rutas de exportación más demandadas fueron:")
            
            for ruta_exp in rutas_exp:
                print (ruta_exp)
            
            print("\nEl número total de exportaciones fue de: ", total_exp)

            print("\nDe las ", total_de_rutas_imp, " rutas de importación,\n")
            print("\nLas 10 rutas de importación más demandadas fueron:")
            for ruta_imp in rutas_imp:
                print (ruta_imp)
            
            print("\nEl número total de importaciones fue de: ", total_imp)
            
            
            print("\nLas 10 rutas de exportación más importantes según el valor que aportaron fueron:")

            for ruta_value_exp in rutas_value_exp:
                print (ruta_value_exp)
            
            print("\nEl valor total de exportaciones fue de: ", total_value_exp)
            
            print("\nLas 10 rutas de importación más importantes según el valor que aportaron fueron:")
            for ruta_value_imp in rutas_value_imp:
                print (ruta_value_imp)
            
            print("\nEl valor total de importaciones fue de: ", total_value_imp)
            
            print("\nDe las rutas de exportación más demandadas,") #Para ver si las más usadas son las que aportaron más valor
            for ruta_demandada in lista_sin_num:
                if ruta_demandada in lista_sin_num_value:
                    print("La ruta", ruta_demandada, "sí fue de las que aportaron más valor")
                else:
                    print("La ruta", ruta_demandada, "no fue de las que aportaron más valor")
           
            print("\nDe las rutas de importación más demandadas,")
            for ruta_demandada in lista_imp_sin_num:
                if ruta_demandada in lista_imp_sin_num_value:
                    print("La ruta", ruta_demandada, "sí fue de las que aportaron más valor")
                else:
                    print("La ruta", ruta_demandada, "no fue de las que aportaron más valor")
            
            
            opcion_elegida = input("\nPresiona r para regresar al menú principal ")
            
    elif opcion_elegida == "2":
        while opcion_elegida != "r":
            print("\nLos transportes ordenados según su frecuencia de uso fueron: ")
            
            for transporte_usado in lista_transportes:
                print(transporte_usado)
                
            lista_transportes.sort(reverse = True, key = lambda x:x[2]) #Ahora ordeno según el valor aportado
            
            print("\nLos transportes ordenados según el valor que aportaron fueron: ")
            
            for transporte_usado in lista_transportes:
                print(transporte_usado)
            
            print("\nLos productos transportados por aire (Air) fueron:\n")
            for elemento in lista_productos_transportados_air:
                print(elemento[1:3])
            
            print("\nLos productos transportados por tierra (Road) fueron:\n")
            for elemento in lista_productos_transportados_road:
                print(elemento[1:3])
            
            
            opcion_elegida = input("\nPresiona r para regresar al menú principal ")
            
    elif opcion_elegida == "3":
        while opcion_elegida != "r":
            print("\nEl porcentaje que aportó cada país fue de:\n")
            for pais in lista_paises_porcentaje:
                print(pais)
            print("\nLos países que representan el 80% del valor son:\n")
            for pais in paises_ochenta_p:
                print(pais)
            print("\nDichos países aportaron ", suma, " del los ", total_final, " del valor total")
            opcion_elegida = input("\nPresiona r para regresar al menú principal ")
    else:
        print("\nOpción inválida, por favor intenta de nuevo\n")
        print("\n¿Qué deseas hacer?\n\n1. Mostrar las 10 rutas más demandadas\n2. Mostrar el análisis de los medios de transporte\n3. Mostrar los países que generan el 80% del valor de importaciones y exportaciones")
        opcion_elegida = input("\nElige una opción (1/2/3 o s para salir) ")
        
print("Has salido del sistema")

