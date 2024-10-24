import math
from proyecto.caculador_probabilidades import CalculadorProbabilidades
from proyecto.metodos_comunes import MetodosComunes


class PrimeraEstretegia:

    def __init__(self, matriz_sistema_candidato, variables_sistema_candidato, estado_inicial: list):
        self.calculador_probabilidades = CalculadorProbabilidades(matriz_sistema_candidato, variables_sistema_candidato, estado_inicial)
        self.cantidad_variables_sistema_candidato = MetodosComunes.obtener_cantidad_variables_a_tener_en_cuenta_en_estado(variables_sistema_candidato)
        self.variables_sistema_candidato = variables_sistema_candidato

    def encontrar_particicion_con_menor_perdida(elementos_subsistema:list, distribucion_probabilidades_subsistema_v) -> list | float:
        pass

    def generar_v_prima(self, elementos_subsistema_v:list[str], distribucion_probabilidades_subsistema_v) -> list:
        """
        Genera el conjunto de estados V' que minimiza la función G
        """
        # Se obtiene el elemento vi del conjunto V (conjunto_subsistema_v)
        elementos_w:list = []
        elementos_w.append(elementos_subsistema_v[0])
        # Se crea el conjunto U, los elementos de V que no estan en W
        elementos_u:list = elementos_subsistema_v - elementos_w

        # Se crea una lista para almacenar las perdidas de cada elemento de U
        perdidas_elementos_u = [math.inf] * len(elementos_u) - 1

        # Mientras el conjunto U tenga mas de un elemento
        while len(elementos_u) > 1:

            # se escoje el elemento a comparar el elemento U
            for indice_elemento_u, elemento_u in enumerate(elementos_u):
                # se obtiene el conjunto W1 + {u}
                conjunto_a_evaluar = elementos_w + [elemento_u]
                # se calcula la perdida de G(W1 + {u})
                perdida_conjunto_a_evaluar = self.funcion_G(conjunto_a_evaluar, elementos_subsistema_v, distribucion_probabilidades_subsistema_v)
                # se calcula la perdida de G({u})
                perdida_conjunto_u = self.funcion_G([elemento_u], elementos_subsistema_v, distribucion_probabilidades_subsistema_v)

                # se calcula perdidad total de G(W1 + {u}) - G({u})
                perdida_total = perdida_conjunto_a_evaluar - perdida_conjunto_u
                perdidas_elementos_u[indice_elemento_u] = perdida_total


        
        print(conjunto_w)
        pass

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