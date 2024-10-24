from pandas import DataFrame

from proyecto.marginalizador import Maginalizador
from proyecto.metodos_comunes import MetodosComunes
from proyecto.validador_casos import ValidadorCasos


class CalculadorProbabilidades:

    def __init__(self, matriz_sistema_candidato: DataFrame,
                    variables_sistema_candidato: list,
                    estado_inicial: list):

        self._marginilizador = Maginalizador()
        self._validador_casos = ValidadorCasos()
        self._variables_sistema_candidato = variables_sistema_candidato
        self._matriz_sistema_candidato = matriz_sistema_candidato
        self._estado_inicial = estado_inicial
        self._cantidad_varibles_matriz = MetodosComunes.obtener_cantidad_variables_a_tener_en_cuenta_en_estado(self._variables_sistema_candidato)
        self._matrices_probalilidades_estados_futuros = {}
        self._cache_probabilidades = {}
        self.calcular_probabilidades_estados_futuros(matriz_sistema_candidato)
    
    def calcular_probabilidad(self, variables_estado_futuro: list, variables_estado_actual: list) -> DataFrame:
       
        letras_estados = MetodosComunes.crear_conjunto_de_letras_segun_estados(variables_estado_futuro, variables_estado_actual, self._variables_sistema_candidato)
        print("###############################################################")
        print(f"# PROBABILIDAD A CALCULAR:       {letras_estados}            #")
        print("###############################################################")

        if letras_estados in self._cache_probabilidades:
            print("Probabilidad ya calculada")
            return self._cache_probabilidades[letras_estados]
        
        matriz = self._matriz_sistema_candidato.copy()
        # 1. Validar casos vacios
        # a. Caso vacio estado actual
        if MetodosComunes.es_estado_vacio(variables_estado_actual):
            return self.calcular_probabilidad_caso_variables_estado_actual_vacio(variables_estado_futuro)
        # b. Caso vacio estado futuro
        if MetodosComunes.es_estado_vacio(variables_estado_futuro):
            return self.calcular_probabilidad_caso_variables_estado_futuro_vacio(variables_estado_actual)

        # 2. valida caso no marginalizar estado actual ni futuro
        if self._validador_casos.es_caso_no_marginalizar_actual_no_marginalizar_futuro(variables_estado_futuro, variables_estado_actual):
            valor_estado_actual = MetodosComunes.obtener_valor_estado_actual(self._estado_inicial, variables_estado_actual)
            print(f"Valor estado actual: {valor_estado_actual}")
            return self.calcular_probabilidad_caso_no_mariginalizar_variables_estado_actual_ni_futuro(matriz, variables_estado_futuro, variables_estado_actual)
        
        if self._validador_casos.es_caso_no_mariginalizar_variables_estado_actual_si_futuro(variables_estado_actual, variables_estado_futuro, self._cantidad_varibles_matriz):
            return self.calcular_probabilidad_caso_no_mariginalizar_variables_estado_actual_si_futuro(matriz, variables_estado_actual, variables_estado_futuro)
        

        return self.calcular_probabilidad_caso_ambos_estados_incompletos(variables_estado_futuro, variables_estado_actual)

        

    #Metodos para calcular probabilidades -------------------------

    def calcular_probabilidad_caso_no_mariginalizar_variables_estado_actual_ni_futuro(self, matriz: DataFrame, variables_estado_futuro: list, variables_estado_actual: list) -> DataFrame:
        valor_variables_estado_actual = MetodosComunes.obtener_valor_estado_actual(self._estado_inicial, variables_estado_actual)
        estado_letras = MetodosComunes.crear_conjunto_de_letras_segun_estados(variables_estado_futuro, variables_estado_actual, self._variables_sistema_candidato)
        distribucion_probabilidades = matriz.loc[valor_variables_estado_actual].values
        self._cache_probabilidades[estado_letras] = distribucion_probabilidades
        return distribucion_probabilidades

    def calcular_probabilidad_caso_no_mariginalizar_variables_estado_actual_si_futuro(self, matriz: DataFrame, variables_estado_actual: list,
                                                                                       variables_estado_futuro: list) -> DataFrame:
        """
        Calcula la probabilidad de un estado futuro en función de un estado actual.
        matriz: DataFrame, matriz sobre la cual se va a calcular la probabilidad
        variables_estado_futuro: list, estado futuro sobre el cual se va a calcular la probabilidad [0, 1, 0, 0] = B
        variables_estado_actual: list, estado actual sobre el cual se va a calcular la probabilidad [1, 0, 1, 0] = C
        matrices_probabilidades_variables_estado_futuros: dict, diccionario con matrices de probabilidades de estados futuros previamete calculadas
        cahe_probabilidades: dict, diccionario con probabilidades previamente calculadas
        """
       
        # 1. Crear conjunto de letras según estados
        letras_estados = MetodosComunes.crear_conjunto_de_letras_segun_estados(variables_estado_futuro, variables_estado_actual, self._variables_sistema_candidato)
        print(f"Letras estados: {letras_estados}")
        # 2. Verificar si la probabilidad ya fue calculada
        if letras_estados in self._cache_probabilidades:
            print("Probabilidad ya calculada")
            return self._cache_probabilidades[letras_estados]
        # 3. Marginalizar en estados futuros       
        matriz_marginalizada = self._marginilizador.marginalizar_en_estados_futuros(matriz, variables_estado_futuro)
        print("Matriz marginalizada")
        print(matriz_marginalizada)
        # 4. Obtener distribución de probabilidades done de la matriz marginalizada donde sea igual al estado actual
        valor_estado_actual = MetodosComunes.obtener_valor_estado_actual(self._estado_inicial,variables_estado_actual)
        distribucion_probabilidades = matriz_marginalizada.loc[valor_estado_actual].values

        # 5. Guardar la probabilidad en el caché
        self._cache_probabilidades[letras_estados] = distribucion_probabilidades

        return distribucion_probabilidades
    
    def calcular_probabilidad_caso_ambos_estados_incompletos(self, variables_estado_futuro: list, variables_estado_actual: list) -> DataFrame:
        print("CASO AMBOS ESTADOS INCOMPLETOS")
        cantidad_variables_estado_fuutro = MetodosComunes.obtener_cantidad_variables_a_tener_en_cuenta_en_estado(variables_estado_futuro)
        if cantidad_variables_estado_fuutro == 1:
            return self.calcular_probabilidad_caso_base_un_elemento_estado_futuro(variables_estado_futuro, variables_estado_actual)
        letras_estados = MetodosComunes.crear_conjunto_de_letras_segun_estados(variables_estado_futuro, variables_estado_actual, self._variables_sistema_candidato)
        subproblemas = MetodosComunes.obtener_subproblemas(variables_estado_actual, variables_estado_futuro)
        print("Subproblemas generados")
        MetodosComunes.mostrar_subproblemas_en_letras(subproblemas, self._variables_sistema_candidato)
        probabilidades_subproblemas_calcualdas = []
        for subproblema in subproblemas:
            variables_estado_actual_subproblema = subproblema[1]
            variables_estado_futuro_subproblema = subproblema[0]
            probabilidad_subproblema = self.calcular_probabilidad_caso_base_un_elemento_estado_futuro(variables_estado_futuro_subproblema, variables_estado_actual_subproblema)
            probabilidades_subproblemas_calcualdas.append(probabilidad_subproblema)
        probabilidad = MetodosComunes.aplicar_producto_tensor_a_lista_distribucion_probabilidades(probabilidades_subproblemas_calcualdas)
        self._cache_probabilidades[letras_estados] = probabilidad
        return probabilidad
        
    def calcular_probabilidad_caso_base_un_elemento_estado_futuro(self, variable_estado_futuro:list, variables_estado_actual:list) -> DataFrame:
        print("CASO BASE UN ELEMENTO ESTADO FUTURO")
        letra_estado_futuro = MetodosComunes.covertir_estado_de_lista_a_letras(variable_estado_futuro, self._variables_sistema_candidato, es_variables_estado_futuro=True)
        print(f"Letra estado futuro: {letra_estado_futuro}")
        # 1. bucamos la matriz de probabilidades para el estado futuro previamente calculada
        matriz_para_analizar = self._matrices_probalilidades_estados_futuros[letra_estado_futuro].copy()
        print("Matriz para analizar")
        print(matriz_para_analizar)
        print("Variables estado actual")
        print(variables_estado_actual)
        valor_estado_actual = MetodosComunes.obtener_valor_estado_actual(self._estado_inicial, variables_estado_actual)
        print(f"Valor estado actual: {valor_estado_actual}")
        # 2. marginalizar sobre los estados actuales
        matriz_marginalizada = self._marginilizador.marginalizar_en_estados_actuales(matriz_para_analizar, variables_estado_actual)
        print("Matriz marginalizada")
        print(matriz_marginalizada)
        # 3. Obtener la distribución de probabilidades
        letras_estados = MetodosComunes.crear_conjunto_de_letras_segun_estados(variable_estado_futuro, variables_estado_actual, self._variables_sistema_candidato)
        distribucion_probabilidades = matriz_marginalizada.loc[valor_estado_actual].values
        self._cache_probabilidades[letras_estados] = distribucion_probabilidades
        return distribucion_probabilidades

    def calcular_probabilidades_estados_futuros(self, matriz: DataFrame):
        estados_futuros_a_analizar = MetodosComunes.obtener_estados_futuros_a_analizar(self._cantidad_varibles_matriz)
        for variables_estado_futuro in estados_futuros_a_analizar:
            matriz_para_analizar = matriz.copy()
            letras_estado_analizar = MetodosComunes.covertir_estado_de_lista_a_letras(variables_estado_futuro, self._variables_sistema_candidato, es_variables_estado_futuro=True)
            matriz_marginalizada = self._marginilizador.marginalizar_en_estados_futuros(matriz_para_analizar, variables_estado_futuro)
            self._matrices_probalilidades_estados_futuros[letras_estado_analizar] = matriz_marginalizada

    def calcular_probabilidad_caso_base_un_elemento_estado_futuro_estado_actual_vacio(self, matriz: DataFrame, variables_estado_actual:list) -> list:
        print("CASO BASE UN ELEMENTO ESTADO FUTURO ESTADO ACTUAL VACIO")
        matriz_agrupada = self._marginilizador.marginalizar_en_estados_actuales(matriz, variables_estado_actual)
        distribucion_probabilidades = matriz_agrupada.loc[''].values
        return distribucion_probabilidades

    def calcular_probabilidad_caso_variables_estado_actual_vacio(self, variables_estado_futuro:list) -> float:
        print("CASO ESTADO ACTUAL VACIO")
        variables_estado_actual = [0] * len(variables_estado_futuro)
        letras_estados = MetodosComunes.crear_conjunto_de_letras_segun_estados(variables_estado_futuro, variables_estado_actual, self._variables_sistema_candidato)
        subproblemas = MetodosComunes.obtener_subproblemas(variables_estado_actual, variables_estado_futuro)
        probabilidades_subproblemas_calcualdas = []
        MetodosComunes.mostrar_subproblemas_en_letras(subproblemas, self._variables_sistema_candidato)
        for subproblema in subproblemas:
            variables_estado_futuro_subproblema = subproblema[0]
            variables_estado_actual_subproblema = subproblema[1]
            letra_estado_futuro = MetodosComunes.covertir_estado_de_lista_a_letras(variables_estado_futuro_subproblema, self._variables_sistema_candidato, es_variables_estado_futuro=True)
            print(f"Variables estado futuro subproblema: {letra_estado_futuro}")
            matriz_para_analizar = self._matrices_probalilidades_estados_futuros[letra_estado_futuro].copy()
            probabilidad_subproblema = self.calcular_probabilidad_caso_base_un_elemento_estado_futuro_estado_actual_vacio(matriz_para_analizar, variables_estado_actual_subproblema)
            print(f"Probabilidad subproblema: {probabilidad_subproblema}")
            probabilidades_subproblemas_calcualdas.append(probabilidad_subproblema)

        distribucion_probabilidades = MetodosComunes.aplicar_producto_tensor_a_lista_distribucion_probabilidades(probabilidades_subproblemas_calcualdas)
        self._cache_probabilidades[letras_estados] = distribucion_probabilidades
        return distribucion_probabilidades

    def calcular_probabilidad_caso_variables_estado_futuro_vacio(self, variables_estado_actual:list) -> list:
        print("CASO ESTADO FUTURO VACIO")
        distribucion_probabilidades = [1.0]
        estado_futuro = [0] * len(variables_estado_actual)
        letras_estados = MetodosComunes.crear_conjunto_de_letras_segun_estados(estado_futuro, variables_estado_actual, self._variables_sistema_candidato)
        if letras_estados in self._cache_probabilidades:
            print("Probabilidad ya calculada")
            return self._cache_probabilidades[letras_estados]
        print(f"Letras estados: {letras_estados}")
        self._cache_probabilidades[letras_estados] = distribucion_probabilidades
        return distribucion_probabilidades


    # Fin de metodos para calcular probabilidades -------------------------



    