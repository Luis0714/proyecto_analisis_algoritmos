import math
from pandas import DataFrame


class MetodosComunes:
  

    @staticmethod
    def obtener_cantidad_de_variables(matriz: DataFrame) -> int:
        cantidad_columnas = matriz.index.size
        print(f"cantidad_columnas: {cantidad_columnas}")
        n_variables = int(math.log2(cantidad_columnas))
        print(f"n_variables: {n_variables}")
        return n_variables
    
    @staticmethod
    def crear_conjunto_de_letras_segun_estados(variables_estado_futuro: list, variables_estado_actual: list, cantidad_variables: int) -> str:
        """
        Crea un conjunto de letras según los estados actual y futuro
        """
        letras_variables_estado_futuro = MetodosComunes.covertir_estado_de_lista_a_letras(variables_estado_futuro, cantidad_variables, es_variables_estado_futuro=True)
        letras_variables_estado_actual = MetodosComunes.covertir_estado_de_lista_a_letras(variables_estado_actual, cantidad_variables)
         # Retorna una cadena con la forma "{At+1, Bt}"
        return f"{{{letras_variables_estado_futuro}, {letras_variables_estado_actual}}}"
    
    @staticmethod
    def covertir_estado_de_lista_a_letras(estado: list,  cantidad_variables: int, es_variables_estado_futuro:bool = False) -> str:
        """
        Convierte un estado de lista a letras
        """
        vacio = "{"+"vacio"+"}"
        letras_variables = MetodosComunes.generar_letras_avecedario_según_cantidad(cantidad_variables)
        letras_estado = ''.join([letras_variables[i] for i, bit in enumerate(estado) if bit == 1])
        if letras_estado == "":
            letras_estado = vacio
        if es_variables_estado_futuro:
            letras_estado = letras_estado + "t+1"
        else:
            letras_estado = letras_estado + "t"
        return letras_estado
    
    @staticmethod
    def generar_letras_avecedario_según_cantidad(cantidad: int) -> list:
        """
        Genera letras del abecedario según la cantidad de variables
        """
        return [chr(65 + i) for i in range(cantidad)]
    
    @staticmethod
    def es_estado_vacio(estado: list) -> bool:
        """
        Verifica si un estado es vacío
        """
        return all([bit == 0 for bit in estado])
    
    @staticmethod
    def se_tiene_en_cuenta_todas_las_variables_en_estado(estado: list) -> bool:
        """
        Verifica si se tienen en cuenta todas las variables
        """
        return all([bit == 1 for bit in estado])
    
    @staticmethod
    def obtener_cantidad_variables_a_tener_en_cuenta_en_estado(estado: list) -> int:
        """
        Retorna la cantidad de variables que se tienen en cuenta en un estado
        """
        return estado.count(1)
    
    @staticmethod
    def obtener_valor_estado_actual(estado_inicial: list, variables_estado_actual: list) -> list:
        """
        Retorna el valor del estado actual
        """
        lista_estado_actual = [estado_inicial[i] for i, bit in enumerate(variables_estado_actual) if bit == 1]
        valor_estado_actual = ''.join(map(str, lista_estado_actual))
        return valor_estado_actual
    
