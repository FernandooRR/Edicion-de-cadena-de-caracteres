import pandas as pd
import itertools as itools

def changeCsvString(data, chunkRange, jump):
  string = data.iloc[0, 3]

  refList = []
  windowList = []
  for i in range(len(data)):
      refList.append([data.iloc[i, 0], data.iloc[i, 1], data.iloc[i, 2]])

  print(string)

  for i in range(0, len(string), jump):
      change = False
      chunk = list(string[i:min(i + chunkRange, len(string))])  # Obtenemos el chunk actual
      changeRefs = []
      window = []
      

      # Verificamos si hay elementos en el chunk que necesitan ser cambiados
      for j, char in enumerate(chunk):
          chunkIndex = i + j          
          nuStr = list(string)
          wset = []
          for ref in refList:
              if ref[0] == chunkIndex:  # Comparamos el índice del chunk con la posición en refList
                  if len(ref) > 1:
                      modStr = list(string) # Creamos una copia del string original
                      modStr[chunkIndex] = ref[2]  # Reemplazamos el carácter en el string
                      nuStr[chunkIndex] = ref[2]
                      changeRefs.append(ref) #Se guardan los registros de cambios en la ventana
                      wset.append("".join(modStr))  # Almacenamos la nueva versión del string en la ventana
                      wset.append(ref)
                      window.append(wset)
                      change = True  # Indicamos que hubo un cambio
      if len(changeRefs) > 2: #Evalua si en la ventana hay mas de 2 cambios registrados
        refComb = []
        for r in range(1,len(changeRefs)):
          refComb.extend(itools.combinations(changeRefs, r)) #Se guarda una lista de posibles combinaciones de registros
        for ref in range(len(changeRefs), len(refComb)): #Se empieza a iterar desde el indice del ultimo elemento de la ventana hasta la longitud de las combinaciones
          print(refComb[ref])
          refs = refComb[ref] #Se guarda en cada iteracion la combinacion de referencias
          combStr = list(string) #Se hace una copia del string en una lista
          wset = []
          for it in refs: #Se itera sobre la combinacion de referencias
            for j, char in enumerate(chunk): #Se itera sobre el chunk              
              chunkIndex = i + j #Se guarda el indice real del string sobre el chunk
              if it[0] == chunkIndex: #revisa si el indice dentro del chunk es igual a la posicion de la referencia actual
                combStr[chunkIndex] = it[2] #Se realiza el cambio
          wset.append("".join(combStr)) #Se agrega el nuevo chunk combinado a la ventana
          wset.append(refs)
          window.append(wset)

      # Se agrega a la lista la ventana solo si se realizaron cambios en el chunk
      if change:
        if len(changeRefs) > 1:
          wset = []
          wset.append("".join(nuStr))
          wset.append(changeRefs)
          window.append(wset)
        windowList.append(window)

  return windowList

def allPosCombs(data):
  combList = []
  string = data.iloc[0, 3]

  refList = []
  strList = []
  for i in range(len(data)):
      refList.append([data.iloc[i, 0], data.iloc[i, 1], data.iloc[i, 2]]) 

  for r in range(len(refList)):
        combList.extend(itools.combinations(refList, r))
  print(combList)
  for i in range(len(combList)):
    refs = combList[i]
    combStr = list(string)
    for j in refs:
      for c, char in enumerate(string):
        if j[0] == c:
          combStr[c] = j[2]
    strList.append("".join(combStr))

  return strList


def combWindows(data,v1, v2):
  string = data.iloc[0, 3]
  refs = []
  combList = []
  strList = []
  for i in v1:
    wset = i 
    refs.append(wset[1])
  for i in v2:
    wset = i
    refs.append(wset[1])

  for r in range(len(refs)):
        combList.extend(itools.combinations(refs, r))
  
  for i in range(len(combList)):
    refs = combList[i]
    combStr = list(string)
    for j in refs:
      for c, char in enumerate(string):
        if j[0] == c:
          combStr[c] = j[2]
    strList.append("".join(combStr))

  return strList
