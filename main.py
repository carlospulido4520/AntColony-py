import string, math, random, copy


'''
Returns an adjacency matrix from a tsp dataset.
''' 
def distancesFromCoords():
    f = open('berlin52.tsp')
    data = [line.replace("\n","").split(" ")[1:] for line in f.readlines()[6:58]]
    coords =  list(map(lambda x: [float(x[0]),float(x[1])], data))
    distances = []
    for i in range(len(coords)):
        row = []
        for j in range(len(coords)):
            row.append(math.sqrt((coords[i][0]-coords[j][0])**2 + (coords[i][1]-coords[j][1])**2))
        distances.append(row)
    return distances

def calcularCosto(ruta):
    costo = 0
    for i in range(len(ruta)-1):
        costo += distancias[ruta[i]][ruta[i+1]]
    return costo

def actualizarFeromona(ruta, costoRuta):
    # print(len(ruta)-1)
    for i in range(len(ruta)-1):
        mFeromonas[ruta[i]][ruta[i+1]] += 1/costoRuta

def evaporacion(p):
    for i in range(len(mFeromonas)):
        for j in range(len(mFeromonas[0])):
            mFeromonas[i][j] *= (1-p)

def exploracion(exploradoras):
    # Rutas
    for i in range(exploradoras):
        ruta = [j for j in range(52)]
        random.shuffle(ruta)
        ruta.append(ruta[0])
        costoRuta = calcularCosto(ruta)
        actualizarFeromona(ruta,costoRuta)

def probabilidad (actual,restantes,alpha,beta):
    p = []
    # denominador = 0
    for i in range(len(restantes)):
        numerador = (mFeromonas[actual][restantes[i]]**alpha) * (mInversa[actual][restantes[i]]**beta)
        
        denominador=0
        for j in range(len(restantes)):
            denominador += (mFeromonas[actual][restantes[j]] ** alpha) * (mInversa[actual][restantes[j]]**beta)
        if denominador == 0:
            p.append(0.0)
        else:
            p.append(numerador/denominador)
    return p

def recorrido(ciudades,ci,alpha,beta):
    # recorrido = [5,1,2,3,4,5]
    #ciudades = [i for i in range(52)]
    ciudades = copy.deepcopy(ciudades)
    ciudades.pop(-1) #linea nueva
    ciudadInicial = ci
    # ciudadInicial = random.choice(ciudades)
    ciudades.remove(ciudadInicial)
    ruta = []
    ruta.append(ciudadInicial)
    z = None #Costo de la ruta

    for i in range(51):
        prob = probabilidad(ruta[-1],ciudades,alpha,beta)
        # print(i,len(prob),type(prob))
        # break
        n = random.uniform(0.01,1)
        p = 0
        for j in range(len(prob)):
            p += prob[j] # Acumulador de probabilidades
            if n < p:
                ruta.append(ciudades[j])
                ciudades.remove(ciudades[j])
                break
    ruta.append(ciudadInicial)
    z = calcularCosto(ruta)
    return ruta,z

if __name__=="__main__":
    distancias = distancesFromCoords()
    
    mInversa = []
    # Llenado de la matriz inversa
    for i in range(len(distancias)):
        mInversa.append([])
        for j in range(len(distancias[0])):
            if distancias[i][j] == 0:
                mInversa[i].append(0.0)
            else:
                mInversa[i].append(1/distancias[i][j])
    
    mFeromonas = []
    # Inicialización de matriz de feromonas en 0.0
    for i in range(len(distancias)):
        mFeromonas.append([])
        for j in range(len(distancias[0])):
            mFeromonas[i].append(0)

    # PARAMETROS 
    exploradoras = 1000 # Cantidad de hormigas exploradoras
    hormigas = 50 # Cantidad de hormigas que recorreran los caminos
    iteraciones = 10 # Cantidad de iteraciones del algoritmo
    alpha = 2
    beta = 1
    p = 0.01 #Factor de evaporacion
    
    exploracion(exploradoras)
    evaporacion(p)

    ciudades = [i for i in range(52)]
    random.shuffle(ciudades)
    ciudadInicial = random.choice(ciudades)
    ciudades.remove(ciudadInicial)
    
    # Para imprimir datos finales
    mostrarRuta = copy.deepcopy(ciudades)
    mostrarRuta.insert(0,ciudadInicial)
    mostrarRuta.append(ciudadInicial)
    costoOptimo = 0
    rutaOptima = 0

    for i in range(iteraciones):
        ruta = copy.deepcopy(ciudades)
        random.shuffle(ruta)
        ruta.insert(0,ciudadInicial)
        ruta.append(ciudadInicial)
        costoAux = 0 #Se va a guardar el costo optimo de cada grupo de hormigas
        
        rutaAux = 0  #Se va a guardar la ruta optima de cada grupo de hormigas
        
        for h in range(hormigas):
            ruta, costo = recorrido(ruta,ciudadInicial,alpha,beta)
            # print(costo)
            # print(ruta)

            
            if h == 0:
                rutaAux = ruta
                costoAux = costo
            
            
            if costo < costoAux:
                costoAux = costo
                rutaAux = ruta
        
        if i == 0:
            costoOptimo = costoAux
            rutaOptima = rutaAux
        if costoAux < costoOptimo:
            costoOptimo = costoAux
            rutaOptima = rutaAux
        print("\nIteración {} de {}".format(i,iteraciones))
        print("Zp: ",costoAux)
        print("Z: ",costoOptimo)
    # ruta.sort() #Para poder contar en orden todas las ciudades y ver que no falte ninguna
    # rutaOptima.sort()
    print("\n\n==> Ciudades a visitar: ",len(ruta))
    print("==> Ciudades visitadas: ",len(rutaOptima))
    print("==> Costo optimo: ",costoOptimo)
    print("==> Optimizar ruta: ",ruta)
    print("\n==> Ruta optima: ",rutaOptima)    