import math
from proyecto.caculador_probabilidades import CalculadorProbabilidades
from proyecto.metodos_comunes import MetodosComunes


class PrimeraEstretegia:

    def __init__(self, matriz_sistema_candidato, variables_sistema_candidato, estado_inicial: list):
        self.calculador_probabilidades = CalculadorProbabilidades(matriz_sistema_candidato, variables_sistema_candidato, estado_inicial)
        self.cantidad_variables_sistema_candidato = MetodosComunes.obtener_cantidad_variables_a_tener_en_cuenta_en_estado(variables_sistema_candidato)
        self.variables_sistema_candidato = variables_sistema_candidato

    def encontrar_particicion_con_menor_perdida(self, elementos_subsistema:list, distribucion_probabilidades_subsistema_v) -> list | float:
        print("###############################################################")
        print("# PROCESO PARA CALCULAR LAS PARTICIONES CON LOS V PRIMA       #")
        print("###############################################################", '\n')
        elementos_subsistema_v = elementos_subsistema.copy()
        particiones_candidatas = []
        # Se genera el conjunto V' que minimiza la función G
        #while len(elementos_subsistema_v) > 2:
        elementos_subsistema_v = self.generar_v_prima(elementos_subsistema_v, distribucion_probabilidades_subsistema_v, particiones_candidatas)
       # print("Conjunto V' que minimiza la función G: ", elementos_subsistema_v)


    def generar_v_prima(self, elementos_subsistema_v:list[str], distribucion_probabilidades_subsistema_v, partciones_candidatas) -> list:
        """
        Genera el conjunto de estados V' que minimiza la función G
        """
        print("###############################################################")
        print("# PROCESO PARA CALCULAR LAS V PRIMA                           #")
        print("###############################################################", '\n')
        # Se obtiene el elemento vi del conjunto V (conjunto_subsistema_v)
        print("Elementos del subsistema V: ", elementos_subsistema_v)
        elementos_w:list = []
        elementos_w.append(elementos_subsistema_v[0])
        print("Elementos del conjunto W: ", elementos_w)
        # Se crea el conjunto U, los elementos de V que no estan en W
        elementos_u:list = MetodosComunes.generar_complemento_estado(elementos_w, elementos_subsistema_v)

        # Se crea una lista para almacenar las perdidas de cada elemento de U
        cantidad_elementos_u = len(elementos_u)
     
        # Mientras el conjunto U tenga mas de un elemento
        while len(elementos_u) > 1:
            print("Elementos del conjunto U: ", elementos_u)
            # se escoje el elemento a comparar el elemento U
            indice_elemento_u = 0
            perdida_total_elemento_u = math.inf
            perdidas_elementos_u:list = [math.inf] * (cantidad_elementos_u)
            print("Perdidas de elementos U: ", perdidas_elementos_u)

            # se recorre cada elemento de U para calcular la perdida total, si la perdida total es 0 se detiene el ciclo
            # y se agrega el elemento a W
            while indice_elemento_u <= (cantidad_elementos_u - 1) and perdida_total_elemento_u != 0:
                elemento_u = elementos_u[indice_elemento_u]
                # se obtiene el conjunto W1 + {u}
                conjunto_a_evaluar = elementos_w + [elemento_u]
                print("Conjunto a evaluar: ", conjunto_a_evaluar)
                # se calcula la perdida de G(W1 + {u})
                perdida_conjunto_a_evaluar = self.funcion_G(conjunto_a_evaluar, elementos_subsistema_v, distribucion_probabilidades_subsistema_v)
                print("Perdida de G(W1 + {u}): ", perdida_conjunto_a_evaluar)
                # se calcula la perdida de G({u})
                perdida_conjunto_u = self.funcion_G([elemento_u], elementos_subsistema_v, distribucion_probabilidades_subsistema_v)
                print("Perdida de G({u}): ", perdida_conjunto_u)
                # se calcula perdidad total de G(W1 + {u}) - G({u})
                perdida_total_elemento_u = perdida_conjunto_a_evaluar - perdida_conjunto_u
                print("Indice del elemento U: ", indice_elemento_u)
                perdidas_elementos_u[indice_elemento_u] = perdida_total_elemento_u
                print("Perdida total: ", perdida_total_elemento_u)
                print("Perdidas de elementos U: ", perdidas_elementos_u)
                indice_elemento_u += 1
            # se obtiene el indice del elemento con menor perdida
            indice_elemento_menor_perdida = perdidas_elementos_u.index(min(perdidas_elementos_u))
            print("Indice del elemento con menor perdida: ", indice_elemento_menor_perdida)
            #se obtiene el elemento con menor perdida
            elemento_menor_perdida = elementos_u[indice_elemento_menor_perdida]
            print("Elemento con menor perdida: ", elemento_menor_perdida)
            # se agrega el elemento con menor perdida al conjunto W
            elementos_w2 = elementos_w + [elemento_menor_perdida]
            elementos_u = MetodosComunes.generar_complemento_estado(elementos_subsistema_v, elementos_w2)
            elementos_w = elementos_w2
            print("Cojunto W con el nuevo elemento: ", elementos_w)

        print("Conjunto W con los elementos minimos: ", elementos_w)
        print("Cojunto U con el ultimo elemento: ", elemento_u)
        
        # Llamar función para generar la partición candidata y guardarla
        return []

    def comparar_particiones_candidatas(self, particiones_candidatas: list) -> dict | float:
        pass
    
    def funcion_G(self, elementos_estado:list, elementos_subsistema_v:list, distribucion_probabilidades_subsistema_v) -> float:
        """
        Función G, g= EMD(P(conjunto_estados)⊗P(conjunto_estados_conplemento), P(distribucion_probabilidades_subsistema))
        cantidad_variables: la cantidad de variables del sistema candidato
        elementos_estado: es Wi-1 ∪ {vi} = [At, Bt, At+1, Bt+1]
        """
        #generar el complemento del estado
        elementos_complemento = MetodosComunes.generar_complemento_estado(elementos_estado, elementos_subsistema_v)

        #convertir los estados a listas de 0 y 1 para representar las variables (1 si esta en el estado, 0 si no)
        variables_estado = MetodosComunes.convertir_estado_de_lista_letras_a_lista_bits(elementos_estado, self.variables_sistema_candidato)
        variables_estado_complemento = MetodosComunes.convertir_estado_de_lista_letras_a_lista_bits(elementos_complemento, self.variables_sistema_candidato)

        #se calcula la distribicion de probanilidades del estado y su complemento
        estado_futuro_estado = variables_estado[0]
        estado_actual_estado = variables_estado[1]
        matrix_probabilidades_estado = self.calculador_probabilidades.calcular_probabilidad(estado_futuro_estado, estado_actual_estado)

        estado_futuro_complemento = variables_estado_complemento[0]
        estado_actual_complemento = variables_estado_complemento[1]
        matrix_probabilidades_complemento = self.calculador_probabilidades.calcular_probabilidad(estado_futuro_complemento, estado_actual_complemento)

        #se aplica el producto tensorial a las distribuciones de probabilidad
        tensor_product = MetodosComunes.tensor_product(matrix_probabilidades_estado, matrix_probabilidades_complemento)

        #se calcula la distancia de earth mover
        emd = MetodosComunes.calcular_emd(tensor_product, distribucion_probabilidades_subsistema_v)

        return emd