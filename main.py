from proyecto.acceso_datos import AccesoDatos
from proyecto.caculador_probabilidades import CalculadorProbabilidades
from proyecto.generador_matriz import GeneradorMatriz
from proyecto.marginalizador import Maginalizador
from proyecto.metodos_comunes import MetodosComunes

acceso_datos = AccesoDatos()
generador_matriz = GeneradorMatriz()
marginalizador = Maginalizador()
metodos_comunes = MetodosComunes()
matriz = acceso_datos.leer_datos("data.csv")

def main():
    matriz = acceso_datos.leer_datos("data.csv")
    print("Matriz original")
    print(matriz,'\n')
    
    #pruba con estados completos
    estado_inicial = [0, 0, 0, 0]
    variables_sistema_candidato = [1, 1, 1, 0] # 1 indica que se tiene en cuenta la variable, 0 que no se tiene en cuenta A, B, C menos D
    matriz_sistema_candidato = generador_matriz.generar_matriz_sistema_candidato(matriz, estado_inicial, variables_sistema_candidato)

    # variable_estado_futuro = [1, 1, 1] # ABC t+1
    # variable_estado_actual = [1, 1, 1] # ABC t
    # print("Matriz sistema candidato")
    # print(matriz_sistema_candidato, '\n')
    # prueba_calcular_probabilidad(matriz_sistema_candidato, 
    #                             variables_sistema_candidato, 
    #                             variable_estado_futuro, 
    #                             variable_estado_actual,
    #                             estado_inicial)

    
    #prueba con solo estado actual completo y estado futuro con un elemento
    variable_estado_futuro = [0,1,0] # B t+1
    variable_estado_actual = [1, 1, 1] # ABC t
    prueba_calcular_probabilidad(matriz_sistema_candidato,
                                variables_sistema_candidato,
                                variable_estado_futuro,
                                variable_estado_actual,
                                estado_inicial)



   
def prueba_calcular_probabilidad(matriz, variables_sistema_candidato, variables_estado_futuro, variables_estado_actual, estado_inicial):
    calculador_probabilidades = CalculadorProbabilidades(
        matriz_sistema_candidato=matriz,
        variables_estado_actual=variables_estado_actual,
        variables_estado_futuro=variables_estado_futuro,
        variables_sistema_candidato=variables_sistema_candidato,
        estado_inicial=estado_inicial
    )
    print("Prueba de calcular probabilidad")
    probabilidad = calculador_probabilidades.calcular_probabilidad(variables_estado_futuro, variables_estado_actual)
    print("distriucion de probabilidad")
    print(probabilidad)

def prueba_generador_letras_estados(estado_futuro: list, estado_actual: list, cantidad_variables: int):
    print("Prueba de generador de letras según estados")
    letras = metodos_comunes.crear_conjunto_de_letras_segun_estados(estado_futuro, estado_actual, cantidad_variables)
    print(letras)


def prueba_generador_matriz_sistema_candidato(matriz, estado_inicial, variables_sistema_candidato):
    matriz_sistema_candidato = generador_matriz.generar_matriz_sistema_candidato(matriz, estado_inicial, variables_sistema_candidato)
    print("Matriz sistema candidato")
    print(matriz_sistema_candidato)
   

def pruba_marginilar(matriz, variables_sistema_candidato):
    print("Prueba de marginalizador")
    matriz = acceso_datos.leer_datos("data.csv")
    print("Marginalizar en estados futuros")
    matriz_marginalizada = marginalizador.marginalizar_en_estados_futuros(matriz, variables_sistema_candidato)
    matriz_marginalizada = marginalizador.marginalizar_en_estados_actuales(matriz_marginalizada, variables_sistema_candidato)

    print("Matriz marginalizada")
    print(matriz_marginalizada)

def prueba_carga_matriz_original():
    print("Prueba de carga de matriz original")
    matriz = acceso_datos.leer_datos("data.csv")
    print("Headers columas")
    print(matriz.columns)
    print(matriz)
    print("Prueba exitosa")


#Pasos para método calcular la probabilidad de una variable e

#1. valid


if __name__ == "__main__":
    main()
