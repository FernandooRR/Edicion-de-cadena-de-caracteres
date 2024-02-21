# Importación de módulos necesarios
import pandas as pd  # Importa la librería Pandas para el manejo de datos
import tkinter as tk  # Importa la librería Tkinter para la interfaz gráfica
from tkinter import filedialog, messagebox, font  # Importa clases y funciones específicas de Tkinter
from tkinter import ttk  # Importa widgets temáticos de Tkinter
import itertools as itools  # Importa funciones para trabajar con iterables

# Variable global para almacenar la cadena cargada
cadena_actual = ""  # Inicializa una cadena vacía
datos_csv = None  # Inicializa una variable para almacenar los datos del archivo CSV

# Función para deshabilitar ciertos elementos al inicio
def inicio():
    editarCadena.config(state='disabled')  # Deshabilita el botón de editar cadena
    mostrarCombinaciones.config(state='disabled')  # Deshabilita el botón de mostrar combinaciones
    entradaCadena.config(state='disabled')  # Deshabilita el widget de entrada de cadena
    botonMostrarDatos.config(state='disabled')  # Deshabilita el botón de mostrar datos

# Función para actualizar la cadena en la ventana principal
def actualizarCadena():
    entradaCadena.config(state='normal')  # Habilita el widget de entrada de cadena
    entradaCadena.delete(1.0, 'end')  # Borra el contenido anterior
    entradaCadena.insert(tk.END, cadena_actual)  # Inserta la cadena actualizada
    entradaCadena.config(state='disabled')  # Deshabilita el widget de entrada de cadena nuevamente

# Función para cargar un archivo CSV
def cargarArchivo():
    global cadena_actual, datos_csv  # Indica que se usará la variable global cadena_actual y datos_csv
    rutaArchivo = filedialog.askopenfilename(filetypes=[("Archivos CSV", "*.csv")])  # Abre el cuadro de diálogo para seleccionar un archivo
    print(rutaArchivo)  # Imprime la ruta del archivo seleccionado (opcional)
    if rutaArchivo:
        try:
            datos_csv = pd.read_csv(rutaArchivo)  # Lee el archivo CSV y lo almacena en datos_csv
            columna_cadena = 'string'  # Define la columna de la cadena (cambiar por el nombre real)
            cadena_actual = datos_csv[columna_cadena].iloc[0]  # Obtiene la cadena de la columna especificada
            actualizarCadena()  # Llama a la función para actualizar la cadena en la ventana principal
            editarCadena.config(state='normal')  # Habilita el botón de editar cadena
            mostrarCombinaciones.config(state='normal')  # Habilita el botón de mostrar combinaciones
            botonMostrarDatos.config(state='normal')  # Habilita el botón de mostrar datos
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el archivo CSV.")  # Muestra un mensaje de error si falla la carga del archivo

# Función para guardar la cadena editada
def guardarCadena(ventanaEditar):
    global cadena_actual, datos_csv  # Indica que se usará la variable global cadena_actual y datos_csv
    nueva_cadena = entradaCadenaTexto.get(1.0, tk.END)  # Obtiene la nueva cadena del widget de entrada
    cadena_actual = nueva_cadena.strip()  # Elimina los espacios en blanco al principio y al final de la cadena
    messagebox.showinfo("Guardado", "Cadena guardada exitosamente.")  # Muestra un mensaje informativo
    actualizarCadena()  # Llama a la función para actualizar la cadena en la ventana principal
    if datos_csv is not None:  # Verifica si hay datos cargados
        columna_cadena = 'string'  # Define la columna de la cadena (cambiar por el nombre real)
        datos_csv[columna_cadena] = cadena_actual  # Actualiza la columna correspondiente con la nueva cadena
    ventanaEditar.destroy()  # Cierra la ventana de edición de cadena

# Función para abrir la ventana de edición de cadena
def editarCadena():
    global cadena_actual  # Indica que se usará la variable global cadena_actual
    ventanaEditar = tk.Toplevel(ventana)  # Crea una nueva ventana emergente
    ventanaEditar.title("Edición de cadena")  # Establece el título de la ventana
    ventanaEditar.geometry("800x350")  # Establece las dimensiones de la ventana
    ventanaEditar.resizable(0, 0)  # Evita que la ventana sea redimensionable
    
    cadenaTitulo = tk.Label(ventanaEditar, text="EDICIÓN DE CADENAS", font=("Gadugi", 14, "bold"))  # Crea una etiqueta con el título
    cadenaTitulo.grid(row=0, column=0, columnspan=6, padx=30, pady=20, sticky="nsew")  # Coloca la etiqueta en la ventana
    
    cadenaTexto = tk.Label(ventanaEditar, text="   Cadena: ")  # Crea una etiqueta para la cadena
    cadenaTexto.grid(row=1, column=0, padx=10, pady=10, sticky="w")  # Coloca la etiqueta en la ventana
    
    global entradaCadenaTexto  # Indica que se usará la variable global entradaCadenaTexto
    entradaCadenaTexto = tk.Text(ventanaEditar, width=80, height=10, wrap=tk.WORD)  # Crea un widget de entrada de texto
    entradaCadenaTexto.grid(row=1, column=1, columnspan=3, padx=5, pady=10, sticky="w")  # Coloca el widget en la ventana
    entradaCadenaTexto.insert(tk.END, cadena_actual)  # Inserta la cadena actual en el widget
    
    botonGuardar = tk.Button(ventanaEditar, text="Guardar", command=lambda: guardarCadena(ventanaEditar), width=15)  # Crea un botón para guardar la cadena
    botonGuardar.grid(row=2, column=1, columnspan=3, padx=10, pady=10, sticky="w")  # Coloca el botón en la ventana
    
    ventanaEditar.protocol("WM_DELETE_WINDOW", actualizarCadena)  # Configura el comportamiento al cerrar la ventana

# Función para mostrar los datos del archivo CSV en una nueva ventana
def mostrarDatos():
    global datos_csv  # Indica que se usará la variable global datos_csv
    if datos_csv is not None:  # Verifica si hay datos cargados
        ventanaDatos = tk.Toplevel(ventana)  # Crea una nueva ventana emergente
        ventanaDatos.title("Datos del archivo CSV")  # Establece el título de la ventana
        ventanaDatos.geometry("700x350")  # Establece las dimensiones de la ventana
        ventanaDatos.resizable(0, 0)  # Evita que la ventana sea redimensionable
        
        datosTitulo = tk.Label(ventanaDatos, text="DATOS DEL ARCHIVO CSV", font=("Gadugi", 14, "bold"))  # Crea una etiqueta con el título
        datosTitulo.pack(pady=20)  # Alinea verticalmente la etiqueta en la ventana
        
        tabla_frame = tk.Frame(ventanaDatos)  # Crea un frame para contener la tabla
        tabla_frame.pack(expand=False, fill="none")  # Ajusta el frame al tamaño de la tabla
        
        tabla = ttk.Treeview(tabla_frame)  # Crea una tabla
        columnas_mostradas = datos_csv.columns[0:3]  # Selecciona las primeras tres columnas para mostrar
        tabla["columns"] = tuple(columnas_mostradas)  # Configura las columnas de la tabla
        
        # Configura las columnas del Treeview
        for col in columnas_mostradas:
            tabla.heading(col, text=col)  # Establece los encabezados de las columnas
            tabla.column(col, anchor=tk.CENTER, width=80)  # Ajusta el ancho de las columnas
        
        # Inserta los datos en la tabla
        for _, row in datos_csv.iterrows():
            valores_fila = [row[col] for col in columnas_mostradas]  # Obtiene los valores de la fila
            tabla.insert("", tk.END, values=tuple(valores_fila))  # Inserta la fila en la tabla
        
        tabla.pack(expand=True, fill="both")  # Ajusta la tabla al tamaño del frame
    else:
        messagebox.showwarning("Advertencia", "Primero carga un archivo CSV.")  # Muestra un mensaje de advertencia si no hay datos cargados

# Función para mostrar las combinaciones de la cadena en una nueva ventana
def mostrarCombinaciones():
    global datos_csv  # Indica que se usará la variable global datos_csv
    if datos_csv is not None:  # Verifica si hay datos cargados
        ventanaCombinaciones = tk.Toplevel(ventana)  # Crea una nueva ventana emergente
        ventanaCombinaciones.title("Combinaciones de la cadena")  # Establece el título de la ventana
        ventanaCombinaciones.geometry("700x300")  # Establece las dimensiones de la ventana
        ventanaCombinaciones.resizable(0, 0)  # Evita que la ventana sea redimensionable
        
        combinacionesTitulo = tk.Label(ventanaCombinaciones, text="COMBINACIONES", font=("Gadugi", 14, "bold"))  # Crea una etiqueta con el título
        combinacionesTitulo.pack(pady=20)  # Alinea verticalmente la etiqueta en la ventana
        
        # Crea un frame para contener las combinaciones y la barra de desplazamiento
        frame_combinaciones = tk.Frame(ventanaCombinaciones)  # Crea un frame
        frame_combinaciones.pack(expand=False, fill="none")  # Ajusta el frame al tamaño de las combinaciones
        
        scrollbar = tk.Scrollbar(frame_combinaciones, orient="vertical")  # Crea una barra de desplazamiento vertical
        scrollbar.pack(side="right", fill="y")  # Coloca la barra de desplazamiento a la derecha
        
        lista_combinaciones = tk.Listbox(frame_combinaciones, yscrollcommand=scrollbar.set, width=100)  # Crea una lista para mostrar las combinaciones
        lista_combinaciones.pack(expand=True, fill="both")  # Ajusta la lista al tamaño del frame
        
        scrollbar.config(command=lista_combinaciones.yview)  # Configura la barra de desplazamiento para que funcione con la lista
        
        chunkRange = 10  # Define el rango del chunk
        jump = 5  # Define el valor de salto
        
        combinaciones = changeCsvString(datos_csv, chunkRange, jump)  # Obtiene las combinaciones de la cadena
        
        # Muestra las combinaciones en la lista
        for i, window in enumerate(combinaciones):
            lista_combinaciones.insert(tk.END, f"Ventana {i+1}:")
            for comb in window:
                lista_combinaciones.insert(tk.END, comb)
                lista_combinaciones.insert(tk.END, "")  # Inserta un espacio en blanco
        
        boton_descargar = tk.Button(ventanaCombinaciones, text="Descargar TXT", command=lambda: descargarTXT(combinaciones))  # Crea un botón para descargar las combinaciones
        boton_descargar.pack(pady=20)  # Coloca el botón debajo del frame de combinaciones
    else:
        messagebox.showwarning("Advertencia", "Primero carga un archivo CSV.")  # Muestra un mensaje de advertencia si no hay datos cargados

# Función para descargar las combinaciones en un archivo de texto
def descargarTXT(combinaciones):
    ruta_archivo = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivo de texto", "*.txt")])  # Abre el cuadro de diálogo para seleccionar la ruta del archivo
    if ruta_archivo:
        with open(ruta_archivo, mode='w') as file:
            for window in combinaciones:
                for comb in window:
                    file.write(comb + '\n')  # Escribe cada combinación en el archivo, seguida de un salto de línea

# Función para generar las combinaciones de la cadena
def changeCsvString(data, chunkRange, jump):
    string = data.iloc[0, 3]  # Obtiene la cadena de la cuarta columna del primer registro
    refList = []  # Inicializa una lista para almacenar referencias
    windowList = []  # Inicializa una lista para almacenar ventanas de combinaciones

    for i in range(len(data)):
        refList.append([data.iloc[i, 0], data.iloc[i, 1], data.iloc[i, 2]])  # Añade las referencias a la lista

    for i in range(0, len(string), jump):
        change = False  # Bandera para indicar si hubo cambios en el chunk actual
        chunk = list(string[i:min(i + chunkRange, len(string))])  # Obtiene el chunk actual
        changeRefs = []  # Lista para almacenar referencias que requieren cambios
        window = []  # Inicializa una ventana de combinaciones

        # Verifica si hay elementos en el chunk que necesitan ser cambiados
        for j, char in enumerate(chunk):
            chunk_index = i + j  # Índice del carácter en la cadena completa
            nuStr = list(string)  # Crea una copia de la cadena original
            for ref in refList:
                if ref[0] == chunk_index:  # Compara el índice del chunk con la posición en refList
                    if len(ref) > 1:  # Verifica si hay un carácter de reemplazo
                        modStr = list(string)  # Crea una copia de la cadena original
                        modStr[j] = ref[2]  # Reemplaza el carácter en el chunk
                        nuStr[j] = ref[2]  # Reemplaza el carácter en la copia de la cadena completa
                        changeRefs.append(ref)  # Añade la referencia a la lista de cambios
                        window.append("".join(modStr))  # Almacena la nueva versión del chunk en la ventana
                        change = True  # Indica que hubo un cambio en el chunk

        # Genera todas las combinaciones posibles de cambios en el chunk
        if len(changeRefs) > 1:
            for r in range(2, len(changeRefs) + 1):
                refComb = itools.combinations(changeRefs, r)  # Genera combinaciones de referencias
                for refs in refComb:
                    combStr = list(string)  # Crea una copia del chunk original
                    for it in refs:
                        for jj, char in enumerate(chunk):
                            chunkIndex = i + jj  # Índice del carácter en el chunk
                            if it[0] == chunkIndex:
                                combStr[jj] = it[2]  # Reemplaza el carácter en el chunk
                    window.append("".join(combStr))  # Almacena la combinación en la ventana

        if change:
            if len(changeRefs) > 1:
                window.append("".join(nuStr))  # Almacena la copia de la cadena completa con los cambios
            windowList.append(window)  # Añade la ventana a la lista de ventanas de combinaciones
    
    return windowList  # Retorna la lista de ventanas de combinaciones

# Configuración de la interfaz gráfica
ventana = tk.Tk()  # Crea la ventana principal
ventana.geometry("800x350")  # Establece las dimensiones de la ventana
ventana.resizable(0, 0)  # Evita que la ventana sea redimensionable

fuente = font.Font(family="Gadugi", size=12)  # Define la fuente para la interfaz gráfica
fuente_titulo = font.Font(family="Gadugi", size=14, weight="bold")  # Define la fuente para los títulos

# Etiqueta para el título
Titulo = tk.Label(ventana, text="EDICIÓN DE CADENAS DE CARACTERES", font=fuente_titulo)  # Crea una etiqueta con el título
Titulo.grid(row=0, column=0, columnspan=6, padx=30, pady=20, sticky="nsew")  # Coloca la etiqueta en la ventana

# Etiqueta y widget de entrada para la cadena
cadena = tk.Label(ventana, text="   Cadena: ")  # Crea una etiqueta para la cadena
cadena.grid(row=1, column=0, padx=10, pady=10, sticky="w")  # Coloca la etiqueta en la ventana
entradaCadena = tk.Text(ventana, width=80, height=10, wrap=tk.WORD)  # Crea un widget de entrada de texto
entradaCadena.grid(row=1, column=1, columnspan=4, padx=5, pady=10, sticky="w")  # Coloca el widget en la ventana

# Botones para cargar archivo, editar cadena, mostrar datos y mostrar combinaciones
botonCargarArchivo = tk.Button(ventana, text="Cargar archivo", command=cargarArchivo, width=15)  # Crea un botón para cargar un archivo
botonCargarArchivo.grid(row=2, column=1, padx=(10, 2), pady=20, sticky="ew")  # Coloca el botón en la ventana
editarCadena = tk.Button(ventana, text="Editar cadena", command=editarCadena, width=15)  # Crea un botón para editar la cadena
editarCadena.grid(row=2, column=2, padx=2, pady=20, sticky="ew")  # Coloca el botón en la ventana
botonMostrarDatos = tk.Button(ventana, text="Mostrar datos", command=mostrarDatos, width=15)  # Crea un botón para mostrar los datos
botonMostrarDatos.grid(row=2, column=3, padx=2, pady=20, sticky="ew")  # Coloca el botón en la ventana
mostrarCombinaciones = tk.Button(ventana, text="Combinaciones", command=mostrarCombinaciones, width=15)  # Crea un botón para mostrar las combinaciones
mostrarCombinaciones.grid(row=2, column=4, padx=(2, 10), pady=20, sticky="ew")  # Coloca el botón en la ventana

inicio()  # Llama a la función para deshabilitar ciertos elementos al inicio

ventana.mainloop()  # Ejecuta el bucle principal de la interfaz gráfica
