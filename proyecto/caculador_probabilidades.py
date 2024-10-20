from pandas import DataFrame

from proyecto.marginalizador import Maginalizador
from proyecto.metodos_comunes import MetodosComunes
from proyecto.validador_casos import ValidadorCasos


class CalculadorProbabilidades:

    def __init__(self, matriz_sistema_candidato: DataFrame,
                    variables_estado_actual: list,
                    variables_estado_futuro: list,
                    variables_sistema_candidato: list,
                    estado_inicial: list):

        self._marginilizador = Maginalizador()
        self._validador_casos = ValidadorCasos()
        self._matriz_sistema_candidato = matriz_sistema_candidato
        self._estado_inicial = estado_inicial
        self._probalilidades_estados_futuros = {}
        self._cache_probabilidades = {}
        self._variables_sistema_candidato = variables_sistema_candidato
    
    def calcular_probabilidad(self, variables_estado_futuro: list, variables_estado_actual: list) -> DataFrame:
     
        matriz = self._matriz_sistema_candidato.copy()
        cantidad_varibles_matriz = MetodosComunes.obtener_cantidad_variables_a_tener_en_cuenta_en_estado(self._variables_sistema_candidato)
        # 1. Validar casos vacios
        

        # 2. valida caso no marginalizar estado actual ni futuro
        if self._validador_casos.es_caso_no_marginalizar_actual_no_marginalizar_futuro(variables_estado_futuro, variables_estado_actual):
            valor_estado_actual = MetodosComunes.obtener_valor_estado_actual(self._estado_inicial, variables_estado_actual)
            print(f"Valor estado actual: {valor_estado_actual}")
            return self.calcular_probabilidad_caso_no_mariginalizar_variables_estado_actual_ni_futuro(matriz, variables_estado_futuro, variables_estado_actual, cantidad_varibles_matriz)
        
        if self._validador_casos.es_caso_no_mariginalizar_variables_estado_actual_si_futuro(variables_estado_actual, variables_estado_futuro, cantidad_varibles_matriz):
            return self.calcular_probabilidad_caso_no_mariginalizar_variables_estado_actual_si_futuro(matriz, variables_estado_actual, variables_estado_futuro, cantidad_varibles_matriz)
        
        return DataFrame()

        

    #Metodos para calcular probabilidades -------------------------

    def calcular_probabilidad_caso_no_mariginalizar_variables_estado_actual_ni_futuro(self, matriz: DataFrame, variables_estado_futuro: list, variables_estado_actual: list, cantidad_variables) -> DataFrame:

        valor_variables_estado_actual = MetodosComunes.obtener_valor_estado_actual(self._estado_inicial, variables_estado_actual)
        estado_letras = MetodosComunes.crear_conjunto_de_letras_segun_estados(variables_estado_futuro, variables_estado_actual, cantidad_variables)
        distribucion_probabilidades = matriz.loc[valor_variables_estado_actual].values
        self._cache_probabilidades[estado_letras] = distribucion_probabilidades
        return distribucion_probabilidades

    def calcular_probabilidad_caso_no_mariginalizar_variables_estado_actual_si_futuro(self, matriz: DataFrame, variables_estado_actual: list, variables_estado_futuro: list, 
                                       cantidad_varibles_matriz:list) -> DataFrame:
        """
        Calcula la probabilidad de un estado futuro en función de un estado actual.
        matriz: DataFrame, matriz sobre la cual se va a calcular la probabilidad
        variables_estado_futuro: list, estado futuro sobre el cual se va a calcular la probabilidad [0, 1, 0, 0] = B
        variables_estado_actual: list, estado actual sobre el cual se va a calcular la probabilidad [1, 0, 1, 0] = C
        matrices_probabilidades_variables_estado_futuros: dict, diccionario con matrices de probabilidades de estados futuros previamete calculadas
        cahe_probabilidades: dict, diccionario con probabilidades previamente calculadas
        """
       
        # 1. Crear conjunto de letras según estados
        letras_estados = MetodosComunes.crear_conjunto_de_letras_segun_estados(variables_estado_futuro, variables_estado_actual, cantidad_varibles_matriz)
        # 2. Verificar si la probabilidad ya fue calculada
        if letras_estados in self._cache_probabilidades:
            return self._cache_probabilidades[letras_estados]
        # 3. Marginalizar en estados futuros       
        matriz_marginalizada = self._marginilizador.marginalizar_en_estados_futuros(matriz, variables_estado_futuro)
        
        # 4. Obtener distribución de probabilidades done de la matriz marginalizada donde sea igual al estado actual
        valor_estado_actual = MetodosComunes.obtener_valor_estado_actual(self._estado_inicial,variables_estado_actual)
        distribucion_probabilidades = matriz_marginalizada.loc[valor_estado_actual].values

        # 5. Guardar la probabilidad en el caché
        self._cache_probabilidades[letras_estados] = distribucion_probabilidades

        return distribucion_probabilidades
    
    def calcular_probabilidades_estados_futuros(self, matriz: DataFrame, variables_estado_actual: list) -> dict:
        cantidad_variables = len(self._variables_sistema_candidato)
        indices_variables_estado_future = [i for i, bit in len(cantidad_variables)]
        for i in indices_variables_estado_future:
            variables_estado_futuro = [0] * cantidad_variables
            variables_estado_futuro[i] = 1
            self._probalilidades_estados_futuros[variables_estado_futuro] = self.calcular_probabilidad_caso_no_mariginalizar_variables_estado_actual_ni_futuro(matriz, variables_estado_futuro, len(variables_estado_actual))

    def calcular_probabilidad_caso_variables_estado_actual_vacio(self, matriz: DataFrame, variables_estado_futuro: list, 
                                                        cantidad_variables:int, cahe_probabilidades: dict = {}) -> float:
        pass

    def calcular_probabilidad_caso_variables_estado_futuro_vacio(self, matriz: DataFrame, variables_estado_actual: list,
                                                        cantidad_variables:int, cahe_probabilidades: dict = {}) -> float:
        pass
    
    # Fin de metodos para calcular probabilidades -------------------------



    