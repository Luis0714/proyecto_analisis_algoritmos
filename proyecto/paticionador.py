from proyecto.caculador_probabilidades import CalculadorProbabilidades
from proyecto.generador_matriz import GeneradorMatriz
from proyecto.metodos_comunes import MetodosComunes
from proyecto.primera_estrategia import PrimeraEstretegia


class Particionador:

    def __init__(self, matriz_sistema_candidato,variables_sistema_candidato: list, conjunto_subsistema: dict, estado_inicial: list):
        self.calculador_probabilidades = CalculadorProbabilidades(matriz_sistema_candidato, variables_sistema_candidato, estado_inicial)
        self.generador_matriz = GeneradorMatriz()
        self.cantidad_variables_sistema_candidato = MetodosComunes.obtener_cantidad_variables_a_tener_en_cuenta_en_estado(variables_sistema_candidato)
        self.distribucion_probabilidades_subsistema_Pv = self.calcular_probabilidad_subsistema_Pv(conjunto_subsistema)


    def ejecutar_primera_estrategia(self, matriz_original, variables_sistema_candidato, conjunto_subsistema, estado_inicial):
        matriz_sistema_candidato = self.generador_matriz.generar_matriz_sistema_candidato(matriz_original, estado_inicial, variables_sistema_candidato)
        primera_estrategia = PrimeraEstretegia(matriz_sistema_candidato, variables_sistema_candidato, estado_inicial)
        mejor_particion, valor_perdida_particion = primera_estrategia.encontrar_particicion_con_menor_perdida(conjunto_subsistema)


    def calcular_probabilidad_subsistema_Pv(self, conjunto_subsistema:dict):
        variables_estados = MetodosComunes.convertir_estado_de_dic_a_lista(conjunto_subsistema, self.cantidad_variables_sistema_candidato)
        estado_futuro = variables_estados[0]
        estado_actual = variables_estados[1]
        return self.calculador_probabilidades.calcular_probabilidad(estado_futuro, estado_actual)