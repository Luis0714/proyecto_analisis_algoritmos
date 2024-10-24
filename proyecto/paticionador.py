from proyecto.caculador_probabilidades import CalculadorProbabilidades
from proyecto.generador_matriz import GeneradorMatriz
from proyecto.metodos_comunes import MetodosComunes
from proyecto.primera_estrategia import PrimeraEstretegia


class Particionador:

    def __init__(self, matriz_original, variables_sistema_candidato: list, elementos_subsistema: list, estado_inicial: list):
        self.generador_matriz = GeneradorMatriz()
        self.matriz_sistema_candidato = self.generador_matriz.generar_matriz_sistema_candidato(matriz_original, estado_inicial, variables_sistema_candidato)
        self.calculador_probabilidades = CalculadorProbabilidades(self.matriz_sistema_candidato, variables_sistema_candidato, estado_inicial)
        self.variables_sistema_cadidato = variables_sistema_candidato
        self.cantidad_variables_sistema_candidato = MetodosComunes.obtener_cantidad_variables_a_tener_en_cuenta_en_estado(variables_sistema_candidato)
        self.distribucion_probabilidades_subsistema_Pv = self.calcular_probabilidad_subsistema_Pv(elementos_subsistema)
        print("Distribucion de probabilidades del subsistema Pv: ", "\n")
        print(self.distribucion_probabilidades_subsistema_Pv)

    def ejecutar_primera_estrategia(self, variables_sistema_candidato, elementos_subsistema, estado_inicial):
        print("###############################################################")
        print("#            EJECUTANDO PRIMERA ESTRATEGIA                    #")
        print("###############################################################", '\n')
        
        primera_estrategia = PrimeraEstretegia(self.matriz_sistema_candidato, variables_sistema_candidato, estado_inicial)
        primera_estrategia.encontrar_particicion_con_menor_perdida(elementos_subsistema, self.distribucion_probabilidades_subsistema_Pv.copy())


    def calcular_probabilidad_subsistema_Pv(self, elementos_subsistema:list):
        print("###############################################################")
        print("# PROCESO PARA CALCULAR LAS MATRICES DE LOS ESTADOS FUTUROS   #")
        print("###############################################################", '\n')
        variables_estados = MetodosComunes.convertir_estado_de_lista_letras_a_lista_bits(elementos_subsistema, self.variables_sistema_cadidato)
        estado_futuro = variables_estados[0]
        estado_actual = variables_estados[1]
        return self.calculador_probabilidades.calcular_probabilidad(estado_futuro, estado_actual)