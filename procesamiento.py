from datetime import datetime
start_time = datetime.now()

# cada cargo son dos nodos

# CONJUNTOS PROBLEMA
N_v = {} # {id_barco: nodos carga, descarga, O, D} --> nodos que puede visitar el barco v
NP_v = {} # {id_barco: nodos carga} --> nodos de carga que puede visitar el barco v
ND_v = {} # {id_barco: nodos descarga} --> nodos de descarga que puede visitar el barco v
A_v = {} # {id_barco: (nodo_carga, nodo_descarga)} --> tuplas de nodos que el barco v puede viajar

# CONJUNTOS CREADOS
Puertos_i = {} # {id_nodo: puerto} --> para nodos de carga y descarga
Tiempos_i = {} # rango de tiempo para cargar o descargar el nodo i
Tiempos_v = {} # Tiempo de inicio del barco v
Tamano_i = {} # tamaño del cargo i
CP_i_j_v = {} # costo de ir de un puerto i a un puerto j con el barco v
TP_i_j_v = {} # tiempo de ir de un puerto i a un puerto j con el barco v

# PARAMETROS
C_i_j_v = {} # {(id_cargo, id_cargo, id_barco): costo_origen}
T_i_j_v = {} # {(id_cargo, id_cargo, id_barco): costo_origen}
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
            CS_i[int(id)] = costoSpot
            Puertos_i[int(id)] = puertoOrigen
            Tamano_i[int(id)] = tamano
            Puertos_i[int(id) + 60] = puertoDestino
            Tiempos_i[int(id)] = tuple([LTCarga, RTCarga])
            Tiempos_i[int(id) + 60] = tuple([LTDescarga, RTDescarga])
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
            Puertos_i[f"O({id_barco})"] = puerto_inicio
            Puertos_i[f"D({id_barco})"] = f"D({id_barco})"
            Tiempos_v[int(id_barco)] = tiempo_inicio
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
        nodos_carga = [x for x in nodos_carga if x != '']
        if contador == 0:
            pass
        else:
            for cargo in nodos_carga:
                nodos_descarga.append(int(cargo) + 60)
            lista_nodos = nodos_carga + nodos_descarga + [f"O({id_barco})"] + [f"D({id_barco})"] # Todos los nodos en los cuales puede estar un barco
            N_v[id_barco] = lista_nodos
            NP_v[id_barco] = nodos_carga
            ND_v[id_barco] = nodos_descarga
            lista_tuplas = []
            for nodo in lista_nodos:
                if nodo == f"D({id_barco})":
                    continue
                for nodo1 in lista_nodos:
                    lista_tuplas.append(tuple([nodo,nodo1]))
                    lista_nodos_barcos.append(tuple([nodo,nodo1,id_barco])) # todas las combinaciones que pueden hacer todos los barcos

            A_v[id_barco] = lista_tuplas # para el barco en cuestión, todas las tuplas posibles

        contador += 1


        
# inicializar dict
for tupla in lista_nodos_barcos:
    C_i_j_v[tupla] = 0
    id_barco = tupla[2]
    try:
        p_origen = Puertos_i[int(tupla[0])]
    except:
        p_origen = Puertos_i[tupla[0]]
    try:
        p_destino = Puertos_i[int(tupla[1])]
    except:
        p_destino = Puertos_i[tupla[1]]
    CP_i_j_v[tuple([p_origen, p_destino, id_barco])] = 0
    TP_i_j_v[tuple([p_origen, p_destino, id_barco])] = 0


with open("Costo-Tiempos-Puertos.csv", encoding="utf-8") as archivo:
    contador = 0
    for linea in archivo:
        a = linea.strip().split(";")
        id_barco = a[0]
        id_cargo_carga = a[1]
        tiempo_origen = a[2]
        costo_carga = a[3]
        tiempo_destino = a[4]
        costo_descarga = a[5]

        if contador == 0:
            pass
        else:
            id_cargo_descarga = int(a[1]) + 60
            if costo_carga != -1:
                # en esta parte se agrega al dicc los costos de carga y descarga
                # luego hay que agregar el costo de transporte para todas las combinaciones
                
                #caso carga
                lista_factibles_cargas = [(i,j,v) for (i,j,v) in lista_nodos_barcos if j == id_cargo_carga and v == id_barco]
                for caso_cargas in lista_factibles_cargas:
                    C_i_j_v[caso_cargas] += int(costo_carga) 
                
                #caso descarga
                lista_factibles_descargas = [(i,j,v) for (i,j,v) in lista_nodos_barcos if j == id_cargo_descarga and v == id_barco]
                for caso_descarga in lista_factibles_descargas:
                    C_i_j_v[caso_descarga] += int(costo_descarga) 


            else:
                pass
                
        contador +=1


with open("Costos-Transporte.csv", encoding="utf-8") as archivo:
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
            TP_i_j_v[tuple([id_puerto_origen, id_puerto_destino, id_barco])] = tiempo_viaje
            CP_i_j_v[tuple([id_puerto_origen, id_puerto_destino, id_barco])] = int(costo_viaje)

        contador +=1
for tupla in lista_nodos_barcos:
    id_barco = tupla[2]
    try:
        p_origen = Puertos_i[int(tupla[0])]
    except:
        p_origen = Puertos_i[tupla[0]]
    try:
        p_destino = Puertos_i[int(tupla[1])]
    except:
        p_destino = Puertos_i[tupla[1]]
    C_i_j_v[tupla] += CP_i_j_v[tuple([p_origen, p_destino, id_barco])]
    T_i_j_v[tupla] = TP_i_j_v[tuple([p_origen, p_destino, id_barco])]


end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))



# print(T_i_j_v[('1', '5', '1')])
# print(C_i_j_v[('1', '5', '1')])

# dict_items = C_i_j_v.items()

# first_two = list(dict_items)[:30]
# print(first_two)


# print(Puertos_i) # {id_nodo: puerto} --> para nodos de carga y descarga
# print(N_v)  # {id_barco: nodos carga, descarga, O, D} --> nodos que puede visitar el barco v
# print(NP_v) # {id_barco: nodos carga} --> nodos de carga que puede visitar el barco v
# print(ND_v) # {id_barco: nodos descarga} --> nodos de descarga que puede visitar el barco v
# print(A_v)  # {id_barco: (nodo_carga, nodo_descarga)} --> tuplas de nodos que el barco v puede viajar
# print(C_i_j_v)  # {(id_cargo, id_cargo + 60, id_barco): costo_origen}