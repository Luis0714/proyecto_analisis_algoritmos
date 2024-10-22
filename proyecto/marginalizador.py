from pandas import DataFrame

from proyecto.metodos_comunes import MetodosComunes

class Maginalizador:
    
    def marginalizar_en_estados_futuros(self, matriz: DataFrame, variables_estado_futuro: list) -> DataFrame:
        """
        Marginaliza las columnas eliminando las que no se van a tener en cuenta y luego 
        sumando las columnas que quedan con el mismo encabezado (binario).
        """

        # 1. Identificar las columnas a eliminar
        indices_columnas_a_eliminar = self.obtener_indices_variables_a_eliminar(variables_estado_futuro)
        if len(indices_columnas_a_eliminar) == 0: return matriz
        
        # 2. Eliminar las columnas que no se van a tener en cuenta
        matriz.columns = [self.eliminar_variables(colunm, indices_columnas_a_eliminar) for colunm in matriz.columns]
        
        # 3. Agrupar las columnas restantes con el mismo encabezado (binario) y sumarlas
        matriz = self.__agrupar_y_sumar_columnas(matriz)

        return matriz

    def marginalizar_en_estados_actuales(self, matriz: DataFrame, variables_a_eliminar: list) -> DataFrame:
        """
           Marginaliza un DataFrame en filas eliminando las que no se van a tener en cuenta.
            y luego sumando y dividiendo sobre 2 las filas que quedan con el mismo encabezado (binario).
        """
        # 1. Identificar las filas a eliminar
        indices_variables_a_eliminar = self.obtener_indices_variables_a_eliminar(variables_sistema_candidato=variables_a_eliminar)

        # 2. Eliminar las filas que no se van a tener en cuenta
        matriz.index = [self.eliminar_variables(fila, indices_variables_a_eliminar) for fila in matriz.index]

        # 3. Agrupar las filas restantes con el mismo encabezado (binario), sumarlas y dividirlas sobre dos elevado
        # a la cantidad de variables eliminadas
        cantidad_filas_agrupadas = 2**len(indices_variables_a_eliminar)
        #print("cantidad de variables para dividir", cantidad_filas_agrupadas)
        matriz = self.__agrupar_y_sumar_filas(matriz) / cantidad_filas_agrupadas

        return matriz
    
    
    def __agrupar_y_sumar_filas(self, matriz: DataFrame) -> DataFrame:
        """
        Agrupa las filas restantes con el mismo encabezado (binario) y las suma.
        """
        matriz = matriz.groupby(matriz.index).sum()
        return matriz

    def __agrupar_y_sumar_columnas(self, matriz: DataFrame) -> DataFrame:
        """
        Agrupa las columnas restantes con el mismo encabezado (binario) y las suma.
        """
        matriz = matriz.T.groupby(level=0).sum().T
        return matriz
        

    #Metodos para eliminar filas de una matriz -------------------------
    def eliminar_filas(self, matriz_original: DataFrame, estado_inicial: list, variables_sistema_candidato: list) -> DataFrame:
        """
        Retorna los índices de las filas que deben ser eliminadas en función del estado inicial
        y las variables que no se toman en cuenta en el sistema candidato.
        """
        indices_variables_a_eliminar = self.obtener_indices_variables_a_eliminar(variables_sistema_candidato)
        if len(indices_variables_a_eliminar) == 0: return matriz_original
        for index, fila in matriz_original.iterrows():
            if self.__se_puede_eliminar(fila.name, estado_inicial, indices_variables_a_eliminar):
                matriz_original.drop(index, inplace=True)
            else:
                # Actualiza el nombre del índice de acuerdo a las variables del sistema candidato
                nuevo_nombre = self.eliminar_variables(fila.name, indices_variables_a_eliminar)
                matriz_original.rename({fila.name: nuevo_nombre}, inplace=True)
        return matriz_original

    def __se_puede_eliminar(self, fila: str, estado_inicial: list, indices_variables_a_eliminar: list) -> bool:
        """
        Verifica si una fila debe ser eliminada comparando las variables no incluidas en el sistema candidato.
        """
        # Si alguna de las variables a eliminar no coincide con el estado inicial, la fila debe eliminarse
        for indice in indices_variables_a_eliminar:
            if int(fila[indice]) != int(estado_inicial[indice]):
                return True
        return False
    
    def eliminar_variables(self, estado: str, indices_variables_a_eliminar: list) -> str:
        """
        Retorna el nombre de la fila eliminando las variables no incluidas en el sistema candidato.
        """
        return "".join([estado[i] for i in range(len(estado)) if i not in indices_variables_a_eliminar])
    
    def obtener_indices_variables_a_eliminar(self, variables_sistema_candidato: list) -> list:
        """
        Retorna los índices de las variables que no se incluyen en el sistema candidato.
        """
        return [i for i in range(len(variables_sistema_candidato)) if variables_sistema_candidato[i] == 0]