from pandas import DataFrame
from proyecto.metodos_comunes import MetodosComunes


class ValidadorCasos:
    #Metodos para validar casos -------------------------
    
    # def validar_casos_vacios(self, matriz: DataFrame, variables_estado_actual: list, variable_estado_futuro: list, cantidad_variables:int, cahe_probabilidades: dict = {}) -> DataFrame:
    #     if self.es_estado_vacio(variables_estado_actual) and MetodosComunes.es_estado_vacio(variable_estado_futuro):
    #         return None
    #     if self.es_estado_vacio(variables_estado_actual):
    #         return self.calcular_probabilidad_caso_variables_estado_actual_vacio(matriz, variable_estado_futuro, cantidad_variables, cahe_probabilidades)
    #     if self.es_estado_vacio(variable_estado_futuro):
    #         return self.calcular_probabilidad_caso_variable_estado_futuro_vacio(matriz, variables_estado_actual, cantidad_variables, cahe_probabilidades)
    #     return -1
        
                        
    def es_caso_no_mariginalizar_variables_estado_actual_si_futuro(self, variables_estado_actual: list, variable_estado_futuro: list, cantidad_variables:list) -> bool:
        """
        Verifica si se puede calcular la probabilidad sin marginalizar el estado actual
        """
        variables_estado_actual_completo = len(variables_estado_actual) == cantidad_variables and MetodosComunes.se_tiene_en_cuenta_todas_las_variables_en_estado(variables_estado_actual)
        variable_estado_futuro_con_un_elemento = MetodosComunes.obtener_cantidad_variables_a_tener_en_cuenta_en_estado(variable_estado_futuro) == 1   
        return variables_estado_actual_completo and variable_estado_futuro_con_un_elemento
    
    def es_caso_no_marginalizar_actual_no_marginalizar_futuro(self, variable_variable_estado_futuro: list, variables_variables_estado_actual: list) -> bool:
        """
        Verifica si se puede calcular la probabilidad sin marginalizar el estado actual y el estado futuro
        """
        return MetodosComunes.se_tiene_en_cuenta_todas_las_variables_en_estado(variable_variable_estado_futuro) and MetodosComunes.se_tiene_en_cuenta_todas_las_variables_en_estado(variables_variables_estado_actual)
    # Fin de metodos para validar casos -------------------------