import pandas as pd
import itertools
import math
import os

class AccesoDatos:

    def leer_datos(self, file_path) -> pd.DataFrame:
        """Lee un archivo de datos y lo retorna como un DataFrame de pandas"""
        file_extension = os.path.splitext(file_path)[1].lower()

        if file_extension == '.csv':
            data = pd.read_csv(file_path, index_col=None, header=None)
        elif file_extension == '.json':
            data = pd.read_json(file_path, orient='split')
        else:
            raise ValueError(f"Unsupported file extension: {file_extension}")
        self._asignar_encabezados_binarios(data)
        return data

    def _generar_combinaciones_binarias(self, n_variables: int) -> list:
        """Genera combinaciones binarias en el orden que sigue la notación personalizada"""
        # Generamos combinaciones binarias normales y luego las ordenamos con el nuevo patrón
        combinaciones = [''.join(map(str, comb)) for comb in itertools.product([0, 1], repeat=n_variables)]
        
        # Reordenamos las combinaciones con el patrón correcto, por ejemplo, cambiando el MSB (bit más significativo) de manera diferente
        combinaciones_reordenadas = sorted(combinaciones, key=lambda x: int(x[::-1], 2))
        
        return combinaciones_reordenadas

    def _asignar_encabezados_binarios(self, df: pd.DataFrame) -> pd.DataFrame:
        """Asigna encabezados de filas y columnas con combinaciones binarias"""
        # Supongamos que el número de columnas indica el número de variables
        cantidad_columnas = df.index.size
        print(f"cantidad_columnas: {cantidad_columnas}")
        n_variables = int(math.log2(cantidad_columnas))

        print(f"n_variables: {n_variables}")


        # Generar combinaciones binarias
        combinaciones_binarias = self._generar_combinaciones_binarias(n_variables)

        # Asignar las combinaciones binarias a filas y columnas
        df.index = combinaciones_binarias
        df.columns = combinaciones_binarias
        
        return df

