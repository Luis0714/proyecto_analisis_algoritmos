from pandas import DataFrame

class Maginalizador:
    
    def marginalizar_en_estados_futuros(self, matrix_original: DataFrame, estado_inicial: list, variables_sistema_candidato: list) -> DataFrame:
        """
        Marginaliza las columnas eliminando las que no se van a tener en cuenta y luego 
        sumando las columnas que quedan con el mismo encabezado (binario).
        """
        # 1. Identificar las columnas a eliminar
        indices_columnas_a_eliminar = self.obtener_columnas_a_eliminar(matrix_original.columns, estado_inicial, variables_sistema_candidato)
        print(f"Indices de columnas a eliminar: {indices_columnas_a_eliminar}")
        
        # 2. Eliminar las columnas que no se van a tener en cuenta
        matrix_resultante = matrix_original.drop(columns=indices_columnas_a_eliminar)
        
        # 3. Agrupar las columnas restantes con el mismo encabezado (binario) y sumarlas
        matrix_resultante = self.agrupar_y_sumar_columnas(matrix_resultante)

        return matrix_resultante

    def obtener_columnas_a_eliminar(self, columnas: list, estado_inicial: list, variables_sistema_candidato: list) -> list:
        """
        Retorna los nombres de las columnas que deben ser eliminadas según el estado inicial
        y las variables que no se toman en cuenta en el sistema candidato.
        """
        columnas_a_eliminar = []
        # Identificar las variables que no se tienen en cuenta en el sistema candidato
        indices_variables_a_eliminar = [i for i, var in enumerate(variables_sistema_candidato) if var == 0]

        # Iterar por cada columna (cada columna es un string binario)
        for columna in columnas:
            # Verificar si la columna tiene un valor distinto al estado inicial para las variables no incluidas
            for indice in indices_variables_a_eliminar:
                if int(columna[indice]) != int(estado_inicial[indice]):
                    columnas_a_eliminar.append(columna)
                    break

        return columnas_a_eliminar

    def agrupar_y_sumar_columnas(self, matrix_resultante: DataFrame) -> DataFrame:
        """
        Agrupa las columnas restantes con el mismo encabezado (binario) y las suma.
        """
        # Crear una copia del DataFrame original para evitar cambios en el original
        matrix_agrupada = matrix_resultante.copy()

        # Crear un diccionario para agrupar y sumar las columnas que tienen el mismo encabezado binario
        columnas_agrupadas = {}

        for columna in matrix_agrupada.columns:
            # Eliminar las columnas que ya se hayan agrupado y sumado
            if columna not in columnas_agrupadas:
                # Filtrar las columnas que tienen el mismo encabezado (binario)
                columnas_similares = [col for col in matrix_agrupada.columns if col == columna]
                
                # Sumar las columnas similares
                suma_columnas = matrix_agrupada[columnas_similares].sum(axis=1)
                
                # Guardar la suma en el nuevo DataFrame
                columnas_agrupadas[columna] = suma_columnas

        # Crear un nuevo DataFrame con las columnas agrupadas y sumadas
        matrix_final = DataFrame(columnas_agrupadas)

        return matrix_final

    
    def marginalizar_en_estados_actuales(self, df: DataFrame, indices_variables_a_eliminar: list) -> DataFrame:
        """Marginaliza un DataFrame en filas"""
        return df.sum(axis=1)