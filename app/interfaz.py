from tkinter import *
from tkinter import ttk, filedialog, messagebox, PhotoImage
from simulacion import iniciar_simulacion  # Importamos la función de simulación desde simulacion.py
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Instanciamiento Tkinter
raiz = Tk()
raiz.title("Smart Drone")
raiz.resizable(0, 0)  # Bloquear el redimensionamiento de la ventana
icono = PhotoImage(file=os.path.join(BASE_DIR, "assets", "imagenes", "dron.png"))
raiz.iconphoto(True, icono)

# Variables globales
archivo_cargado = None
mundo = None
tipo_busqueda = StringVar(value="")
algoritmo_seleccionado = StringVar(value="...")
nombre_archivo = StringVar()

# Opciones de los algoritmos
opciones_no_informada = ["Amplitud", "Costo uniforme", "Profundidad"]
opciones_informada = ["Avara", "A*"]

# Función para cargar el archivo TXT
def cargar_archivo():
    global archivo_cargado, mundo
    archivo_cargado = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
    
    if archivo_cargado:
        nombre_archivo.set(archivo_cargado.split('/')[-1])
        messagebox.showinfo("Archivo Cargado", "El archivo ha sido cargado con éxito.")
    
        mundo = []
        with open(archivo_cargado, "r") as archivo:
            for linea in archivo:
                mundo.append(list(map(int, linea.strip().split())))

# Función para borrar el archivo seleccionado
def borrar_archivo():
    global archivo_cargado, mundo
    archivo_cargado = None
    mundo = None
    nombre_archivo.set("")
    tipo_busqueda.set("")
    algoritmo_seleccionado.set("...")
    combo_algoritmo["values"] = ["..."]
    combo_algoritmo.current(0)

    boton_informada.config(relief=RAISED)
    boton_no_informada.config(relief=RAISED)
    
    # Limpiar el contenido del reporte
    text_reporte.config(state="normal")
    text_reporte.delete("1.0", END)
    text_reporte.config(state="disabled")

    messagebox.showinfo("Archivo Borrado", "El archivo ha sido eliminado de la selección.")

# Función para cambiar el estado de los botones de búsqueda
def seleccionar_busqueda(tipo):
    tipo_busqueda.set(tipo)
    boton_informada.config(relief=SUNKEN if tipo == "Informada" else RAISED)
    boton_no_informada.config(relief=SUNKEN if tipo == "No informada" else RAISED)
    combo_algoritmo["values"] = opciones_informada if tipo == "Informada" else opciones_no_informada
    combo_algoritmo.set("...")

# Función para iniciar la simulación
def iniciar():
    if not archivo_cargado or mundo is None:
        messagebox.showerror("Error", "Debe cargar un archivo antes de iniciar la simulación.")
        return
    if not tipo_busqueda.get():
        messagebox.showerror("Error", "Debe seleccionar un tipo de búsqueda antes de iniciar la simulación.")
        return
    if algoritmo_seleccionado.get() == "...":
        messagebox.showerror("Error", "Debe seleccionar un algoritmo antes de iniciar la simulación.")
        return
    
    # Llamada a la simulación, que retorna las métricas (esta llamada se bloqueará hasta cerrar la ventana Pygame)
    metricas = iniciar_simulacion(mundo, algoritmo_seleccionado.get())
    
    # Prepara el reporte
    reporte = "Nodos expandidos: {}\nProfundidad del árbol: {}\nTiempo de cómputo: {:.4f} segundos\n".format(
        metricas['nodos_expandidos'], metricas['profundidad_arbol'], metricas['tiempo_computo'])
    
    if algoritmo_seleccionado.get() in ["Costo uniforme", "A*"]:
        reporte += "Costo del la solución: {}\n".format(metricas['costo_solucion'])
        
    # Actualiza el reporte en la interfaz
    text_reporte.config(state="normal")
    text_reporte.delete("1.0", END)
    text_reporte.insert("1.0", reporte)
    text_reporte.config(state="disabled")

# Contenedor para cargar el archivo
contenedor1 = LabelFrame(raiz, text="Datos del entorno", bd=3)
contenedor1.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="we")

boton_cargar = Button(contenedor1, text="Cargar mundo", command=cargar_archivo, width=20)
boton_cargar.grid(row=0, column=0, padx=5, pady=5)

label_archivo = Label(contenedor1, textvariable=nombre_archivo, width=20, anchor="c")
label_archivo.grid(row=0, column=1, padx=5, pady=5)

# Contenedor para seleccionar tipo de búsqueda y algoritmo
contenedor2 = LabelFrame(raiz, text="Tipo de búsqueda", bd=3)
contenedor2.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="we")

boton_informada = Button(contenedor2, text="Informada", width=20, command=lambda: seleccionar_busqueda("Informada"))
boton_informada.grid(row=0, column=0, padx=5, pady=5)

boton_no_informada = Button(contenedor2, text="No Informada", width=20, command=lambda: seleccionar_busqueda("No informada"))
boton_no_informada.grid(row=0, column=1, padx=5, pady=5)

# Etiqueta para el ComboBox
label_algoritmo = Label(contenedor2, text="Escoger algoritmo:")
label_algoritmo.grid(row=1, column=0, padx=5, pady=5, sticky="")

# Combobox de algoritmos
combo_algoritmo = ttk.Combobox(contenedor2, state="readonly", width=21, textvariable=algoritmo_seleccionado)
combo_algoritmo["values"] = ["..."]  # Opción inicial
combo_algoritmo.grid(row=1, column=1, padx=5, pady=5)
combo_algoritmo.current(0)

# Contenedor de botones finales
contenedor3 = LabelFrame(raiz, bd=3)
contenedor3.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="we")

boton_iniciar = Button(contenedor3, text="Iniciar", width=20, command=iniciar)
boton_iniciar.grid(row=0, column=0, padx=5, pady=5)

boton_borrar = Button(contenedor3, text="Limpiar", command=borrar_archivo, width=20)
boton_borrar.grid(row=0, column=1, padx=5, pady=5)

boton_salir = Button(contenedor3, text="Salir", width=43, command=raiz.destroy)
boton_salir.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

# Contenedor del Reporte
contenedor4 = LabelFrame(raiz, text="Reporte", bd=3)
contenedor4.grid(row=0, column=2, rowspan=3, padx=5, pady=5, sticky="ns")

text_reporte = Text(contenedor4, height=13, width=35, wrap="word", state="disabled")
text_reporte.pack(padx=5, pady=5, fill="both", expand=False)

# Iniciar la interfaz gráfica
raiz.mainloop()