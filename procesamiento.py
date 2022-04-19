from classes import *


with open("Barcos.csv", encoding="utf-8") as archivo:
    V = []
    contador = 0
    for linea in archivo:
        a = linea.strip().split(";")
        id_barco = a[0]
        puerto_inicio = a[1]
        tiempo_inicio = a[2]
        capacidad = a[3]
        if contador == 0:
            pass
        else:
            barco = Barco(id_barco, puerto_inicio, tiempo_inicio, capacidad)
            V.append(barco)
        contador += 1
    Kv = []
    for boat in V:
        Kv.append(boat.capacidad)


with open("Cargo.csv", encoding="utf-8") as archivo:
    lista_cargos = []
    contador = 0
    for linea in archivo:
        a = linea.strip().split(";")
        id = a[0]
        puertoOrigen = a[1]
        puertoDestino = a[2]
        tamano = a[3]
        costoSpot = a[4]
        LTCarga = a[5]
        RTCarga = a[6]
        LTDescarga = a[7]
        RTDescarga = a[8]
        if contador == 0:
            pass
        else:
            cargo = Cargo(id, puertoOrigen, puertoDestino, tamano, costoSpot, LTCarga, RTCarga, LTDescarga, RTDescarga)
            lista_cargos.append(cargo)
        contador += 1
    contador2 = 1
    NP = []
    ND = []
    for cargoe in lista_cargos:
        cargo = CargoCarga(contador2, cargoe.id, cargoe.puertoOrigen, cargoe.tamano, cargoe.costoSpot, cargoe.LTCarga, cargoe.RTCarga, cargoe.LTDescarga, cargoe.RTDescarga)
        NP.append(cargo)
        contador2 += 1
    for cargoe in lista_cargos:
        cargo = CargoDescarga(contador2, cargoe.id, cargoe.puertoOrigen, cargoe.tamano, cargoe.costoSpot, cargoe.LTCarga, cargoe.RTCarga, cargoe.LTDescarga, cargoe.RTDescarga)
        ND.append(cargo)
        contador2 += 1
    
        
    


with open("Puertos.csv", encoding="utf-8") as archivo:
    lista_puertos = []
    contador = 0
    for linea in archivo:
        a = linea.strip().split(";")
        id = a[0]
        nombre = a[1]
        longitud = a[2]
        latitud = a[3]
        if contador == 0:
            pass
        else:
            puerto = Puerto(id, nombre, longitud, latitud)
            lista_puertos.append(puerto)
        contador += 1


with open("CompatibilidadCargos.csv", encoding="utf-8") as archivo:
    NV = []
    contador = 0
    for linea in archivo:
        a = linea.strip().split(";")
        id_barco = a[0]
        cargos = a[1:]
        cargos = [x for x in cargos if x != '']
        barco = [x for x in V if x.id == id_barco]
        if contador == 0:
            pass
        else:
            comp = CompatibilidadCargo(barco, cargos)
            NV.append(comp)
        contador += 1
    NPV = [x for x in NP for y in NV if x.idOriginal in y.cargos] 
    for x in NPV:
        print("-----------\n\n")
        print(x.idOriginal)

