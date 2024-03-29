from datetime import datetime
import random
from sqlalchemy import except_
start_time = datetime.now()


##### Se solicita al usuario elegir el set de datos a utilizar ####

print("Enter 1 for the big dataset and 2 for the small dataset:")
setDatos = input()
Datos = 'set' + setDatos

##### Se define la cantidad de nodos que habran dependiendo del set escogido anteriormente ####

if setDatos == '1':
    n = 60
elif setDatos == '2':
    n = 15



##### Se definen los diccionarios y listas que se llenaran a la hora de preprocesar los datos para luego utilizarlos en el modelo ####

# CONJUNTOS PROBLEMA
V = [] # id de los barcos
NP = [] # id de los nodos de carga
N_v = {} # {id_barco: nodos carga, descarga, O, D} --> nodos que puede visitar el barco v
NP_v = {} # {id_barco: nodos carga} --> nodos de carga que puede visitar el barco v
ND_v = {} # {id_barco: nodos descarga} --> nodos de descarga que puede visitar el barco v
A_v = {} # {id_barco: [(nodo_carga, nodo_descarga), (.,.), (.,.), ...]} --> tuplas de nodos que el barco v puede viajar

# CONJUNTOS CREADOS
Puertos_i = {} # {id_nodo: puerto} --> para nodos de carga y descarga
Tiempos_i = {} # rango de tiempo para cargar o descargar el nodo i
Tiempos_v = {} # Tiempo de inicio del barco v
Tamano_i = {} # tamaño del cargo i
CP_i_j_v = {} # costo de ir de un puerto i a un puerto j con el barco v
TP_i_j_v = {} # tiempo de ir de un puerto i a un puerto j con el barco v
Lat_Long_P = {} # (latitud, longitud) del puerto p
Nombre_P = {} # nombre del puerto p
nodos_con_barcos = {}

# PARAMETROS
C_i_j_v = {} # {(id_cargo, id_cargo, id_barco): costo_origen}
T_i_j_v = {} # {(id_cargo, id_cargo, id_barco): costo_origen}
CS_i = {} # costo Spot
K_v = {} # {id_barco: capacidad}



##### Se abre el archivo con la información de cargos ####

with open(f"{Datos}/Cargo.csv", encoding="utf-8") as archivo:
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
            CS_i[int(id)] = int(costoSpot)
            Puertos_i[int(id)] = puertoOrigen
            Tamano_i[id] = tamano
            Puertos_i[int(id) + n] = puertoDestino
            Tiempos_i[id] = tuple([LTCarga, RTCarga])
            Tiempos_i[str(int(id) + n)] = tuple([LTDescarga, RTDescarga])
            NP.append(id)
        contador += 1


##### Se abre el archivo con la información de Barcos ####

with open(f"{Datos}/Barcos.csv", encoding="utf-8") as archivo:
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
            Tiempos_i[f'O({id_barco})'] = tuple([tiempo_inicio, 2000])
            Tiempos_i[f'D({id_barco})'] = tuple([0, 2000])
            Tiempos_v[int(id_barco)] = tiempo_inicio
            K_v[id_barco] = capacidad
            V.append(id_barco)
        contador += 1


##### Se abre el archivo con la información de Puertos ####

with open(f"{Datos}/Puertos.csv", encoding="utf-8") as archivo:
    contador = 0
    for linea in archivo:
        a = linea.strip().split(";")
        id_puerto = a[0]
        nombre_puerto = a[1]
        longitud = a[2]
        latitud = a[3]
        if contador == 0:
            pass
        else:
            Lat_Long_P[int(id_puerto)] = tuple([latitud, longitud])
            Nombre_P[int(id_puerto)] = nombre_puerto
        contador += 1


##### Se abre el archivo con la información de que cargo puede llevar cada barco ####

with open(f"{Datos}/CompatibilidadCargos.csv", encoding="utf-8") as archivo:
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
                nodos_descarga.append(str(int(cargo) + n))
            lista_nodos = nodos_carga + nodos_descarga + [f"O({id_barco})"] + [f"D({id_barco})"] # Todos los nodos en los cuales puede estar un barco
            N_v[id_barco] = lista_nodos
            NP_v[id_barco] = nodos_carga
            ND_v[id_barco] = nodos_descarga
            lista_tuplas = []
            for nodo in lista_nodos:
                nodos_con_barcos[nodo, id_barco] = 0
                if nodo == f'D({id_barco})':
                    continue
                for nodo1 in lista_nodos:
                    if nodo1 == nodo:
                        continue
                    lista_tuplas.append(tuple([nodo,nodo1]))
                    lista_nodos_barcos.append(tuple([nodo,nodo1,id_barco])) # todas las combinaciones que pueden hacer todos los barcos

            A_v[int(id_barco)] = lista_tuplas # para el barco en cuestión, todas las tuplas posibles

        contador += 1


##### Se Inicializan los diccionarios con todas las tuplas posibles factibles ####

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


##### Se abre el archivo con la información de los costos y tiempos de viajes entre puertos ####


with open(f"{Datos}/Costo-Tiempos-Puertos.csv", encoding="utf-8") as archivo:
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
            id_cargo_descarga = int(a[1]) + n
            if costo_carga != -1:
                # en esta parte se agrega al dicc los costos de carga y descarga
                # luego hay que agregar el costo de transporte para todas las combinaciones

                #caso carga
                lista_factibles_cargas = [(i,j,v) for (i,j,v) in lista_nodos_barcos if j == id_cargo_carga and v == id_barco and i != j and i != f'D({id_barco})']
                for caso_cargas in lista_factibles_cargas:
                    C_i_j_v[caso_cargas] += int(costo_carga)
                    T_i_j_v[caso_cargas] = int(tiempo_origen)

                #caso descarga
                lista_factibles_descargas = [(i,j,v) for (i,j,v) in lista_nodos_barcos if j == id_cargo_descarga and v == id_barco and i != j and i != f'D({id_barco})']
                for caso_descarga in lista_factibles_descargas:
                    C_i_j_v[caso_descarga] += int(costo_descarga)
                    T_i_j_v[caso_descarga] = int(tiempo_destino)

            else:
                pass

        contador +=1


##### Se abre el archivo con la información de los costos asociados a transportar los cargos ####


with open(f"{Datos}/Costos-Transporte.csv", encoding="utf-8") as archivo:
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
for tupla in lista_nodos_barcos or tupla[0] == f'D({tupla[2]})':
    if tupla[0] == tupla[1]:
        continue
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
    try:
        T_i_j_v[tupla] += int(TP_i_j_v[tuple([p_origen, p_destino, id_barco])])
    except:
        T_i_j_v[tupla] = int(TP_i_j_v[tuple([p_origen, p_destino, id_barco])])



##### Se finaliza el preprocesamiento y se imprime el tiempo que se demoro en realizarlo ####

end_time = datetime.now()
print('Duración Preprocesamiento: {}'.format(end_time - start_time))



#### Se da inicio al Modelo de Optimización ####

# Importamos los modulos necesarios #
import gurobipy as gp
from gurobipy import GRB

# Creamos el modelo #
m = gp.Model("Asignacion de Rutas optimas para una compania de Transporte Maritimo")
m.Params.TimeLimit = 5  # Desactivar comentario para dar maximo de tiempo de 5 minutos

# Definimos las variables del modelo

x = m.addVars(list(C_i_j_v.keys()), vtype = GRB.BINARY, name = "x_ijv")
y = m.addVars(list(NP), vtype = GRB.BINARY, name = "y_i")
t = m.addVars(nodos_con_barcos, vtype = GRB.CONTINUOUS, name = "t_iv")
l = m.addVars(nodos_con_barcos, vtype = GRB.CONTINUOUS, name = "l_iv")


# Definimos la Funcion Objetivo del modelo
def funcion_objetivo():
    return gp.quicksum(gp.quicksum(C_i_j_v[i, j, v]*x[i, j, v] for i,j in A_v[int(v)]) for v in V) + gp.quicksum(CS_i[int(i)]*y[i] for i in NP)

# Creamos las funciones de las restricciones del modelo

def restriccion_1(i):
    return (gp.quicksum(gp.quicksum(x[i, j, v] for j in N_v[v] if i in NP_v[v] and tuple([i,j,v]) in C_i_j_v) for v in V) + y[i] == 1)

def restriccion_2(v):
    return (gp.quicksum(x[f'O({v})', j, v] for j in N_v[v] if f'O({v})' != j and tuple([f'O({v})',j,v]) in C_i_j_v) == 1)

def restriccion_3(v, i):
    return ((gp.quicksum(x[i, j, v] for j in N_v[v] if tuple([i,j,v]) in C_i_j_v) - gp.quicksum(x[j, i, v] for j in N_v[v] if tuple([j,i,v]) in C_i_j_v)) == 0)

def restriccion_4(v):
    return (gp.quicksum(x[j, f'D({v})', v] for j in N_v[v] if f'D({v})' != j and tuple([j,f'D({v})',v]) in C_i_j_v) == 1)

def restriccion_5(v,i):
    return (gp.quicksum(x[i, j, v] for j in N_v[v] if tuple([i,j,v]) in C_i_j_v) - gp.quicksum(x[str(n + int(i)), j, v] for j in N_v[v] if tuple([str(n + int(i)),j,v]) in C_i_j_v) == 0)

def restriccion_6(v,i):
    return (gp.quicksum(x[i, j, v] for j in N_v[v] if tuple([i,j,v]) in C_i_j_v) - gp.quicksum(x[str(n + int(i)), j, v] for j in N_v[v] if tuple([str(n + int(i)),j,v]) in C_i_j_v) == 0)

def restriccion_7(v, i, j):
    return (t[i,v] + int(T_i_j_v[i, j, v]) - t[j,v] <= (int(Tiempos_i[i][1]) + int(T_i_j_v[i, j, v])) * (1-x[i, j, v]))

def restriccion_8(v, i):
    return (t[i, v] + int(T_i_j_v[i, str(n + int(i)), v]) - t[str(n + int(i)), v] <= 0)

def restriccion_9(v,i):
    return (t[i, v] <= int(Tiempos_i[i][1]))

def restriccion_10(v,i):
    return (t[i,v] >= int(Tiempos_i[i][0]))

def restriccion_11(v,i,j):
    return (l[i, v] + int(Tamano_i[j]) - l[j, v] <= int(K_v[v]) * (1 - x[i, j, v]))

def restriccion_12(v,i,j):
    return (l[i, v] - int(Tamano_i[j]) - l[str(int(j) + n), v] <= int(K_v[v]) * (1 - x[i,str(n + int(j)), v]))

def restriccion_13(v,i):
    return (0 <= l[i, v])

def restriccion_14(v,i):
    return (l[i, v] <= int(K_v[v]))

def restriccion_15(v,i,j):
    return (x[i,j,v] + x[j,i,v] <= 1)


# Asociamos todas las funciones de restricciones al modelo

m.setObjective(funcion_objetivo(), GRB.MINIMIZE)
m.addConstrs(restriccion_1(i) for i in NP)
m.addConstrs(restriccion_2(v) for v in V)
m.addConstrs(restriccion_3(v,i) for v in V for i in N_v[v] if i != f'O({v})' and i != f'D({v})')
m.addConstrs(restriccion_4(v) for v in V)
m.addConstrs(restriccion_5(v,i) for v in V for i in NP_v[v])
m.addConstrs(restriccion_6(v,i) for v in V for i in NP_v[v])
m.addConstrs(restriccion_7(v,i,j) for v in V for i,j in A_v[int(v)])
m.addConstrs(restriccion_8(v,i) for v in V for i in NP_v[v])
m.addConstrs(restriccion_9(v,i) for v in V for i in N_v[v])
m.addConstrs(restriccion_10(v,i) for v in V for i in N_v[v])
m.addConstrs(restriccion_11(v,i,j) for v in V for j in NP_v[v] for i,k in A_v[int(v)] if k == j)
m.addConstrs(restriccion_12(v,i,j) for v in V for j in NP_v[v] for i,k in A_v[int(v)] if k == str(n + int(j)))
m.addConstrs(restriccion_13(v,i) for v in V for i in NP_v[v])
m.addConstrs(restriccion_14(v,i) for v in V for i in NP_v[v])
m.addConstrs(restriccion_15(v,i,j) for v in V for i,j in A_v[int(v)] if tuple([i,j,v]) in C_i_j_v and tuple([j,i,v]) in C_i_j_v)



### IMPLEMENTACIÓN HEURISTICA ###

#Comenzamos con todos los cargos externalizados
for i in NP:
    y[i].lb = 1
    y[i].ub = 1


#Solicitamos al usuario la cantidad de iteraciones para la heuristica
print("Enter the number of iterations to use:")
iteraciones = int(input())

m.setParam("LogToConsole", 0)
m.update() # If you have unstaged changes in the model
m.optimize()

solucion_best = m.copy()
solucion_best.setParam("LogToConsole", 0)
solucion_best.optimize()
iteracion_actual = 0


while iteracion_actual < iteraciones:

    # Copiamos para crear una solucion
    solucion_current = solucion_best.copy()
    solucion_current.setParam("LogToConsole", 0)
    solucion_current.update() # If you have unstaged changes in the model
    solucion_current.optimize()

    # Destruimos la solucion
    lista = []
    for valor in solucion_current.getVars():
        if valor.X == 1:
            lista.append(valor)
    candidatos_a_salir = random.sample(lista, 3) # Tomamos 3 variables
    for variable in candidatos_a_salir:
        variable.lb = 0
        variable.ub = 1

    # Reparammos la solucion
    solucion_current.update()
    solucion_current.optimize()

    for valor in solucion_current.getVars():
        if valor.X == 1:
            valor.lb = 1
            valor.ub = 1
    solucion_current.update()
    solucion_current.optimize()

    print(f"SOLUCION_BEST: {solucion_best.objVal}, SOLUCION_ACTUAL: {solucion_current.objVal}\n\n")
    if solucion_current.objVal < solucion_best.objVal:
        solucion_best = solucion_current.copy()
        solucion_best.update() # If you have unstaged changes in the model
        solucion_best.optimize()
        
    iteracion_actual += 1





#Los siguientes comandos son para imprimir la solucion entregada por el modelo

# m.write("outcont.sol")
# # print(f"Optimal objective value: {m.objVal}")

# m.printAttr('X')
