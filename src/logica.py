import copy

a = {'A8': 'd', 'B8': 'g', 'C8': 0, 'D8': 0, 'E8': 0, 'F8': 0, 'G8': 0, 'H8': 0,    
    'A7': 'R', 'B7': 0, 'C7': 0, 'D7': 0, 'E7': 0, 'F7': 0, 'G7': 0, 'H7': 0,
    'A6': 0, 'B6': 0, 'C6': 0, 'D6':0, 'E6': 0, 'F6': 0, 'G6': 0, 'H6': 0, 
    'A5': 0, 'B5': 0, 'C5': 0, 'D5': 0, 'E5': 0, 'F5': 0, 'G5': 0, 'H5': 0, 
    'A4': 0, 'B4': 0, 'C4': 0, 'D4': 0, 'E4': 0, 'F4': 0, 'G4': 0, 'H4': 0,
    'A3': 0, 'B3': 0, 'C3': 0, 'D3': 0, 'E3': 0, 'F3': 0, 'G3': 0, 'H3': 0, 
    'A2': 0, 'B2': 0, 'C2': 0, 'D2': 0, 'E2': 0, 'F2': 0, 'G2': 0, 'H2': 0, 
    'A1': 'E', 'B1': 'R', 'C1': 0, 'D1': 0, 'E1': 0, 'F1': 0, 'G1': 0, 'H1': 0, 
    'A0': 0, 'A-1': 0, 'B0': 0, 'B-1': 0, 'C0': 0, 'C-1': 0, 'D0': 0, 'D-1': 0, 'E0': 0, 'F0': 0, 'E-1': 0, 'G0': 0, 'F-1': 0, 'H0': 0, 'G-1': 0, 'H-1': 0}

#CREAR UN NODO DEL ARBOL(valor=HEURISTICA)
class Nodo:
    def __init__(self, tablero,profundidad, valor, turnos=4, movimiento=None,indiceH = None):
        self.tablero = tablero  # Tablero del nodo
        self.movimiento = movimiento  # Movimiento realizado para llegar a este nodo
        self.hijos = []  # Lista de nodos hijos
        self.turnos = turnos
        self.profundidad = profundidad
        self.valor = valor 
        self.indiceH = indiceH
        self.cambio = []

#TRAE EN DICCIONARIO LAS COORDENAS DEL TIPO DE FICHA DADO {'A1': 'E', 'B1': 'R'}
def coordenadas_letras(tablero, tipo="minusculas"):
    # Buscar coordenadas y valores según el tipo especificado (minúsculas o mayúsculas)
    if tipo == "minusculas":
        resultado = {k: v for k, v in tablero.items() if isinstance(v, str) and v.islower()}
    elif tipo == "mayusculas":
        resultado = {k: v for k, v in tablero.items() if isinstance(v, str) and v.isupper()}
    else:
        resultado = {}
    return resultado

#BOOLEANO DE SI LETRA1 GANA A LETRA2 EN PRIORIDAD (quien_gana('R','E') = False)
def quien_gana(letra1, letra2):
    # Definir la jerarquía de letras (E > C > H > D > G > R, mayúsculas y minúsculas equivalentes)
    jerarquia = ['E', 'C', 'H', 'D', 'G', 'R']
    
    # Normalizar las letras a mayúsculas para simplificar la comparación
    letra1 = letra1.upper()
    letra2 = letra2.upper()
    
    # Verificar si ambas letras están en la jerarquía
    if letra1 not in jerarquia or letra2 not in jerarquia:
        raise ValueError("Ambas letras deben ser una de: E, C, H, D, G, R")
    
    # Comparar posiciones en la jerarquía
    return jerarquia.index(letra1) < jerarquia.index(letra2)

#SEPARA EN UNA TUPLA LOS VALORES DE COORDENADA ('A', 8)
def extraer_letra_o_numero(cadena):
    # Extraer la letra (primera parte) y el número (segunda parte)
    letra = ''.join(filter(str.isalpha, cadena))
    numero = ''.join(filter(str.isdigit, cadena))
    return letra, int(numero) if numero else None

#VERIFICA SI LA LETRA DE ESA COORDENADA TIENE UN ALIADO ADYACENTE validar_adyacentes_mismo_tipo(a, 'B8') = True
def validar_adyacentes_mismo_tipo(tablero, coordenada):
    bandera = False
    
    # Extraer la letra y número de la coordenada inicial
    letra, numero = extraer_letra_o_numero(coordenada)
    
    # Recorrer los movimientos válidos (arriba, abajo, derecha, izquierda)
    for mov in [0, 1, 2, 3]:
        # Determinar la nueva coordenada según la dirección del movimiento
        if mov == 0:  # Arriba
            nueva_letra = chr(ord(letra))
            nueva_numero = numero + 1
        elif mov == 1:  # Abajo
            nueva_letra = chr(ord(letra))
            nueva_numero = numero - 1
        elif mov == 2:  # Derecha
            nueva_letra = chr(ord(letra) + 1)
            nueva_numero = numero
        elif mov == 3:  # Izquierda
            nueva_letra = chr(ord(letra) - 1)
            nueva_numero = numero

        nueva_coordenada = nueva_letra + str(nueva_numero)

        # Verificar si la nueva coordenada está dentro del tablero
        if nueva_coordenada in tablero:
            casilla_destino = tablero[nueva_coordenada]


            # Asegurarse de que la casilla destino es una cadena antes de llamar a isupper o islower
            if isinstance(casilla_destino, str) and casilla_destino != '0' and tablero[coordenada] !=0 :
                
                
                if (tablero[coordenada].islower() and casilla_destino.islower()) or (tablero[coordenada].isupper() and casilla_destino.isupper()):
                    # print('BANDERA', coordenada,mov,casilla_destino)
                    bandera = True

    return bandera

#DEVUELVE LISTA DE COORDENADAS EN LA QUE LA FICHA DE ESA POS ESTA CONGELADA
def coordenadas_congeladas(tablero):
    # Definir las direcciones adyacentes (arriba, abajo, izquierda, derecha)
    direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    # Crear una lista para las coordenadas congeladas
    congeladas = []

    # Recorrer todas las coordenadas en el tablero
    for coordenada, ficha in tablero.items():
        if isinstance(ficha, str):  # Solo procesar si es una ficha (minúscula o mayúscula)
            letra, numero = extraer_letra_o_numero(coordenada)
            
            # Recorrer las direcciones adyacentes
            for dx, dy in direcciones:
                # Obtener la coordenada adyacente
                nueva_coordenada = chr(ord(letra) + dx) + str(numero + dy)
                
                # Verificar si la coordenada es válida y existe en el tablero
                if nueva_coordenada in tablero:
                    vecino = tablero[nueva_coordenada]
                    
                    if isinstance(vecino, str):  # Si es una ficha (de cualquier tipo)
                        # Evitar comparar la misma ficha (misma letra, sin importar mayúsculas o minúsculas)
                        if ficha.lower() != vecino.lower():
                            # Si la ficha es minúscula y la vecina es mayúscula, evaluar quién gana
                            if ficha.islower() and vecino.isupper() and quien_gana(vecino, ficha):
                                if coordenada not in congeladas:  # Evitar agregar dos veces
                                    congeladas.append(coordenada)  # Solo agregamos la ficha que pierde
                            # Si la ficha es mayúscula y la vecina es minúscula, evaluar quién gana
                            elif ficha.isupper() and vecino.islower() and quien_gana(vecino, ficha):
                                if coordenada not in congeladas:  # Evitar agregar dos veces
                                    congeladas.append(coordenada)  # Solo agregamos la ficha que pierde
    
    # Ahora revisar las coordenadas congeladas y eliminar las que tienen un vecino del mismo tipo
    congeladas_finales = []
    for coordenada in congeladas:
        letra, numero = extraer_letra_o_numero(coordenada)
        ficha = tablero[coordenada]
        
        # Bandera para saber si tiene un vecino del mismo tipo
        tiene_vecino_mismo_tipo = False
        
        # Recorrer las direcciones adyacentes
        for dx, dy in direcciones:
            # Obtener la coordenada adyacente
            nueva_coordenada = chr(ord(letra) + dx) + str(numero + dy)
            
            # Verificar si la coordenada es válida y existe en el tablero
            if nueva_coordenada in tablero:
                vecino = tablero[nueva_coordenada]
                
                if isinstance(vecino, str):  # Si es una ficha (de cualquier tipo)
                    if ficha.islower() == vecino.islower():  # Mismo tipo (mayúscula o minúscula)
                        tiene_vecino_mismo_tipo = True
                        break
        
        # Si tiene un vecino del mismo tipo, no agregarla a las coordenadas congeladas finales
        if not tiene_vecino_mismo_tipo:
            congeladas_finales.append(coordenada)

    return congeladas_finales
congeladas = coordenadas_congeladas(a)
#print("Fichas congeladas:", congeladas)

#RETORNA LISTA DE MOV VALIDOS PARA UNA COORDENADA Y SU FICHA [ARRIBA,ABAJO,DERECHA,IZQ] = [0,1,2,3]
def validaMov(congeladas,coordenada, ficha):

    def extraer_letra_o_numero(cadena):
        # Extraer la letra (primera parte) y el número (segunda parte)
        letra = ''.join(filter(str.isalpha, cadena))
        numero = ''.join(filter(str.isdigit, cadena))
        return letra, int(numero) if numero else None

    letraCoor, num = extraer_letra_o_numero(coordenada)

    movimientosValidos = set([0, 1, 2, 3])  # arriba, abajo, derecha, izquierda

    #quitarCongeladas:
    if coordenada in congeladas:
        movimientosValidos.discard(0)
        movimientosValidos.discard(1)
        movimientosValidos.discard(2)
        movimientosValidos.discard(3)

    # Conejo (r, R) no se devuelve
    if ficha == 'r':
        movimientosValidos.discard(0)  # colores no pueden subir
    elif ficha == 'R':
        movimientosValidos.discard(1)  # Grises no pueden bajar

    # LIMITES MAPAS
    if letraCoor == 'A':
        movimientosValidos.discard(3)  # No puede ir IZQ
    if letraCoor == 'H':
        movimientosValidos.discard(2)  # No puede ir DER
    if num == 8:
        movimientosValidos.discard(0)  # No puede Subir
    if num == 1:
        movimientosValidos.discard(1)  # No puede Bajar


    return list(movimientosValidos)

movPrueba = (validaMov(congeladas,'B8','g'))
#print(movPrueba)

#EFECTUA EL MOV EN EL TABLERO Y RETORNA LOS CAMBIOS [[['B8', 0, None], ['B7', 'g', 1], [3]], [['B8', 0, None], ['C8', 'g', 2], [3]]]
def mover(coordenada, ficha, movimientos_validos, tablero, turno):

    
    # blue_coordinates = ["C3", "F3", "C6", "F6"]

    movimientos_realizados = []  # Lista para almacenar los movimientos realizados
    
    # Extraer la letra y número de la coordenada inicial
    letra, numero = extraer_letra_o_numero(coordenada)
    
    # Recorrer los movimientos válidos
    for mov in movimientos_validos:

        
        # Determinar la nueva coordenada según la dirección del movimiento
        if mov == 0:  # Arriba
            nueva_letra = chr(ord(letra))
            nueva_numero = numero + 1
        elif mov == 1:  # Abajo
            nueva_letra = chr(ord(letra))
            nueva_numero = numero - 1
        elif mov == 2:  # Derecha
            nueva_letra = chr(ord(letra)+1)
            nueva_numero = numero
        elif mov == 3:  # Izquierda
            nueva_letra = chr(ord(letra)-1)
            nueva_numero = numero
        
        nueva_coordenada = nueva_letra + str(nueva_numero)
        
        # Verificar si la nueva coordenada está dentro del tablero
        if nueva_coordenada in tablero:
            casilla_destino = tablero[nueva_coordenada]
            
            # Comprobar si la casilla de destino es válida
            if casilla_destino == 0:  # Si la casilla está vacía (0)
                # Agregar el movimiento a la lista de movimientos realizados
                
                totalM = []

                # print("COORDENADA MOV",coordenada, tablero)
                totalM.append([coordenada, 0, None]) #VACIAR LA COORDENA EN LA QUE ESTABA
                totalM.append([nueva_coordenada, ficha, mov]) #MOVERSE A LA NUEVA CASILLA
                totalM.append([turno-1])
                
                
                # if(nueva_coordenada in blue_coordinates):
                #     junta = validar_adyacentes_mismo_tipo(tablero, nueva_coordenada)
                    
                #     if not(junta):
                #         totalM.append([nueva_coordenada,0,'ELIMINADA'])

                movimientos_realizados.append(totalM)

                # print(tablero)
            elif isinstance(casilla_destino, str):
                
                # SON FICHAS RIVALES ??
                if (ficha.islower() and casilla_destino.isupper()) or (ficha.isupper() and casilla_destino.islower()):
                    
                    
                    if(turno>=2 and (quien_gana(ficha,casilla_destino))):
                        # Extraer la letra y número de la coordenadaNueva
                        letraN, numeroN = extraer_letra_o_numero(nueva_coordenada)
                        
                        # Recorrer los movimientos válidos
                        for movN in [0,1,2,3]:
                            # Determinar la nueva coordenada según la dirección del movimiento
                            if movN == 0:  # Arriba
                                nueva_letraN = chr(ord(letraN))
                                nueva_numeroN = numeroN + 1
                            elif movN == 1:  # Abajo
                                nueva_letraN = chr(ord(letraN))
                                nueva_numeroN = numeroN - 1
                            elif movN == 2:  # Derecha
                                nueva_letraN = chr(ord(letraN)+1)
                                nueva_numeroN = numeroN
                            elif movN == 3:  # Izquierda
                                nueva_letraN = chr(ord(letra)-1)
                                nueva_numeroN = numeroN

                            nueva_nueva_coordenada = nueva_letraN + str(nueva_numeroN)
                            
                            # Verificar si la nueva coordenada está dentro del tablero
                            if nueva_nueva_coordenada in tablero:
                                casilla_nueva_destino = tablero[nueva_nueva_coordenada]
                                
                                # Comprobar si la casilla de destino es válida
                                if casilla_nueva_destino == 0:  # Si la casilla está vacía (0)
                                    # Agregar el movimiento a la lista de movimientos realizados
                                    totalMov = []
                                    totalMov.append([coordenada, 0, None,'aaaa']) #VACIAR LA ACTUAL
                                    totalMov.append([nueva_coordenada, ficha, mov,'aaaa']) #MOVERME A DONDE MI ENEMIGO
                                    totalMov.append([nueva_nueva_coordenada, casilla_destino, movN,'aaaa'])#ENIMIGO EMPUJADO A ADYACENTE VACIA
                                    totalMov.append([turno-2])


                                    # if(nueva_coordenada in blue_coordinates):
                                    #     juntaN = validar_adyacentes_mismo_tipo(tablero,nueva_coordenada)
                                    #     print(nueva_coordenada, juntaN)
                                    #     if not (juntaN):
                                    #         totalMov.append([nueva_coordenada,0,'ELIMINADA'])
                                    # elif(nueva_nueva_coordenada in blue_coordinates):
                                    #     juntaN = validar_adyacentes_mismo_tipo(tablero,nueva_nueva_coordenada)
                                    #     print(nueva_coordenada, juntaN)
                                    #     if not (juntaN):
                                    #         totalMov.append([nueva_nueva_coordenada,0,'ELIMINADA'])

                                    movimientos_realizados.append(totalMov)

                                    # break  TODOS LOS HIJOS DE
                        
    # Devolver la lista de movimientos realizados
    return movimientos_realizados

movPrueba2 = mover('B8', 'g',movPrueba,a,4)
#print(movPrueba2)

#ACTUALIZAR CAMBIO DE FICHA EN EL TABLERO
def actualizar_tablero(tablero, coordenada, valor):
    """
    Actualiza el tablero con un nuevo valor en la coordenada especificada.

    Parámetros:
        tablero (dict): El tablero representado como un diccionario.
        coordenada (str): La clave del tablero donde se actualizará el valor.
        valor (str/int): El nuevo valor a asignar en la coordenada.

    Retorna:
        dict: El tablero actualizado.
    """
    if coordenada in tablero:  # Verificar si la coordenada existe en el tablero
        
        tablero[coordenada] = valor

    
        
        blue_coordinates = ["C3", "F3", "C6", "F6"]

        if(coordenada in blue_coordinates):
            junta = validar_adyacentes_mismo_tipo(tablero, coordenada)
            if not (junta):
                print(tablero[coordenada],'Eliminado por estar ', coordenada)
                tablero[coordenada] = '0'

    else:
        print(f"Error: La coordenada '{coordenada}' no existe en el tablero.")


    
    return tablero

#RETORNA EN UNA LISTA LOS HIJOS DE UN NODO, LOS ELEMENTOS DE LA LISTA SON A SU VEZ NODOS
def hijos(board_status,raizOriginal,contadorTurno=4, depth=0, jugador='-inf'):

    #Creo el nodo del arbol, que es el tablero que ingresa.
    tableroOriginal = copy.deepcopy(board_status)
    # raiz = Nodo(copy.deepcopy(board_status),depth,float(jugador))
    raiz = copy.deepcopy(board_status)

    listaHijos = []

    #INF(MIN) TRAE FICHAS DE INF(MATUSCULAS)
    if(jugador=='inf'):
        de = 'mayusculas'
    else:
        de = 'minusculas'

    fichasMin = coordenadas_letras(copy.deepcopy(board_status), de)

    congeladas = coordenadas_congeladas(copy.deepcopy(board_status))

    #recorrer cada una de las fichas y hacer sus posibles movimientos
    for c,f in fichasMin.items():

        #PARA CADA FICHA EN UNA POS PRIMERO TRAE LOS MOV QUE PODRIA HACER
        valido = validaMov(congeladas,c,f)
        print(c,f,valido)

        #LISTA DE LOS MOVIENTOS YA HECHOS Y FILTRADOS
        mov = mover(c,f,valido,tableroOriginal,contadorTurno)
        # print("CAMBIOS:", mov)
        
        if(mov != []):
            # print("Mov no VACIO")
            cont = 0

            #cada uno de los movimientos a efectuar
            for i in mov:
                tableroNuevo = copy.deepcopy(board_status)
                print("Cambios----------",i)
                cont2 = 0

                queCambio =[]
                for j in i:
                    #\print("UN cambio", j)
                    if j != i[-1]:
                
                        coordenada = mov[cont][cont2][0]
                        #print('coordenda',coordenada)
                        valor = mov[cont][cont2][1]
                        #print('VALOR',valor)
                        ultM = mov[cont][cont2][2]
                        #print('ULTM', ultM)
                        turnosRes = mov[cont][-1]
                        #print('Tur', turnosRes)
                        tableroNuevo = actualizar_tablero(tableroNuevo,coordenada,valor)
                        queCambio.append(coordenada)
                        

                    cont2 = cont2 + 1
                
                #OBLIGAR A QUE EL TABLERO CAMBIE Y NO SE REPITA EL ESTADO ANTERIOR O LA RAIZ
                if(tableroNuevo != raiz and tableroNuevo != raizOriginal):
                    
                        if(jugador == '-inf'):
                            hijoN = Nodo(tableroNuevo,depth+1, float('inf'),turnosRes,ultM)
                            hijoN.cambio = queCambio
                        else:
                            hijoN = Nodo(tableroNuevo,depth+1, float('-inf'),turnosRes,ultM)
                            hijoN.cambio = queCambio

                        # raiz.hijos.append(hijoN) 
                        listaHijos.append(hijoN) 
                        # print(hijoN.tablero)
                else:
                    print("SE ELIMINA POR QUE YA EXISTE ESE ESTADO",)
                        
                            

                cont = cont + 1


        print('------------')


    # imprimir_arbol(raiz)

    return listaHijos

#ALGORITMO MINIMAX, VA DE PROF 0...A LA DADA POR EL USAURIO.  SE AGREGA AL NODO ARBOL. 
#EN CADA PROFUNDIDAD SE EXPANDE EL NODO Y SE CREAN SUS HIJOS MAS NO SE EXPANDEN SI LLEGA A LA CONDICION DE PARADA.
# EN PARADA MI RAIZ ES LA LISTA DE HIJOS DEL NODO DE LA ULTIMA PORFUNDIDAD POR ESO NO SE EXPANDEN. 
#SIMPLEMNTE QUEDARON CREADOS COMO HIJOS DEL ULTIMO NODO DE LA PORFUNDIDAD DADA 
def recursivo(raiz, raizOriginal, profT, profA, jugador, Arbol,nodoPadre):
    if profA > profT:
        print("TABLERO HEURISTICA",nodoPadre)
        # m = totalHeuristica(raiz[0].tablero)                                 #TOTAL HEURISTICAAAAAAAAAAAAAAAAAAAA AQUI VA  <------
        m = totalHeuristica(nodoPadre)                                 #TOTAL HEURISTICAAAAAAAAAAAAAAAAAAAA AQUI VA  <------
        return  0, m  # No hay nodos adicionales en este nivel

    cantN = 0  # Contador local de nodos creados

    for index,i in enumerate(raiz):
        cantN += 1  # Incrementar la cantidad de nodos en este nivel
        
        if profA == 0:
            print("RAIZ A EXPANDIR:", i)
            hijosN = hijos(i, raizOriginal, 4, profA, jugador)
            print("HIJOS DE RAIZ:", len(hijosN))
            
            for hi in hijosN:
                Arbol.hijos.append(hi)

            # Sumar los nodos creados en niveles inferiores
            can, m = recursivo(Arbol.hijos, raizOriginal, profT, profA + 1, 'inf' if jugador == '-inf' else '-inf', Arbol,i)
            cantN += can
            print("PROF",profA,"NODO",i,"VALOR",m)
            
    
            # Inicializamos las listas para los valores y los índices
            valores = []
            indices = []

            for idx, k in enumerate(hijosN):  # Enumerar para obtener el índice y el valor
                valores.append(k.valor)
                indices.append(idx)  # Guardamos el índice del valor

            print('VALORES HEURISTICAS:', valores)
            print('INDICES:', indices)

            # Ahora, calculamos el valor máximo o mínimo y guardamos el índice correspondiente
            if jugador == '-inf':  # Maximización
                max_val = max(valores)  # Tomar el valor máximo de los hijos
                idx_max = indices[valores.index(max_val)]  # Encontrar el índice del valor máximo
                Arbol.valor = max_val
                Arbol.indiceH = idx_max  # Guardamos el índice del valor máximo
            elif jugador == 'inf':  # Minimización
                min_val = min(valores)  # Tomar el valor mínimo de los hijos
                idx_min = indices[valores.index(min_val)]  # Encontrar el índice del valor mínimo
                Arbol.valor = min_val
                Arbol.indiceH = idx_min  # Guardamos el índice del valor mínimo

            print('HEURISTICA seleccionada:', Arbol.valor)
            print('INDICE:', Arbol.indiceH)


        else:
            print("PROFUNDIDAD ACTUAL:",profA,"- NODO HIJO",index, i.tablero)
            hijosN = hijos(i.tablero, raizOriginal, 4, profA, jugador)
            print("HIJOS:", len(hijosN))

            
            for hi in hijosN:
                i.hijos.append(hi)
            

            # Sumar los nodos creados en niveles inferiores
            can, m = recursivo(i.hijos, raizOriginal, profT, profA + 1, 'inf' if jugador == '-inf' else '-inf', Arbol,i.tablero)
            cantN += can
            print("VALOR HEURISTICA:",m)
            
            if(profA == profT): #ASIGNA A LAS HOJAS
                if(i.valor == float('-inf')):
                    if(m > float('-inf')):  #como es max, pregunta si mi nuevo valor es mayor que el avlor actual del nodo  
                        i.valor = m
                elif(i.valor == float('inf')):
                    if(m < float('inf')):
                        i.valor = m
            else:
                print("valor",i.valor)
                listaV = []
                
                for k in hijosN: 
                    listaV.append(k.valor)
                
                if i.valor == float('-inf'):  # Maximización
                    i.valor = max(listaV)  # Tomar el valor máximo de los hijos
                elif i.valor == float('inf'):  # Minimización
                    i.valor = min(listaV)  # Tomar el valor mínimo de los hijos



                print('LISTAV', listaV)
                print("valor",i.valor)
            


            

    return cantN, m

#IMPRIME ARBOL
def imprimir_arbol(nodo, nivel=0):
    """
    Función recursiva para imprimir un árbol de nodos.
    
    Parámetros:
        nodo (Nodo): El nodo a imprimir.
        nivel (int): Nivel de profundidad actual en el árbol (para formatear la impresión).
    """
    # Imprimir la información del nodo actual
    print(f"{'  ' * nivel}Nodo en nivel {nivel}: {nodo.tablero}")
    
    # Si el nodo tiene hijos, recorrerlos
    if nodo.hijos:
        for hijo in nodo.hijos:
            imprimir_arbol(hijo, nivel + 1)

# Ejemplo de uso:
# Suponiendo que tienes un nodo raíz 'raiz' y has añadido algunos hijos en su lista 'hijos'


#respuesta = algoritmoMiniMax(a).hijos
# respuesta = miniMaxR(a,4,3)



#----------------------------------------------------------------------- HEURISTICAS -------------------------------------------------------------------------------------------
#  SI NO ENCUENTRO SOLUCION: IA - HUMANO
#SUMAR TODAS LAS HEURISTICAS

def totalHeuristica(tablero):
    # Calcular la heurística total sumando los resultados de las funciones heurísticas
    heuristica_conejos = contar_conejos(tablero)
    heuristica_cuadros_azules = fichas_en_cuadros_azules(tablero)
    heuristica_conejo_meta = conejo_mas_cercano_meta(tablero)
    heuristica_congeladas = contar_fichas_congeladas(tablero)
    
    total = heuristica_conejos + heuristica_cuadros_azules + heuristica_conejo_meta + heuristica_congeladas
    return total

#--CANTIDAD DE FICHAS CONGELADAS
def contar_fichas_congeladas(tablero):
    # Obtener las coordenadas de las fichas congeladas
    congeladas = coordenadas_congeladas(tablero)
    
    # Contar la cantidad de fichas congeladas de la IA (minúsculas) y del humano (mayúsculas)
    cantidad_congeladas_IA = sum(1 for coord in congeladas if tablero[coord].islower())
    cantidad_congeladas_HUMANO = sum(1 for coord in congeladas if tablero[coord].isupper())
    
    # Calcular la diferencia para maximizar las ganancias de la IA
    #HUMANO 1   IA  3   === -2
    #HUMANO 3   IA  1  === 2
    diferencia_congeladas = cantidad_congeladas_HUMANO - cantidad_congeladas_IA
    
    return diferencia_congeladas

#--CONTAR LA CANTIDAD DE CONEJOS si es R o r
def contar_conejos(tablero):
    # Contar la cantidad de conejos (R o r) en el tablero
    cantidad_conejosIA = sum(1 for v in tablero.values() if v in ['r'])   #in ['R'] o para el otro caso #in ['r']
    cantidad_conejosHUMANO = sum(1 for v in tablero.values() if v in ['R'])   #in ['R'] o para el otro caso #in ['r']

    #HUMANO 7   IA  8   === 1   IA COMIO FICHA
    #HUMANO 8   IA  7  === -1   HUMANO COMIO FICHA
    cantidadBunnies = cantidad_conejosIA - cantidad_conejosHUMANO  #
    return cantidadBunnies

#PRUEBA ------>  print("Cantidad HEURISTICA CONEJOS: ",contar_conejos(a))

#--FICHAS EN LOS CUADROS AZULES
def fichas_en_cuadros_azules(tablero):
    # Definir las posiciones de los cuadros azules
    cuadros_azules = ['C6', 'F6', 'C3', 'F3']
    
    # Contar las fichas de la IA y del humano en los cuadros azules
    fichas_IA = sum(1 for pos in cuadros_azules if tablero.get(pos, 0) in ['r', 'g', 'd', 'h', 'c', 'e'])
    fichas_HUMANO = sum(1 for pos in cuadros_azules if tablero.get(pos, 0) in ['R', 'G', 'D', 'H', 'C', 'E'])
    
    #HUMANO 3  IA  1   === 2  
    #HUMANO 1   IA  3  === -2   
    return fichas_HUMANO - fichas_IA

#PRUEBA ------->   contar_conejos(a)

#--ENCUENTRA EL CONEJO MAS CERCANO A LA META
def conejo_mas_cercano_meta(tablero):
    # Inicializar variables para almacenar la menor distancia encontrada
    menor_distancia_IA = float('inf')
    menor_distancia_HUMANO = float('inf')
    
    # Recorrer el tablero para encontrar conejos 'r' y 'R'
    for posicion, valor in tablero.items():
        if valor == 'r':
            # Extraer la letra y el número de la posición
            letra, numero = extraer_letra_o_numero(posicion)
            # Calcular la distancia a la meta (fila 1)
            distancia = numero - 1
            # Si la distancia es menor que la menor distancia encontrada, actualizar la variable
            if distancia < menor_distancia_IA:
                menor_distancia_IA = distancia
        elif valor == 'R':
            # Extraer la letra y el número de la posición
            letra, numero = extraer_letra_o_numero(posicion)
            # Calcular la distancia a la meta (fila 8)
            distancia = 8 - numero
            # Si la distancia es menor que la menor distancia encontrada, actualizar la variable
            if distancia < menor_distancia_HUMANO:
                menor_distancia_HUMANO = distancia
    
    #DISTANCIA CONEJO HUMANO = 7casillas a meta
    #DISTANCIA IA = 1casilla a la meta
    #H=6

    
    #DISTANCIA CONEJO HUMANO = 1casillas a meta
    #DISTANCIA IA = 7casilla a la meta
    #H=-6

    return menor_distancia_HUMANO - menor_distancia_IA

def iniciar(a,profundidad):
    Arbol = Nodo(a,0,'-inf')

    #crear todo el arbol de logica
    respuesta,m = recursivo([a],a,profundidad, 0,'-inf',Arbol,[])
    print("CANTIDAD NODOS",respuesta)
    print('HEURISTICA GANADORA', Arbol.valor)

    for indx, arb in enumerate(Arbol.hijos):
        if(indx == Arbol.indiceH):
            print(arb.tablero)
            print(arb.cambio)
            return(arb.tablero,arb.cambio)

#hola = iniciar(a,1)
# print(hola)
#mprimir_arbol(respuesta)
# print(validar_adyacentes_mismo_tipo(a,'C1'))

