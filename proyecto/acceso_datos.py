import pandas as pd
import itertools
import os
import tkinter as tk
from tkinter import filedialog
from proyecto.metodos_comunes import MetodosComunes

class AccesoDatos:

    def leer_datos(self, file_path=None) -> pd.DataFrame:
        """Lee un archivo de datos y lo retorna como un DataFrame de pandas"""
        # Si no se proporciona una ruta de archivo, abrir un cuadro de diálogo para seleccionarlo
        if file_path is None:
            file_path = self._seleccionar_archivo()

        # Obtener la extensión del archivo
        file_extension = os.path.splitext(file_path)[1].lower()

        # Leer el archivo en función de su tipo
        if file_extension == '.csv':
            data = pd.read_csv(file_path, index_col=None, header=None)
        elif file_extension == '.json':
            data = pd.read_json(file_path, orient='split')
        else:
            raise ValueError(f"Unsupported file extension: {file_extension}")
        
        self._asignar_encabezados_binarios(data)
        return data

    def _seleccionar_archivo(self) -> str:
        """Abre una ventana para seleccionar un archivo y retorna la ruta seleccionada"""
        root = tk.Tk()
        root.withdraw()  # Oculta la ventana principal
        # Abre un cuadro de diálogo para seleccionar archivos
        file_path = filedialog.askopenfilename(title="Seleccionar archivo",
                                               filetypes=[("CSV files", "*.csv"), ("JSON files", "*.json")])
        if not file_path:
            raise FileNotFoundError("No se seleccionó ningún archivo")
        return file_path

    def _generar_combinaciones_binarias(self, n_variables: int) -> list:
        """Genera combinaciones binarias en el orden que sigue la notación personalizada"""
        combinaciones = [''.join(map(str, comb)) for comb in itertools.product([0, 1], repeat=n_variables)]
        combinaciones_reordenadas = sorted(combinaciones, key=lambda x: int(x[::-1], 2))
        return combinaciones_reordenadas

    def _asignar_encabezados_binarios(self, matriz: pd.DataFrame) -> pd.DataFrame:
        """Asigna encabezados de filas y columnas con combinaciones binarias"""
        cantidad_variables = MetodosComunes.obtener_cantidad_de_variables(matriz)
        combinaciones_binarias = self._generar_combinaciones_binarias(cantidad_variables)
        matriz.index = combinaciones_binarias
        matriz.columns = combinaciones_binarias
        return matriz
