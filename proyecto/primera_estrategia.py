from proyecto.caculador_probabilidades import CalculadorProbabilidades
from proyecto.metodos_comunes import MetodosComunes


class PrimeraEstretegia:

    def __init__(self, matriz_sistema_candidato, variables_sistema_candidato, estado_inicial: list):
        self.calculador_probabilidades = CalculadorProbabilidades(matriz_sistema_candidato, variables_sistema_candidato, estado_inicial)
   

    def encontrar_particicion_con_menor_perdida(conjunto_subsistema:dict) -> dict | float:
        pass

    def comparar_particiones_candidatas(self, particiones_candidatas: list) -> dict | float:
        pass
    
    def funcion_G(self, conjunto_estados:dict, distribucion_probabilidades_subsistema, cantidad_variables:dict) -> float:
        """
        Función G, g= EMD(P(conjunto_estados)⊗P(conjunto_estados_conplemento), P(distribucion_probabilidades_subsistema))
        cantidad_variables: la cantidad de variables del sistema candidato
        conjunto_estados: es Wi-1 ∪ {vi}
        """
        #generar el complemento del estado
        conjunto = conjunto_estados.copy()
        conjunto_complemento = MetodosComunes.generar_complemento_estado(conjunto_estados)

        #convertir los estados a listas de 0 y 1 para representar las variables (1 si esta en el estado, 0 si no)
        variables_estado = MetodosComunes.convertir_estado_de_dic_a_lista(conjunto, cantidad_variables)
        variables_estado_complemento = MetodosComunes.convertir_estado_de_dic_a_lista(conjunto_complemento, cantidad_variables)

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
        emd = MetodosComunes.calcular_emd(tensor_product, distribucion_probabilidades_subsistema)

        return emd