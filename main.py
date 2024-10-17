from proyecto.acceso_datos import AccesoDatos
from proyecto.generador_matriz import GeneradorMatriz

acceso_datos = AccesoDatos()
generador_matriz = GeneradorMatriz()

def main():
    matriz = acceso_datos.leer_datos("data.csv")
    print(matriz)
    estado_inicial = [0, 1, 1, 0]
    variables_sitema_candidato = [1, 1, 1, 0] # 1 indica que se tiene en cuenta la variable, 0 que no se tiene en cuenta A, B, C menos D

    matriz_sistema_candidato = generador_matriz.generar_matriz_sistema_candidato(matriz, estado_inicial, variables_sitema_candidato)

    print("Matriz sistema candidato")
    print(matriz_sistema_candidato)


def prueba_carga_matriz_original():
    print("Prueba de carga de matriz original")
    matriz = acceso_datos.leer_datos("data.csv")
    print("Headers columas")
    print(matriz.columns)
    print(matriz)
    print("Prueba exitosa")



    

if __name__ == "__main__":
    main()
