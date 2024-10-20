from pandas import DataFrame

from proyecto.marginalizador import Maginalizador

class GeneradorMatriz:

    def __init__(self):
        self._maginalizador = Maginalizador()

    def generar_matriz_sistema_candidato(self, matriz_original: DataFrame, estado_inicial: list, variables_sistema_candidato: list) -> DataFrame:
        """
        Genera la matriz del sistema candidato eliminando las filas y columnas 
        que no se van a tener en cuenta según las variables del sistema candidato.
        """
        # 1. Eliminar las filas que no se van a tener en cuenta según el estado inicial
        matriz_resultante = self._maginalizador.eliminar_filas(matriz_original, estado_inicial, variables_sistema_candidato)
        print("Matriz resultante de eliminar filas para encontrar matriz sistema candidato")
        print(matriz_resultante, '\n')
    
        # 2. Marginalizar las columnas que no se van a tener en cuenta según las variables del sistema candidato
        matriz_resultante = self._maginalizador.marginalizar_en_estados_futuros(matriz_resultante, variables_sistema_candidato)
        print("Matriz resultante de marginalizar columnas para encontrar matriz sistema candidato")
        print(matriz_resultante, '\n')
        
        # 3. Retornar la matriz resultante
        return matriz_resultante

   

    