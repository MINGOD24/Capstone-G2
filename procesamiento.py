# CONJUNTOS
NP = {} # set nodos de carga
ND = {} # set nodos de descarga
N_v = {} # set de nodos que puede visitar el barco v
NP_v = {} # set de nodos de carga que pueden ser visitados por el barco v
ND_v = {} # set de nodos de descarga que pueden ser visitados por el barco v
A_v = {} # set de tuplas de nodos que el barco v puede viajar
Puertos_i = {} # set de puertos para cada nodo

# PARAMETROS
C_i_j_v = {} # costo zarpar de i a j usando barco v
CS_i = {} # costo Spot
K_v = {} # capacidad que posee cada barco

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
            CS_i[id] = costoSpot
            Puertos_i[id] = puertoOrigen
            Puertos_i[id + 60] = puertoDestino
        contador += 1


with open("Barcos.csv", encoding="utf-8") as archivo:
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
            K_v[id_barco] = capacidad
        contador += 1


with open("CompatibilidadCargos.csv", encoding="utf-8") as archivo:
    lista_nodos_barcos = []
    contador = 0
    for linea in archivo:
        a = linea.strip().split(";")
        id_barco = a[0]
        nodos_descarga = []
        nodos_carga = a[1:]
        for cargo in nodos_carga:
            nodos_descarga.append(cargo + 60)
        if contador == 0:
            pass
        else:
            N_v[id_barco] = nodos_carga + nodos_descarga + [f"O({id_barco})"] + [f"D({id_barco})"] # Todos los nodos en los cuales puede estar un barco
            NP_v[id_barco] = nodos_carga
            ND_v[id_barco] = nodos_descarga
            lista_nodos =  N_v[id_barco]
            lista_tuplas = []
            for nodo in lista_nodos:
                if nodo == f"D({id_barco})":
                    continue
                for nodo1 in lista_nodos:
                    lista_tuplas.append(tuple(nodo,nodo1))
                    lista_nodos_barcos.append(tuple(nodo,nodo1,id_barco)


            A_v[id_barco] = lista_tuplas
        contador += 1


with open("Costo - Tiempos Puertos.csv", encoding="utf-8") as archivo:
    contador = 0
    for linea in archivo:
        a = linea.strip().split(";")
        id_barco = a[0]
        id_cargo = a[1]
        tiempo_origen = a[2]
        costo_origen = a[3]
        tiempo_destino = a[4]
        costo_destino = a[5]

        if contador == 0:
            pass
        else:
            if costo_origen != -1:
                    C_i_j_v[tuple(id_cargo, id_cargo + 60, id_barco)] = costo_origen 
            else:
                pass


                
        contador +=1
        