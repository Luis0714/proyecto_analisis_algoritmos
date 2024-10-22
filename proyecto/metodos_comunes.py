import math
from pandas import DataFrame
import numpy as np
from scipy.stats import wasserstein_distance


class MetodosComunes:
  
    @staticmethod
    def obtener_cantidad_de_variables(matriz: DataFrame) -> int:
        cantidad_columnas = matriz.index.size
        n_variables = int(math.log2(cantidad_columnas))
        return n_variables
    
    @staticmethod
    def crear_conjunto_de_letras_segun_estados(variables_estado_futuro: list, variables_estado_actual: list, variables_sistama_candidato: list) -> str:
        """
        Crea un conjunto de letras según los estados actual y futuro
        """
        letras_variables_estado_futuro = MetodosComunes.covertir_estado_de_lista_a_letras(variables_estado_futuro, variables_sistama_candidato, es_variables_estado_futuro=True)
        letras_variables_estado_actual = MetodosComunes.covertir_estado_de_lista_a_letras(variables_estado_actual, variables_sistama_candidato)
         # Retorna una cadena con la forma "{At+1, Bt}"
        return f"{{{letras_variables_estado_futuro}, {letras_variables_estado_actual}}}"
    
    @staticmethod
    def covertir_estado_de_lista_a_letras(estado: list,  variables_sistama_candidato: list, es_variables_estado_futuro:bool = False) -> str:
        """
        Convierte un estado de lista a letras
        """
        vacio = "{"+"vacio"+"}"
        letras_variables = MetodosComunes.generar_letras_abecedario_según_cantidad(variables_sistama_candidato)
        letras_estado = ''.join([letras_variables[i] for i, bit in enumerate(estado) if bit == 1])
        if letras_estado == "":
            letras_estado = vacio
        if es_variables_estado_futuro:
            letras_estado = letras_estado + "t+1"
        else:
            letras_estado = letras_estado + "t"
        return letras_estado
    
    @staticmethod
    def generar_letras_abecedario_según_cantidad(variables_sistema_candidato: list) -> list:
        """
        Genera letras del abecedario según la cantidad de variables
        """
        cantidad = len(variables_sistema_candidato)
        abecedario = [chr(65 + i) for i in range(cantidad)]
        letras = [abecedario[i] for i, bit in enumerate(variables_sistema_candidato) if bit == 1]
        return letras
    
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
    
    @staticmethod
    def obtener_estados_futuros_a_analizar(cantidad_variables: int):
        """
        Retorna los estados futuros a analizar, una lista de listas
        cada lista representa un estado futuro
        si son 3 variables, se tienen 3 estados futuros cada uno con un 1 en una posición diferente y el resto de ceros
        """
        estados_futuros = []
        for i in range(cantidad_variables):
            estado_futuro = [0] * cantidad_variables
            estado_futuro[i] = 1
            estados_futuros.append(estado_futuro)
        return estados_futuros
    
    @staticmethod
    def obtener_subproblemas(variables_estado_actual: list, variables_estado_futuro: list) -> list:
        """
        Genera los subproblemas a partir de los estados actuales y futuros.
        Si tenemos estado futuro [0, 1, 1] y estado actual [1, 0, 1] = BCt+1, ACt
        se obtienen los subproblemas: [[[0, 1, 0], [1, 0, 1]], [[0, 0, 1], [1, 0, 1]]] = [Bt+1, ACt], [Ct+1, ACt]
        """
        subproblemas = []

        # Recorre cada variable en el estado futuro para generar los subproblemas
        for i in range(len(variables_estado_futuro)):
            # Si la variable es diferente de 0 (es relevante), creamos un subproblema
            if variables_estado_futuro[i] != 0:
                subproblema_estado_futuro = [0] * len(variables_estado_futuro)
                subproblema_estado_futuro[i] = variables_estado_futuro[i]  # Solo mantiene la variable en la posición i
                
                # Añade el subproblema a la lista de subproblemas (futuro, actual)
                subproblemas.append([subproblema_estado_futuro, variables_estado_actual])

        return subproblemas
    
    @staticmethod
    def aplicar_producto_tensor_a_lista_distribucion_probabilidades(lista_distribuciones_probabilidades: list):
        """
        Aplica el producto tensor a una lista de distribuciones de probabilidades
        """
        producto_tensor = lista_distribuciones_probabilidades[0]
        for distribucion in lista_distribuciones_probabilidades[1:]:
            producto_tensor = MetodosComunes.tensor_product(producto_tensor, distribucion)
        return producto_tensor
    
    @staticmethod
    def tensor_product(distribucion_uno, distribucion_dos):
        """Realiza el producto tensorial de dos matrices."""
        resul1 = np.array(distribucion_uno)
        resul2 = np.array(distribucion_dos)
        tensor_product = np.kron(resul1, resul2)
        return tensor_product
    
    @staticmethod
    def mostrar_subproblemas_en_letras(subproblemas: list, variables_sistama_candidato: list):
        """
        Muestra los subproblemas en letras
        """
        for subproblema in subproblemas:
            variables_estado_actual = subproblema[1]
            variables_estado_futuro = subproblema[0]
            letras_estado_futuro = MetodosComunes.covertir_estado_de_lista_a_letras(variables_estado_futuro, variables_sistama_candidato, es_variables_estado_futuro=True)
            letras_estado_actual = MetodosComunes.covertir_estado_de_lista_a_letras(variables_estado_actual, variables_sistama_candidato)
            print(f"Subproblema: {letras_estado_futuro}, {letras_estado_actual}")

    @staticmethod
    def generar_complemento_estado(variables_estado:dict, variables_subsistema:dict) -> list:
        """
        Genera el complemento del estado, es decir, las variables que no están en el estado
        y si están en el subsistema ejem:
        estado = {At, Bt}  y subsistema = {At, Bt, At+1, Ct+1}.
        complemento = {At+1, Ct+1}
        """
        complemento = variables_subsistema - variables_estado
        return complemento
    
    @staticmethod
    def convertir_estado_de_dic_a_lista(variables_estados: dict[str], variables_sistema_candidato: list) -> list:
        """
        Convierte un estado de diccionario a lista, 
        devuelve una lista con dos elementos, el primero representa el estado futuro y el segundo el estado actual
        """
        variables_estado_futuro = [""] * len(variables_sistema_candidato)
        variables_estado_actual = [""] * len(variables_sistema_candidato)
        for variable in variables_estados:
            if variable.endswith("t+1"):
                variables_estado_futuro.append(variable)
            else:
                variables_estado_actual.append(variable)
        #reemplzar las variables por 1 si estan en el estado y "" por 0 
        estado_futuro = [1 if variable in variables_estado_futuro else 0 for variable in variables_sistema_candidato]
        estado_actual = [1 if variable in variables_estado_actual else 0 for variable in variables_sistema_candidato]
        return [estado_futuro, estado_actual]
    
    @staticmethod
    def calcular_emd(distribucion_uno: np.ndarray, distribucion_dos: np.ndarray) -> float:
        """
        Calcula la distancia de earth mover
        """
        return wasserstein_distance(distribucion_uno, distribucion_dos)
