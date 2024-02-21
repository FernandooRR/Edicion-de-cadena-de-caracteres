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
          chunk_index = i + j
          nuStr = list(string)
          for ref in refList:
              if ref[0] == chunk_index:  # Comparamos el índice del chunk con la posición en refList
                  if len(ref) > 1:
                      modStr = list(string) # Creamos una copia del string original
                      modStr[j] = ref[2]  # Reemplazamos el carácter en el string
                      nuStr[j] = ref[2]
                      changeRefs.append(ref)
                      window.append("".join(modStr))  # Almacenamos la nueva versión del string en la ventana
                      change = True  # Indicamos que hubo un cambio
      if len(changeRefs) > 2:
        refComb = []
        for r in range(1,len(changeRefs)):
          refComb.extend(itools.combinations(changeRefs, r))
        for ref in range(len(changeRefs), len(refComb)):
          print(refComb[ref])
          refs = refComb[ref]
          combStr = list(string)
          for it in refs:
            for j, char in enumerate(chunk):
              chunkIndex = i + j
              if it[0] == chunkIndex:
                combStr[j] = it[2]
          window.append("".join(combStr))

      if change:
        if len(changeRefs) > 1:
          window.append("".join(nuStr))
        windowList.append(window)

  return windowList

      # Imprimimos la ventana solo si se realizaron cambios en el chunk
      if change:
        windowList.append(window)

  return windowList
