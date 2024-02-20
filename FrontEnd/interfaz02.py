import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox, font
from tkinter import ttk

# Variable global para almacenar la cadena cargada
cadena_actual = ""
datos_csv = None  # Variable global para almacenar los datos del archivo CSV

def inicio():
    editarCadena.config(state='disabled')
    mostrarCombinaciones.config(state='disabled')
    entradaCadena.config(state='disabled')

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
    
    cadenaTexto = tk.Label(ventanaEditar, text="     Cadena: ")
    cadenaTexto.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    global entradaCadenaTexto
    entradaCadenaTexto = tk.Text(ventanaEditar, width=80, height=10, wrap=tk.WORD)  # Ajustar el ancho y alto del widget entradaCadena
    entradaCadenaTexto.grid(row=0, column=1, columnspan=3, padx=5, pady=10, sticky="w")
    # Mostrar la cadena actual
    entradaCadenaTexto.insert(tk.END, cadena_actual)
    
    # Botón para guardar la cadena editada
    botonGuardar = tk.Button(ventanaEditar, text="Guardar", command=lambda: guardarCadena(ventanaEditar))
    botonGuardar.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky="w")
    # Enlazar la destrucción de la ventana de edición con la actualización de la cadena principal
    ventanaEditar.protocol("WM_DELETE_WINDOW", actualizarCadena)

def mostrarDatos():
    global datos_csv
    if datos_csv is not None:
        ventanaDatos = tk.Toplevel(ventana)
        ventanaDatos.title("Datos del archivo CSV")
        ventanaDatos.geometry("800x400")
        ventanaDatos.resizable(0, 0)
        
        tabla = ttk.Treeview(ventanaDatos)
        tabla["columns"] = tuple(datos_csv.columns)
        tabla.heading("#0", text="Índice")
        for col in datos_csv.columns:
            tabla.heading(col, text=col)
            tabla.column(col, anchor=tk.CENTER)
        
        for i, row in datos_csv.iterrows():
            tabla.insert("", tk.END, text=str(i), values=tuple(row))
        
        tabla.pack(expand=tk.YES, fill=tk.BOTH)
    else:
        messagebox.showwarning("Advertencia", "Primero carga un archivo CSV.")


# Crear la interfaz gráfica
ventana = tk.Tk()
ventana.title("Edición de cadenas de caracteres")
#ventana.iconbitmap(r"./02.ico")  # Comentado temporalmente
ventana.geometry("800x350")
ventana.resizable(0, 0)

# Etiqueta para el título
Titulo = tk.Label(ventana, text="EDICIÓN DE CADENAS DE CARÁCTERES")
Titulo.grid(row=0, column=0, columnspan=4, padx=10, pady=20, sticky="nsew")
fuente = font.Font(family="Gadugi", size=12)

cadena = tk.Label(ventana, text="     Cadena: ")
cadena.grid(row=1, column=0, padx=10, pady=10, sticky="w")
entradaCadena = tk.Text(ventana, width=80, height=10, wrap=tk.WORD)  # Ajustar el ancho y alto del widget entradaCadena
entradaCadena.grid(row=1, column=1, columnspan=3, padx=5, pady=10, sticky="w")

# Botón para cargar el archivo CSV
botonCargarArchivo = tk.Button(ventana, text="Cargar archivo", command=cargarArchivo)
botonCargarArchivo.grid(row=2, column=0, padx=10, pady=20, sticky="w")
editarCadena = tk.Button(ventana, text="Editar cadena", command=editarCadena)
editarCadena.grid(row=2, column=1, padx=10, pady=20, sticky="w")
mostrarCombinaciones = tk.Button(ventana, text="Mostrar combinaciones")
mostrarCombinaciones.grid(row=2, column=2, padx=10, pady=20, sticky="w")
botonMostrarDatos = tk.Button(ventana, text="Mostrar datos", command=mostrarDatos)
botonMostrarDatos.grid(row=2, column=3, padx=10, pady=20, sticky="w")

inicio()

ventana.mainloop()
