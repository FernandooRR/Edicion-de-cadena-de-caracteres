import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox, font
from tkinter import ttk
import itertools as itools

# Variable global para almacenar la cadena cargada
cadena_actual = ""
datos_csv = None  # Variable global para almacenar los datos del archivo CSV

def inicio():
    editarCadena.config(state='disabled')
    mostrarCombinaciones.config(state='disabled')
    entradaCadena.config(state='disabled')
    botonVentanas.config(state='disabled')
    botonMostrarDatos.config(state='disabled')

# Función para actualizar la cadena en la ventana principal
def actualizarCadena():
    entradaCadena.config(state='normal')
    entradaCadena.delete(1.0, 'end')
    entradaCadena.insert(tk.END, cadena_actual)  # Insertar la cadena actualizada
    entradaCadena.config(state='disabled')

# Función para cargar un archivo CSV
def cargarArchivo():
    global cadena_actual, datos_csv
    rutaArchivo = filedialog.askopenfilename(filetypes=[("Archivos CSV", "*.csv")])
    print(rutaArchivo)  # Agregar esta línea para verificar la ruta del archivo seleccionado
    if rutaArchivo:
        try:
            datos_csv = pd.read_csv(rutaArchivo)
            columna_cadena = 'string'  # Reemplaza 'nombre_de_la_columna' con el nombre real de la columna
            cadena_actual = datos_csv[columna_cadena].iloc[0]  # Obtener la cadena de la columna adecuada
            actualizarCadena()  # Actualizar la cadena en la ventana principal
            editarCadena.config(state='normal')  # Habilitar el botón de editar cadena
            mostrarCombinaciones.config(state='normal')  # Habilitar el botón de mostrar combinaciones
            botonVentanas.config(state='normal')
            botonMostrarDatos.config(state='normal')
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el archivo CSV.")

# Función para guardar la cadena editada
def guardarCadena(ventanaEditar):
    global cadena_actual
    nueva_cadena = entradaCadenaTexto.get(1.0, tk.END)
    cadena_actual = nueva_cadena
    messagebox.showinfo("Guardado", "Cadena guardada exitosamente.")
    actualizarCadena()  # Actualizar la cadena en la ventana principal
    ventanaEditar.destroy()  # Cerrar la ventana de edición

# Función para abrir la ventana de edición de cadena
def editarCadena():
    global cadena_actual
    ventanaEditar = tk.Toplevel(ventana)
    ventanaEditar.title("Edición de cadena")
    ventanaEditar.geometry("800x350")
    ventanaEditar.resizable(0, 0)
    
    cadenaTitulo = tk.Label(ventanaEditar, text="EDICIÓN DE CADENAS")
    cadenaTitulo.grid(row=0, column=0, columnspan=6, padx=30, pady=20, sticky="nsew") 
    
    cadenaTexto = tk.Label(ventanaEditar, text="   Cadena: ")
    cadenaTexto.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    
    global entradaCadenaTexto
    entradaCadenaTexto = tk.Text(ventanaEditar, width=80, height=10, wrap=tk.WORD)  # Ajustar el ancho y alto del widget entradaCadena
    entradaCadenaTexto.grid(row=1, column=1, columnspan=3, padx=5, pady=10, sticky="w")
    entradaCadenaTexto.insert(tk.END, cadena_actual)
    
    botonGuardar = tk.Button(ventanaEditar, text="Guardar", command=lambda: guardarCadena(ventanaEditar), width=15)
    botonGuardar.grid(row=2, column=1, columnspan=3, padx=10, pady=10, sticky="w")
    
    ventanaEditar.protocol("WM_DELETE_WINDOW", actualizarCadena)

def mostrarDatos():
    global datos_csv
    if datos_csv is not None:
        ventanaDatos = tk.Toplevel(ventana)
        ventanaDatos.title("Datos del archivo CSV")
        ventanaDatos.geometry("800x400")
        ventanaDatos.resizable(0, 0)
        
        datosTitulo = tk.Label(ventanaDatos, text="EDICIÓN DE CADENAS")
        datosTitulo.grid(row=0, column=0, columnspan=2, padx=30, pady=20, sticky="nsew") 
        
        tabla = ttk.Treeview(ventanaDatos)
        columnas_mostradas = datos_csv.columns[0:3]  # Seleccionar las columnas de la segunda a la cuarta
        tabla["columns"] = tuple(columnas_mostradas)
        
        # Configurar las columnas del Treeview (mostrando solo las columnas seleccionadas)
        for col in columnas_mostradas:
            tabla.heading(col, text=col)
            tabla.column(col, anchor=tk.CENTER, width=50)
        
        # Insertar los datos en la tabla (solo para las columnas seleccionadas)
        for _, row in datos_csv.iterrows():
            valores_fila = [row[col] for col in columnas_mostradas]
            tabla.insert("", tk.END,values=tuple(valores_fila))
        
        tabla.grid(row=1, column=0, columnspan=1, padx=10, pady=20, sticky="e")
    else:
        messagebox.showwarning("Advertencia", "Primero carga un archivo CSV.")

def mostrarCombinaciones():
    global datos_csv
    if datos_csv is not None:
        ventanaCombinaciones = tk.Toplevel(ventana)
        ventanaCombinaciones.title("Combinaciones de la cadena")
        ventanaCombinaciones.geometry("800x400")
        ventanaCombinaciones.resizable(0, 0)
        
        chunkRange = 3  # Definir el rango del chunk
        jump = 1  # Definir el valor de salto
        
        # Llamar a la función changeCsvString para obtener las combinaciones
        combinaciones = changeCsvString(datos_csv, chunkRange, jump)
        
        # Mostrar las combinaciones en una lista
        for i, window in enumerate(combinaciones):
            label = tk.Label(ventanaCombinaciones, text=f"Ventana {i+1}:")
            label.pack()
            for comb in window:
                tk.Label(ventanaCombinaciones, text=comb).pack()
    else:
        messagebox.showwarning("Advertencia", "Primero carga un archivo CSV.")

def mostrarVentanas(data, chunkRange, jump):
    ventanaVentanas = tk.Toplevel()  # Crear una nueva ventana emergente
    ventanaVentanas.title("Ventanas de Cambio")  # Establecer el título de la ventana
    ventanaVentanas.geometry("800x400")  # Establecer las dimensiones de la ventana
    
    try:
        # Llamar a la función changeCsvString para obtener las ventanas de cambio
        ventanas = changeCsvString(data, chunkRange, jump)
        
        for i, window in enumerate(ventanas):
            tk.Label(ventanaVentanas, text=f"Ventana {i+1}:", font=("Arial", 12, "bold")).pack()  # Etiqueta para el número de ventana
            for w in window:
                tk.Label(ventanaVentanas, text=w).pack()  # Mostrar cada ventana de cambio en una etiqueta de texto
    except Exception as e:
        messagebox.showerror("Error", f"Se produjo un error al procesar los datos: {e}")  # Manejar cualquier error con un mensaje de error

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

def changeCsvChunk(data, chunkRange, jump):
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
          combChunk = chunk
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

# Crear la interfaz gráfica
ventana = tk.Tk()
ventana.title("Edición de cadenas de caracteres")
#ventana.iconbitmap(r"./02.ico")  # Comentado temporalmente
ventana.geometry("800x350")
ventana.resizable(0, 0)

fuente = font.Font(family="Gadugi", size=12)

# Etiqueta para el título
Titulo = tk.Label(ventana, text="EDICIÓN DE CADENAS DE CARÁCTERES")
Titulo.grid(row=0, column=0, columnspan=6, padx=30, pady=20, sticky="nsew")

cadena = tk.Label(ventana, text="   Cadena: ")
cadena.grid(row=1, column=0, padx=10, pady=10, sticky="w")
entradaCadena = tk.Text(ventana, width=80, height=10, wrap=tk.WORD)  # Ajustar el ancho y alto del widget entradaCadena
entradaCadena.grid(row=1, column=1, columnspan=5, padx=5, pady=10, sticky="w")

# Botónes
botonCargarArchivo = tk.Button(ventana, text="Cargar archivo", command=cargarArchivo, width=15)
botonCargarArchivo.grid(row=2, column=1, padx=(10, 2), pady=20, sticky="ew")

editarCadena = tk.Button(ventana, text="Editar cadena", command=editarCadena, width=15)
editarCadena.grid(row=2, column=2, padx=2, pady=20, sticky="ew")

botonMostrarDatos = tk.Button(ventana, text="Mostrar datos", command=mostrarDatos, width=15)
botonMostrarDatos.grid(row=2, column=3, padx=2, pady=20, sticky="ew")

botonVentanas = tk.Button(ventana, text="Mostrar ventanas", command=lambda: mostrarVentanas(datos_csv, 3, 1), width=15)
botonVentanas.grid(row=2, column=4, padx=2, pady=20, sticky="ew")


mostrarCombinaciones = tk.Button(ventana, text="Combinaciones", command=mostrarCombinaciones, width=15)
mostrarCombinaciones.grid(row=2, column=5, padx=(2, 10), pady=20, sticky="ew")

inicio()

ventana.mainloop()
