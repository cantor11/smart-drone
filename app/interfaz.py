from tkinter import *
from tkinter import ttk, filedialog, messagebox, PhotoImage
from simulacion import iniciar_simulacion  # Importamos la función de simulación desde simulacion.py
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COLOR_FONDO = "#303030"
COLOR_BOTON = "#606060"  # Color negro para botones
COLOR_TEXTO = "#FFFFFF"  # Color blanco para el texto de los botones

# Instanciamiento Tkinter
raiz = Tk()
raiz.title("Smart Drone")
raiz.resizable(False, False)  # Bloquear el redimensionamiento de la ventana
raiz.configure(bg=COLOR_FONDO) # Color de fondo
icono = PhotoImage(file=os.path.join(BASE_DIR, "assets", "imagenes", "dron.png"))
raiz.iconphoto(True, icono)
style = ttk.Style()
style.theme_use("vista")

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
    
    iniciar_simulacion(mundo)

# Contenedor para cargar el archivo
contenedor1 = LabelFrame(raiz, text="Datos del entorno", bd=3, bg=COLOR_FONDO, fg=COLOR_TEXTO)
contenedor1.grid(row=0, column=0, columnspan=2, padx=8, pady=8, sticky="we")

boton_cargar = Button(contenedor1, text="Cargar mundo", command=cargar_archivo, width=20, bg=COLOR_BOTON, fg=COLOR_TEXTO)
boton_cargar.grid(row=0, column=0, padx=5, pady=5)

label_archivo = Label(contenedor1, textvariable=nombre_archivo, width=20, anchor="c", bg=COLOR_FONDO, fg=COLOR_TEXTO)
label_archivo.grid(row=0, column=1, padx=5, pady=5)

# Contenedor para seleccionar tipo de búsqueda y algoritmo
contenedor2 = LabelFrame(raiz, text="Tipo de búsqueda", bd=3, bg=COLOR_FONDO, fg=COLOR_TEXTO)
contenedor2.grid(row=1, column=0, columnspan=2, padx=8, pady=8, sticky="we")

boton_informada = Button(contenedor2, text="Informada", width=20, command=lambda: seleccionar_busqueda("Informada"), bg=COLOR_BOTON, fg=COLOR_TEXTO)
boton_informada.grid(row=0, column=0, padx=5, pady=5)

boton_no_informada = Button(contenedor2, text="No Informada", width=20, command=lambda: seleccionar_busqueda("No informada"), bg=COLOR_BOTON, fg=COLOR_TEXTO)
boton_no_informada.grid(row=0, column=1, padx=5, pady=5)

# Etiqueta para el ComboBox
label_algoritmo = Label(contenedor2, text="Escoger algoritmo:", bg=COLOR_FONDO, fg=COLOR_TEXTO)
label_algoritmo.grid(row=1, column=0, padx=5, pady=5, sticky="")

# Combobox de algoritmos
combo_algoritmo = ttk.Combobox(contenedor2, state="readonly", width=21, textvariable=algoritmo_seleccionado)
combo_algoritmo["values"] = ["..."]  # Opción inicial
combo_algoritmo.grid(row=1, column=1, padx=5, pady=5)
combo_algoritmo.current(0)

# Contenedor de botones finales
contenedor3 = LabelFrame(raiz, bd=3, bg=COLOR_FONDO, fg=COLOR_TEXTO)
contenedor3.grid(row=2, column=0, columnspan=2, padx=8, pady=8, sticky="we")

boton_iniciar = Button(contenedor3, text="Iniciar", width=20, command=iniciar, bg=COLOR_BOTON, fg=COLOR_TEXTO)
boton_iniciar.grid(row=0, column=0, padx=5, pady=5)

boton_borrar = Button(contenedor3, text="Limpiar", command=borrar_archivo, width=20, bg=COLOR_BOTON, fg=COLOR_TEXTO)
boton_borrar.grid(row=0, column=1, padx=5, pady=5)

boton_salir = Button(contenedor3, text="Salir", width=43, command=raiz.destroy, bg=COLOR_BOTON, fg=COLOR_TEXTO)
boton_salir.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

# Contenedor del Reporte
contenedor4 = LabelFrame(raiz, text="Reporte", bd=3, bg=COLOR_FONDO, fg=COLOR_TEXTO)
contenedor4.grid(row=0, column=2, rowspan=3, padx=8, pady=8, sticky="ns")

text_reporte = Text(contenedor4, height=14, width=35, wrap="word", state="disabled", bg=COLOR_FONDO, fg=COLOR_TEXTO)
text_reporte.pack(padx=5, pady=5, fill="both", expand=False)

# Iniciar la interfaz gráfica
raiz.mainloop()