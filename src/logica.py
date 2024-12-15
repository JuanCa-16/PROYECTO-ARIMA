import copy

class Nodo:
    def __init__(self, tablero, turnos=4, movimiento=None):
        self.tablero = tablero  # Tablero del nodo
        self.movimiento = movimiento  # Movimiento realizado para llegar a este nodo
        self.hijos = []  # Lista de nodos hijos
        self.turnos = turnos


def coordenadas_letras(tablero, tipo="minusculas"):
    # Buscar coordenadas y valores según el tipo especificado (minúsculas o mayúsculas)
    if tipo == "minusculas":
        resultado = {k: v for k, v in tablero.items() if isinstance(v, str) and v.islower()}
    elif tipo == "mayusculas":
        resultado = {k: v for k, v in tablero.items() if isinstance(v, str) and v.isupper()}
    else:
        resultado = {}
    return resultado

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

def extraer_letra_o_numero(cadena):
    # Extraer la letra (primera parte) y el número (segunda parte)
    letra = ''.join(filter(str.isalpha, cadena))
    numero = ''.join(filter(str.isdigit, cadena))
    return letra, int(numero) if numero else None


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
            if isinstance(casilla_destino, str) and casilla_destino != '0':
                if (coordenada.islower() and casilla_destino.islower()) or \
                (coordenada.isupper() and casilla_destino.isupper()):
                    # print('BANDERA', coordenada,mov,casilla_destino)
                    bandera = True

    return bandera


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

        print("NUEVA COORDENADA", nueva_coordenada)
        
        # Verificar si la nueva coordenada está dentro del tablero
        if nueva_coordenada in tablero:
            casilla_destino = tablero[nueva_coordenada]
            print("QUE HAY EN DESTICO", casilla_destino)
            # Comprobar si la casilla de destino es válida
            if casilla_destino == 0:  # Si la casilla está vacía (0)
                # Agregar el movimiento a la lista de movimientos realizados
                totalM = []
                # print("COORDENADA MOV",coordenada, tablero)
                totalM.append([coordenada, 0, None])
                totalM.append([nueva_coordenada, ficha, mov])
                totalM.append([turno-1])

                
                # if(nueva_coordenada in blue_coordinates):
                #     junta = validar_adyacentes_mismo_tipo(tablero, nueva_coordenada)
                    
                #     if not(junta):
                #         totalM.append([nueva_coordenada,0,'ELIMINADA'])

                movimientos_realizados.append(totalM)
            elif isinstance(casilla_destino, str):
                # Verificar si la ficha en la nueva coordenada es del mismo tipo (mayúscula/minúscula)
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
                                    totalMov.append([coordenada, 0, None,'aaaa'])
                                    totalMov.append([nueva_coordenada, ficha, mov,'aaaa'])
                                    totalMov.append([nueva_nueva_coordenada, casilla_destino, movN,'aaaa'])
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
                print('Eliminado')
                tablero[coordenada] = '0'

    else:
        print(f"Error: La coordenada '{coordenada}' no existe en el tablero.")
    return tablero


def algoritmoMiniMax(board_status,contadorTurno=4, depth=1):

    #Creo el nodo del arbol, que es el tablero que ingresa.
    raiz = Nodo(copy.deepcopy(board_status))

    #obtener fichas de min(enemigo)
    fichasMin = coordenadas_letras(copy.deepcopy(board_status), "mayusculas")

    congeladas = coordenadas_congeladas(copy.deepcopy(board_status))

    #recorrer cada una de las fichas y hacer sus posibles movimientos
    for c,f in fichasMin.items():

        #....QUITAR DE LAS VALIDAS LAS CONGELADAS
        valido = validaMov(congeladas,c,f)
        print(c,f,valido)

        mov = mover(c,f,valido,copy.deepcopy(board_status),contadorTurno)
        print("CAMBIOS:", mov)

        if(mov != []):
            print("Mov no VACIO")
            cont = 0
            for i in mov:
                print("Cambios",i)
                cont2 = 0
                for j in i:
                    #print("UN cambio", j)
                    if j != i[-1]:
                
                        coordenada = mov[cont][cont2][0]
                        # print('coordenda',coordenada)
                        valor = mov[cont][cont2][1]
                        # print('VALOR',valor)
                        ultM = mov[cont][cont2][2]
                        # print('ULTM', ultM)
                        turnosRes = mov[cont][-1]
                        #print('Tur', turnosRes)
                        tableroNuevo = actualizar_tablero(board_status,coordenada,valor)

                    cont2 = cont2 + 1
                
                
                if(tableroNuevo != raiz.tablero):
                        hijoN = Nodo(tableroNuevo,turnosRes,ultM)
                        raiz.hijos.append(hijoN)
                        
                    
                        
                            

                cont = cont + 1

    # imprimir_arbol(raiz)

    return raiz




    #Validar movimientos

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

a = {'A8': 'r', 'B8': 'g', 'C8': 'g', 'D8': 'r', 'E8': 'd', 'F8': 'h', 'G8': 'd', 'H8': 'r',    
    'A7': 0, 'B7': 0, 'C7': 0, 'D7': 0, 'E7': 0, 'F7': 0, 'G7': 0, 'H7': 0,
    'A6': 0, 'B6': 0, 'C6': 0, 'D6':0, 'E6': 0, 'F6': 0, 'G6': 0, 'H6': 0, 
    'A5': 0, 'B5': 0, 'C5': 0, 'D5': 0, 'E5': 0, 'F5': 0, 'G5': 0, 'H5': 0, 
    'A4': 0, 'B4': 0, 'C4': 0, 'D4': 0, 'E4': 0, 'F4': 0, 'G4': 0, 'H4': 0,
    'A3': 0, 'B3': 0, 'C3': 0, 'D3': 0, 'E3': 0, 'F3': 0, 'G3': 0, 'H3': 0, 
    'A2': 0, 'B2': 0, 'C2': 0, 'D2': 0, 'E2': 0, 'F2': 0, 'G2': 0, 'H2': 0, 
    'A1': 'R', 'B1': 'R', 'C1': 'R', 'D1': 'R', 'E1': 'R', 'F1': 'R', 'G1': 'E', 'H1': 'R', 
    'A0': 0, 'A-1': 0, 'B0': 0, 'B-1': 0, 'C0': 0, 'C-1': 0, 'D0': 0, 'D-1': 0, 'E0': 0, 'F0': 0, 'E-1': 0, 'G0': 0, 'F-1': 0, 'H0': 0, 'G-1': 0, 'H-1': 0}
congeladas = coordenadas_congeladas(a)
print("Fichas congeladas:", congeladas)

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


respuesta = algoritmoMiniMax(a).hijos
# imprimir_arbol(respuesta)

