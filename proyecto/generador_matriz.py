from pandas import DataFrame

from proyecto.marginalizador import Maginalizador

class GeneradorMatriz:

    def __init__(self):
        self._maginalizador = Maginalizador()

    def generar_matriz_sistema_candidato(self, matrix_original: DataFrame, estado_inicial: list, variables_sistema_candidato: list) -> DataFrame:
        """
        Genera la matriz del sistema candidato eliminando las filas y columnas 
        que no se van a tener en cuenta según las variables del sistema candidato.
        """
        # 1. Eliminar las filas que no se van a tener en cuenta según el estado inicial
        matrix_resultante = self.eliminar_filas(matrix_original, estado_inicial, variables_sistema_candidato)
        
        # 2. Marginalizar las columnas que no se van a tener en cuenta según las variables del sistema candidato
        #matrix_resultante = self.marginalizar_columnas(matrix_resultante, variables_sistema_candidato)
        
        # 3. Retornar la matriz resultante
        return matrix_resultante

    def marginalizar_columnas(self, matrix_original: DataFrame, variables_sistema_candidato: list) -> DataFrame:
        """
        Marginaliza las columnas (estados futuros) eliminando las columnas no presentes 
        en las variables del sistema candidato.
        """
        indices_columnas_a_eliminar = [i for i, var in enumerate(variables_sistema_candidato) if var == 0]
        return self._maginalizador.marginalizar_en_estados_futuros(matrix_original, indices_columnas_a_eliminar)

    def eliminar_filas(self, matrix_original: DataFrame, estado_inicial: list, variables_sistema_candidato: list) -> DataFrame:
        """
        Retorna los índices de las filas que deben ser eliminadas en función del estado inicial
        y las variables que no se toman en cuenta en el sistema candidato.
        """
        # Identificar las variables que no se tienen en cuenta en el sistema candidato
        indices_variables_a_eliminar = [i for i, var in enumerate(variables_sistema_candidato) if var == 0]    

        for index, fila in matrix_original.iterrows():
            if self._es_fila_a_eliminar(fila.name, estado_inicial, indices_variables_a_eliminar):
                matrix_original.drop(index, inplace=True)
            else:
                # Actualiza el nombre del índice de acuerdo a las variables del sistema candidato
                nuevo_nombre = self.eliminar_variables_fila(fila.name, indices_variables_a_eliminar)
                matrix_original.rename({fila.name: nuevo_nombre}, inplace=True)
        return matrix_original

    def _es_fila_a_eliminar(self, fila: str, estado_inicial: list, indices_variables_a_eliminar: list) -> bool:
        """
        Verifica si una fila debe ser eliminada comparando las variables no incluidas en el sistema candidato.
        """
        # Si alguna de las variables a eliminar no coincide con el estado inicial, la fila debe eliminarse
        for indice in indices_variables_a_eliminar:
            if int(fila[indice]) != int(estado_inicial[indice]):
                return True
        return False
    
    def eliminar_variables_fila(self, fila: str, indices_variables_a_eliminar: list) -> str:
        """
        Retorna el nombre de la fila eliminando las variables no incluidas en el sistema candidato.
        """
        return "".join([fila[i] for i in range(len(fila)) if i not in indices_variables_a_eliminar])