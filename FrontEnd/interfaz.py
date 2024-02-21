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
            botonMostrarDatos.config(state='normal')
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el archivo CSV.")

# Función para guardar la cadena editada
def guardarCadena(ventanaEditar):
    global cadena_actual, datos_csv
    nueva_cadena = entradaCadenaTexto.get(1.0, tk.END)
    cadena_actual = nueva_cadena.strip()  # Eliminar espacios en blanco al principio y al final
    messagebox.showinfo("Guardado", "Cadena guardada exitosamente.")
    actualizarCadena()  # Actualizar la cadena en la ventana principal
    if datos_csv is not None:
        # Actualizar la columna correspondiente con la nueva cadena
        columna_cadena = 'string'  # Reemplaza 'nombre_de_la_columna' con el nombre real de la columna
        datos_csv[columna_cadena] = cadena_actual
    ventanaEditar.destroy() 

# Función para abrir la ventana de edición de cadena
def editarCadena():
    global cadena_actual
    ventanaEditar = tk.Toplevel(ventana)
    ventanaEditar.title("Edición de cadena")
    ventanaEditar.geometry("800x350")
    ventanaEditar.resizable(0, 0)
    
    cadenaTitulo = tk.Label(ventanaEditar, text="EDICIÓN DE CADENAS", font=("Gadugi", 14, "bold"))
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
        
        datosTitulo = tk.Label(ventanaDatos, text="DATOS DEL ARCHIVO CSV", font=("Gadugi", 14, "bold"))
        datosTitulo.pack(pady=(50, 20))  # Alineado verticalmente en el centro
        
        # Crear un frame para contener la tabla y ocupar todo el espacio de la ventana
        tabla_frame = tk.Frame(ventanaDatos)
        tabla_frame.pack(expand=False, fill="none")  # Abarca todo el espacio
        
        tabla = ttk.Treeview(tabla_frame)
        columnas_mostradas = datos_csv.columns[0:3]  # Seleccionar las columnas de la segunda a la cuarta
        tabla["columns"] = tuple(columnas_mostradas)
        
        # Configurar las columnas del Treeview (mostrando solo las columnas seleccionadas)
        for col in columnas_mostradas:
            tabla.heading(col, text=col)
            tabla.column(col, anchor=tk.CENTER, width=80)
        
        # Insertar los datos en la tabla (solo para las columnas seleccionadas)
        for _, row in datos_csv.iterrows():
            valores_fila = [row[col] for col in columnas_mostradas]
            tabla.insert("", tk.END, values=tuple(valores_fila))
        
        tabla.pack(expand=True, fill="both")  # Abarca todo el espacio del frame
    else:
        messagebox.showwarning("Advertencia", "Primero carga un archivo CSV.")



def mostrarCombinaciones():
    global datos_csv
    if datos_csv is not None:
        ventanaCombinaciones = tk.Toplevel(ventana)
        ventanaCombinaciones.title("Combinaciones de la cadena")
        ventanaCombinaciones.geometry("700x300")
        ventanaCombinaciones.resizable(0, 0)
        
        combinacionesTitulo = tk.Label(ventanaCombinaciones, text="COMBINACIONES", font=("Gadugi", 14, "bold"))
        combinacionesTitulo.pack(pady=20)
        
        # Crear un frame para contener las combinaciones y la barra de desplazamiento
        frame_combinaciones = tk.Frame(ventanaCombinaciones)  # Limitar el espacio del frame
        frame_combinaciones.pack(expand=False, fill="none")
        
        # Crear una barra de desplazamiento vertical
        scrollbar = tk.Scrollbar(frame_combinaciones, orient="vertical")
        scrollbar.pack(side="right", fill="y")
        
        # Crear una lista para mostrar las combinaciones
        lista_combinaciones = tk.Listbox(frame_combinaciones, yscrollcommand=scrollbar.set, width=100)
        lista_combinaciones.pack(expand=True, fill="both")
        
        scrollbar.config(command=lista_combinaciones.yview)
        
        chunkRange = 10  # Definir el rango del chunk
        jump = 5  # Definir el valor de salto
        
        combinaciones = changeCsvString(datos_csv, chunkRange, jump)
        
        # Mostrar las combinaciones en la lista
        for i, window in enumerate(combinaciones):
            lista_combinaciones.insert(tk.END, f"Ventana {i+1}:")
            for comb in window:
                lista_combinaciones.insert(tk.END, comb)
                lista_combinaciones.insert(tk.END, "")  # Insertar un espacio en blanco

        
        # Agregar un botón debajo del frame
        boton_descargar = tk.Button(ventanaCombinaciones, text="Descargar TXT", command=lambda: descargarTXT(combinaciones))
        boton_descargar.pack(pady=20)
        
    else:
        messagebox.showwarning("Advertencia", "Primero carga un archivo CSV.")

def descargarTXT(combinaciones):
    ruta_archivo = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivo de texto", "*.txt")])
    if ruta_archivo:
        with open(ruta_archivo, mode='w') as file:
            for window in combinaciones:
                for comb in window:
                    file.write(comb + '\n')

def changeCsvString(data, chunkRange, jump):
    string = data.iloc[0, 3]
    refList = []
    windowList = []

    for i in range(len(data)):
        refList.append([data.iloc[i, 0], data.iloc[i, 1], data.iloc[i, 2]])

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

        # Generar todas las combinaciones posibles de cambios en el chunk
        if len(changeRefs) > 1:
            for r in range(2, len(changeRefs) + 1):
                refComb = itools.combinations(changeRefs, r)
                for refs in refComb:
                    combStr = list(string)
                    for it in refs:
                        for jj, char in enumerate(chunk):
                            chunkIndex = i + jj
                            if it[0] == chunkIndex:
                                combStr[jj] = it[2]
                    window.append("".join(combStr))

        if change:
            if len(changeRefs) > 1:
                window.append("".join(nuStr))
            windowList.append(window)
    
    return windowList

# Crear la interfaz gráfica
ventana = tk.Tk()
#ventana.iconbitmap(r"./02.ico")  # Comentado temporalmente
ventana.geometry("800x350")
ventana.resizable(0, 0)

fuente = font.Font(family="Gadugi", size=12)
fuente_titulo = font.Font(family="Gadugi", size=14, weight="bold")
# Etiqueta para el título
Titulo = tk.Label(ventana, text="EDICIÓN DE CADENAS DE CARACTERES", font=fuente_titulo)
Titulo.grid(row=0, column=0, columnspan=6, padx=30, pady=20, sticky="nsew")

cadena = tk.Label(ventana, text="   Cadena: ")
cadena.grid(row=1, column=0, padx=10, pady=10, sticky="w")
entradaCadena = tk.Text(ventana, width=80, height=10, wrap=tk.WORD)  # Ajustar el ancho y alto del widget entradaCadena
entradaCadena.grid(row=1, column=1, columnspan=4, padx=5, pady=10, sticky="w")

# Botónes
botonCargarArchivo = tk.Button(ventana, text="Cargar archivo", command=cargarArchivo, width=15)
botonCargarArchivo.grid(row=2, column=1, padx=(10, 2), pady=20, sticky="ew")

editarCadena = tk.Button(ventana, text="Editar cadena", command=editarCadena, width=15)
editarCadena.grid(row=2, column=2, padx=2, pady=20, sticky="ew")

botonMostrarDatos = tk.Button(ventana, text="Mostrar datos", command=mostrarDatos, width=15)
botonMostrarDatos.grid(row=2, column=3, padx=2, pady=20, sticky="ew")

mostrarCombinaciones = tk.Button(ventana, text="Combinaciones", command=mostrarCombinaciones, width=15)
mostrarCombinaciones.grid(row=2, column=4, padx=(2, 10), pady=20, sticky="ew")

inicio()

ventana.mainloop()
