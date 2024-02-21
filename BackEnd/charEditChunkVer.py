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
      nuChunk = chunk.copy()
      window = []
      changeRefs = []
      chunkIndex = 0
      # Verificamos si hay elementos en el chunk que necesitan ser cambiados
      for j, char in enumerate(chunk):
          chunkIndex = i + j
          for ref in refList:
              if ref[0] == chunkIndex:  # Comparamos el índice del chunk con la posición en refList
                  if len(ref) > 1:
                      modChunk = chunk[:]  # Creamos una copia del chunk original
                      modChunk[j] = ref[2]  # Reemplazamos el carácter en el chunk
                      nuChunk[j] = ref[2]
                      changeRefs.append(ref)
                      window.append("".join(modChunk))  # Almacenamos la nueva versión del chunk en la ventana
                      change = True  # Indicamos que hubo un cambio
      
      if len(changeRefs) > 2:
        refComb = []
        for r in range(1,len(changeRefs)):
          refComb.extend(itools.combinations(changeRefs, r))
        for ref in range(len(changeRefs), len(refComb)):
          print(refComb[ref])
          refs = refComb[ref]
          combChunk = chunk.copy()
          for it in refs:
            for j, char in enumerate(chunk):
              chunkIndex = i + j
              if it[0] == chunkIndex:
                combChunk[j] = it[2]
          window.append("".join(combChunk))

      if change:
        if len(changeRefs) > 1:
          window.append("".join(nuChunk))
        windowList.append(window)

  return windowList

