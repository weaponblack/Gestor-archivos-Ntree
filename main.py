import os
import traceback
from tkinter import filedialog, messagebox

from Model.FileInfo import *
from Model.NaryTree import NaryTree
import tkinter as tk

tree = NaryTree()


# Recupera las carpetas del directorio dado, crea objetos tipo fileInfo y los guarda en una lista
def list_files(startpath):
    file_objects = []
    file_id = 0

    for root, dirs, files in os.walk(startpath):
        folder_name = os.path.basename(root)
        file_name = folder_name
        level = root.count(os.sep)
        file_path = os.path.join(root)
        file_path = os.path.dirname(file_path)
        file = FileInfo(file_name, file_id, file_path, level)
        file_objects.append(file)
        file_id += 1
        level_files = []  # Almacenar archivos en el mismo nivel
        for f in files:
            item_path = os.path.join(root, f)
            item_path = os.path.dirname(item_path)

            file = FileInfo(f, file_id, item_path, level + 1)
            level_files.append(file)

        # Asignar ID incremental a los archivos en el mismo nivel
        for level_file in level_files:
            level_file.id = file_id
            file_objects.append(level_file)
            file_id += 1

        file_objects = Ordenar(file_objects)

    return file_objects


# Ordena la lista para que las ID queden en orden segun el nivel de carpeta
def Ordenar(list_objects):
    list_objects = sorted(list_objects, key=lambda x: x.level)
    for i in range(len(list_objects)):
        list_objects[i].id = i
    return list_objects

#Inserta la lista dada en ordenar en el arbol, creando Nodos con data como un objeto tipo FileInfo
def insert_in_Tree(files):
    parent = None
    tree.add_node(files[0])
    for i in range(1, len(files)):
        file = files[i]
        ultima_palabra = file.path.split("\\")[-1]
        for j in files:
            if ultima_palabra == j.name:
                parent = j
        tree.add_node(file, parent)


# ---------------------------------------------------------------------------------#
# ---------------------------------Printer-----------------------------------------#
def dibujar_carpeta(canvas, x, y, name):
    # Dibuja la parte principal de la carpeta
    canvas.create_rectangle(x - 10, y - 10, x + 10, y + 10, fill="yellow", outline="black")

    # Dibuja el ícono de la carpeta
    canvas.create_rectangle(x - 8, y - 6, x - 2, y + 2, fill="blue", outline="black")
    canvas.create_line(x - 8, y + 2, x - 2, y + 2, fill="black", width=2)

    # Dibuja el texto en la carpeta
    canvas.create_text(x, y + 14, text=name, fill="black", font=("Arial", 8), anchor=tk.CENTER)


def dibujar_arbol(arbol, canvas, x, y, separacion):
    # Dibujar el nodo actual como una carpeta
    dibujar_carpeta(canvas, x, y, arbol.data.name)

    # Dibujar el texto con los datos del nodo

    # Calcula las coordenadas de los hijos
    num_hijos = len(arbol.children)
    if num_hijos > 0:
        dx = separacion * (num_hijos - 1) // 2
        hijo_x = x - dx
        hijo_y = y + 100

        # Dibuja las conexiones con los hijos
        for hijo in arbol.children:
            canvas.create_line(x, y + 10, hijo_x, hijo_y - 10)
            dibujar_arbol(hijo, canvas, hijo_x, hijo_y, separacion)
            hijo_x += separacion


# Funcion Renombrar
def renombrar_archivo():
    archivo = filedialog.askopenfilename(title="Seleccionar archivo")
    if archivo:
        ventana_renombrar = tk.Toplevel()
        ventana_renombrar.title("Renombrar archivo")

        etiqueta = tk.Label(ventana_renombrar, text="Ingrese el nuevo nombre:")
        etiqueta.pack()

        entrada_nombre = tk.Entry(ventana_renombrar)
        entrada_nombre.pack()

        def confirmar_renombrar():
            nuevo_nombre = entrada_nombre.get().strip()
            if nuevo_nombre:
                try:
                    import os
                    nuevo_nombre_completo = os.path.join(os.path.dirname(archivo), nuevo_nombre)
                    os.rename(archivo, nuevo_nombre_completo)
                    messagebox.showinfo("Éxito", "Archivo renombrado con éxito.")
                    ventana_renombrar.destroy()
                except Exception as e:
                    messagebox.showerror("Error", f"Error al renombrar el archivo: {str(e)}")
            else:
                messagebox.showwarning("Advertencia", "Nombre de archivo inválido.")

        boton_confirmar = tk.Button(ventana_renombrar, text="Confirmar", command=confirmar_renombrar)
        boton_confirmar.pack()

#Funcion Eliminar
def eliminar_archivo():
    ruta = filedialog.askdirectory(title="Seleccionar archivo o carpeta")
    if ruta:
        confirmacion = messagebox.askquestion("Eliminar", "¿Estás seguro/a de que quieres eliminar el archivo o carpeta?")
        if confirmacion == "yes":
            try:
                if os.path.isfile(ruta):
                    os.remove(ruta)
                else:
                    os.rmdir(ruta)
                messagebox.showinfo("Éxito", "Archivo o carpeta eliminado/a con éxito.")
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar el archivo o carpeta: {str(e)}")

#Funcion Crear
def crear_archivo():
    nombre_archivo = filedialog.asksaveasfilename(title="Guardar archivo", defaultextension=".txt")
    if nombre_archivo:
        try:
            with open(nombre_archivo, 'w'):
                pass
            messagebox.showinfo("Éxito", "Archivo creado con éxito.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear el archivo: {str(e)}")


# Función para buscar el nodo
def buscar_nodo(entrada1):
    nombre_archivo = entrada1.get().strip()
    if nombre_archivo:
        # Aquí debes agregar tu lógica para buscar el nodo correspondiente al nombre del archivo ingresado
        # y obtener los datos del nodo encontrado
        datos_nodo = tree.find_node(nombre_archivo)
        datos_nodo = datos_nodo.data
        datos_nodo_list = []
        datos_nodo_list.append(datos_nodo.name)
        datos_nodo_list.append(datos_nodo.id)
        datos_nodo_list.append(datos_nodo.path)
        datos_nodo_list.append(datos_nodo.level)

        if datos_nodo:
            mostrar_datos_nodo(datos_nodo_list)
        else:
            messagebox.showwarning("Advertencia", "No se encontró ningún nodo con ese nombre de archivo.")
    else:
        messagebox.showwarning("Advertencia", "Nombre de archivo inválido.")


# Función para mostrar los datos del nodo en una ventana adicional
def mostrar_datos_nodo(datos_nodo):
    ventana_nodo = tk.Toplevel()
    ventana_nodo.title("Datos del nodo")

    # Etiqueta para el nombre del archivo
    etiqueta_nombre = tk.Label(ventana_nodo, text=f"Nombre: {datos_nodo[0]}")
    etiqueta_nombre.pack()
    # Etiqueta para el nombre del archivo
    etiqueta_nombre = tk.Label(ventana_nodo, text=f"ID: {datos_nodo[1]}")
    etiqueta_nombre.pack()
    # Etiqueta para el nombre del archivo
    etiqueta_nombre = tk.Label(ventana_nodo, text=f"Ruta: {datos_nodo[2]}")
    etiqueta_nombre.pack()
    # Etiqueta para el nombre del archivo
    etiqueta_nombre = tk.Label(ventana_nodo, text=f"Level: {datos_nodo[3]}")
    etiqueta_nombre.pack()

def crear_botones():
    zona_botones = tk.Frame(ventana)
    zona_botones.pack(side=tk.BOTTOM)

    boton_renombrar = tk.Button(ventana, text="Renombrar archivo", command=renombrar_archivo)
    boton_renombrar.pack()

    boton_reload = tk.Button(zona_botones, text="reload", command=actualizar_ventana)
    boton_reload.pack(side=tk.LEFT, padx=10)

    boton_eliminar = tk.Button(zona_botones, text="Eliminar archivo", command=eliminar_archivo)
    boton_eliminar.pack(side=tk.LEFT, padx=10)

    boton_crear = tk.Button(zona_botones, text="Crear archivo", command=crear_archivo)
    boton_crear.pack(side=tk.LEFT, padx=10)

    # Crear la zona de entrada de texto y botones
    zona_entrada = tk.Frame(ventana)
    zona_entrada.pack(side=tk.BOTTOM)

    # Agregar las entradas de texto
    entrada1 = tk.Entry(zona_entrada)
    entrada1.pack(side=tk.LEFT, padx=10)

    # Agregar el botón de Aceptar
    boton_entrada1 = tk.Button(zona_entrada, text="Buscar", command=lambda: buscar_nodo(entrada1))
    boton_entrada1.pack(side=tk.LEFT, padx=10)

# Reload
def actualizar_ventana():
    try:
        # Eliminar todos los elementos de la ventana
        for widget in ventana.winfo_children():
            widget.destroy()

        # Dibujar nuevamente el árbol y los botones
        canvas = tk.Canvas(ventana, width=1200, height=600)
        canvas.pack()
        files = list_files(startpath)
        insert_in_Tree(files)
        dibujar_arbol(tree.root, canvas, 700, 50, 200)
        crear_botones()

    except Exception as e:
        traceback.print_exc()


startpath = "C:\Root"
files = list_files(startpath)
insert_in_Tree(files)

# Crear ventana y lienzo
ventana = tk.Tk()
canvas = tk.Canvas(ventana, width=1200, height=600)
canvas.pack()

# Dibujar árbol
dibujar_arbol(tree.root, canvas, 700, 50, 200)
crear_botones()

# Ejecutar interfaz gráfica
ventana.mainloop()
# ---------------------------------------------------------------------------------#
