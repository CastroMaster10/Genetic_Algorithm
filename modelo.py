import time
import random
import timeit
import statistics

#generarmos soluciones iniciales

def generar_poblacion_inicial(n_individuos, longitud_individuo,beneficios):
    poblacion = {}
    for _ in range(n_individuos):
        individuo = ''.join(random.choice('01') for _ in range(longitud_individuo))
        fitness =  sum(int(bit)*peso for bit, peso in zip(individuo, beneficios))
        poblacion[individuo] = fitness
    return poblacion


def filtrar_poblacion(poblacion, pesos, beneficios,peso_maximo):
    poblacion_filtrada = {}
    for individuo in poblacion:
        peso_total = sum(int(bit)*peso for bit, peso in zip(individuo, pesos))
        fitness =  sum(int(bit)*peso for bit, peso in zip(individuo, beneficios))
        if peso_total <= peso_maximo:
            poblacion_filtrada[individuo] = fitness
    return poblacion_filtrada

def ordenar_poblacion(poblacion):
    return {k: v for k, v in sorted(poblacion.items(), key=lambda item: item[1])}


def algoritmoGenetico(poblacion_inicial,pesos,beneficios,factibilidad,pesoMaximo=800,n=100):

    poblacion = ordenar_poblacion(poblacion_inicial)
    p_cruce = 0.9#probabilidad de cruce
    p_mutacion = 0.1#probabilidad de mutacion

    for x in range(n):
        individuos  = list(poblacion.keys())
        funcionesFitness = list(poblacion.values())
        #Elegimos aleatoriamente dos padres de la poblacion inicial
        cruce = random.random()
        if cruce < p_cruce:
            numero_padre1,numero_padre2 = random.sample(range(0, len(individuos)), 2) #numero de padre
            padre1 = individuos[numero_padre1]
            padre2 = individuos[numero_padre2]

            hijo1 = padre1[0:5] + padre2[5:10]
            hijo2 = padre2[0:5] + padre1[5:10]

            for i in range(0,len(hijo1)):
                mutacion = random.random()
                if mutacion < p_mutacion:
                    if hijo1[i] == '1':
                        hijo1[i] ==  '0'
                    else:
                        hijo1[i] == '1'


            for i in range(0,len(hijo2)):
                mutacion = random.random()
                if mutacion < p_mutacion:
                    if hijo1[i] == '1':
                        hijo1[i] ==  '0'
                    else:
                        hijo1[i] == '1'
            
            fitnessHijo1 = sum(int(bit)*peso for bit, peso in zip(hijo1, beneficios))
            fitnessHijo2 = sum(int(bit)*peso for bit, peso in zip(hijo2, beneficios))

            #factibilidad
            nofueFactible1 = False
            nofueFactible2 = False

            if factibilidad:
                pesoHijo1 = sum(int(bit)*peso for bit, peso in zip(hijo1, pesos))
                pesoHijo2 = sum(int(bit)*peso for bit, peso in zip(hijo2, pesos))
                if pesoHijo1 > pesoMaximo:
                    #hijo1 = padre1
                    #fitnessHijo1 = sum(int(bit)*peso for bit, peso in zip(padre1, beneficios))
                    nofueFactible1 = True
                if pesoHijo2 > pesoMaximo:
                    #hijo2 = padre2
                    #fitnessHijo2 = sum(int(bit)*peso for bit, peso in zip(padre2, beneficios))
                    nofueFactible2 = True

                

            if fitnessHijo2 > fitnessHijo1 and nofueFactible1 == False and nofueFactible2 == False:
                individuos[0] = hijo1
                individuos[1] = hijo2

                funcionesFitness[0] = fitnessHijo1
                funcionesFitness[1] = fitnessHijo2

            elif fitnessHijo1 > fitnessHijo2 and nofueFactible1 == False and nofueFactible2 == False:
                individuos[0] = hijo2
                individuos[1] = hijo1

                funcionesFitness[0] = fitnessHijo2
                funcionesFitness[1] = fitnessHijo1
            
            elif  fitnessHijo2 > fitnessHijo1 and nofueFactible1 == True and nofueFactible2 == False:
                individuos[0] = hijo2
                funcionesFitness[0] = fitnessHijo2
            
            elif  fitnessHijo2 > fitnessHijo1 and nofueFactible1 == False and nofueFactible2 == True:
                individuos[0] = hijo1
                funcionesFitness[0] = fitnessHijo1
            
            else:
                continue
                
            poblacion = ordenar_poblacion(dict(zip(individuos,funcionesFitness)))
    
    return poblacion






            

            
            
# Definir los pesos de los contenedores del problema1
pesos1 = [61,58,92,50,108,83,93,101,54,50,72,51,100,108,91,112,66,58,110,73]
beneficios1 = [1100,1147,1442,1591,1078,1385,1777,1196,1753,1371,1517,1675,1193,1177,1365,1143,1314,1526,1470,1605] #beneficios por los contenedores

# Genera una población inicial de 64 individuos, cada uno de los cuales es una cadena binaria de 10 dígitos
poblacion_inicial_sinFactibilidad = generar_poblacion_inicial(64, 20,beneficios1)
poblacion_inicial = filtrar_poblacion(poblacion_inicial_sinFactibilidad,pesos1,beneficios1,peso_maximo=800)

print(poblacion_inicial)
print()

#Contamos el tiempo de ejecucion promedio
tiemposPromedio = []
soluciones = []

for i in range(200):
    start_time = timeit.default_timer()
    poblacionFinal1 = algoritmoGenetico(poblacion_inicial,pesos1,beneficios1,factibilidad=True,pesoMaximo=800,n=100)
    end_time = timeit.default_timer()
    execution_time =  end_time - start_time
    tiemposPromedio.append(execution_time)
    soluciones.append(list(poblacionFinal1.items())[-1])
#print(poblacionFinal1)
print(f'\n Tiempo de ejecucion promedio del algoritmo: {statistics.mean(tiemposPromedio)}')
print(f'\n Funcion objetivo (promedio): {statistics.mean(soluciones)}')



        

    












