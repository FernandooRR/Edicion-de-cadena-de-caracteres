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
      window = []

      # Verificamos si hay elementos en el chunk que necesitan ser cambiados
      for j, char in enumerate(chunk):
          chunk_index = i + j
          for ref in refList:
              if ref[0] == chunk_index:  # Comparamos el índice del chunk con la posición en refList
                  if len(ref) > 1:
                      volatileStr = list(string) # Creamos una copia del string original
                      volatileStr[j] = ref[2]  # Reemplazamos el carácter en el string
                      window.append("".join(volatileStr))  # Almacenamos la nueva versión del string en la ventana
                      change = True  # Indicamos que hubo un cambio

      if len(window) > 1: #Evalua si hay mas de un cambio registrado en la ventana
        combinaciones = []
        for r in range(2, len(window) + 1):
          combinaciones.extend(itools.combinations(window, r))
        for combinacion in combinaciones:
          window.extend(combinacion)

      # Imprimimos la ventana solo si se realizaron cambios en el chunk
      if change:
        windowList.append(window)

  return windowList
