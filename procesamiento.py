# cada cargo son dos nodos

# CONJUNTOS PROBLEMA
N_v = {} # {id_barco: nodos carga, descarga, O, D} --> nodos que puede visitar el barco v
NP_v = {} # {id_barco: nodos carga} --> nodos de carga que puede visitar el barco v
ND_v = {} # {id_barco: nodos descarga} --> nodos de descarga que puede visitar el barco v
A_v = {} # {id_barco: (nodo_carga, nodo_descarga)} --> tuplas de nodos que el barco v puede viajar

# CONJUNTOS CREADOS
Puertos_i = {} # {id_nodo: puerto} --> para nodos de carga y descarga

# PARAMETROS
C_i_j_v = {} # {(id_cargo, id_cargo + 60, id_barco): costo_origen}
CS_i = {} # costo Spot
K_v = {} # {id_barco: capacidad}

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
            lista_nodos = nodos_carga + nodos_descarga + [f"O({id_barco})"] + [f"D({id_barco})"] # Todos los nodos en los cuales puede estar un barco
            N_v[id_barco] = lista_nodos
            NP_v[id_barco] = nodos_carga
            ND_v[id_barco] = nodos_descarga
            lista_tuplas = []
            for nodo in lista_nodos:
                if nodo == f"D({id_barco})":
                    continue
                for nodo1 in lista_nodos:
                    lista_tuplas.append(tuple(nodo,nodo1))
                    lista_nodos_barcos.append(tuple(nodo,nodo1,id_barco)) # todas las combinaciones que pueden hacer todos los barcos

            A_v[id_barco] = lista_tuplas # para el barco en cuestión, todas las tuplas posibles

        contador += 1


        
# inicializar dict
for tupla in lista_nodos_barcos:
    C_i_j_v[tupla] = 0

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
                # en esta parte se agrega al dicc los costos de carga y descarga
                # luego hay que agregar el costo de transporte para todas las combinaciones
                C_i_j_v[tuple(id_cargo, id_cargo + 60, id_barco)] = costo_origen + costo_destino # hay q sumar transporte
            else:
                pass
                
        contador +=1

# pasar a puerto las tuplas posibles
for i in range(len(lista_nodos_barcos)):
    tupla = lista_nodos_barcos[i]
    origen = tupla[0]
    destino = tupla[1]
    barco = tupla[2]
    p_origen = Puertos_i[origen]
    p_destino = Puertos_i[destino]
    tupla_puertos = tuple(p_origen, p_destino, barco)
    lista_nodos_barcos[i] = [tupla, tupla_puertos]


with open("Costos Transporte.csv", encoding="utf-8") as archivo:
    contador = 0
    for linea in archivo:
        a = linea.strip().split(";")
        id_barco = a[0]
        id_puerto_origen = a[1]
        id_puerto_destino = a[2]
        tiempo_viaje = a[3]
        costo_viaje = a[4]

        if contador == 0:
            pass
        else:
            for lista in lista_nodos_barcos:
                tupla_puertos = lista[1]
                tupla_nodos = lista[0]
                puerto_origen = tupla_puertos[0]
                puerto_destino = tupla_puertos[1]
                barco = tupla_puertos[2]
                if id_barco == barco:
                    if id_puerto_origen == puerto_origen and id_puerto_destino == puerto_destino:
                        # si es la tupla que busco 
                        # revisar esto
                        actual = C_i_j_v[tupla_nodos] 
                        actual += costo_viaje
                        C_i_j_v[tupla_nodos] = actual

        contador +=1


# print(Puertos_i) # {id_nodo: puerto} --> para nodos de carga y descarga
# print(N_v)  # {id_barco: nodos carga, descarga, O, D} --> nodos que puede visitar el barco v
# print(NP_v) # {id_barco: nodos carga} --> nodos de carga que puede visitar el barco v
# print(ND_v) # {id_barco: nodos descarga} --> nodos de descarga que puede visitar el barco v
# print(A_v)  # {id_barco: (nodo_carga, nodo_descarga)} --> tuplas de nodos que el barco v puede viajar
# print(C_i_j_v)  # {(id_cargo, id_cargo + 60, id_barco): costo_origen}