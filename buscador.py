import os
import tkinter as tk
from tkinter import filedialog, scrolledtext
from tkinterdnd2 import DND_FILES, TkinterDnD
from datetime import datetime
import json

# Obtén la ruta al directorio del script
directorio_script = os.path.dirname(os.path.realpath(__file__))

# Función para cargar la configuración desde un archivo JSON
def cargar_configuracion(nombre_archivo):
    try:
        ruta_completa = os.path.join(directorio_script, nombre_archivo)
        with open(ruta_completa, 'r') as archivo:
            datos = json.load(archivo)
            return datos['extraer']
    except FileNotFoundError:
        print(f"Archivo de configuración no encontrado: {ruta_completa}")
        return [[".mil.uy", "ejercito"], [".edu.uy", "educa"], [".gub.uy", "gobierno"], [".org.uy", "uruguay"], [".com.uy", "uruguay"], [".net.uy", "uruguay"], ["montevideo.com.uy", "montevideo"]]

# Intenta cargar la configuración desde el archivo 'config.json'
extraer = cargar_configuracion('config.json')

def actualizar_lista():
    lista_box.delete(0, tk.END)
    for item in extraer:
        lista_box.insert(tk.END, item)

def agregar_elemento():
    clave = entrada_clave.get()
    categoria = entrada_categoria.get()
    if clave and categoria:
        extraer.append([clave, categoria])
        actualizar_lista()
        guardar_configuracion(extraer, 'config.json')

def eliminar_elemento():
    seleccionado = lista_box.curselection()
    if seleccionado:
        extraer.pop(seleccionado[0])
        actualizar_lista()
        guardar_configuracion(extraer, 'config.json')

def modificar_elemento():
    seleccionado = lista_box.curselection()
    if seleccionado:
        clave = entrada_clave.get()
        categoria = entrada_categoria.get()
        if clave and categoria:
            extraer[seleccionado[0]] = [clave, categoria]
            actualizar_lista()
            guardar_configuracion(extraer, 'config.json')

def guardar_configuracion(datos, nombre_archivo):
    ruta_completa = os.path.join(directorio_script, nombre_archivo)
    with open(ruta_completa, 'w') as archivo:
        json.dump({"extraer": datos}, archivo, indent=4)

# Creación de la interfaz gráfica
root = TkinterDnD.Tk()
root.title("Extractor de Líneas")

frame_modificar = tk.Frame(root)
frame_modificar.pack(pady=10)

entrada_clave = tk.Entry(frame_modificar)
entrada_clave.grid(row=0, column=1, padx=5)
entrada_categoria = tk.Entry(frame_modificar)
entrada_categoria.grid(row=1, column=1, padx=5)
tk.Label(frame_modificar, text="Clave:").grid(row=0, column=0)
tk.Label(frame_modificar, text="Categoría:").grid(row=1, column=0)

boton_agregar = tk.Button(frame_modificar, text="Agregar", command=agregar_elemento)
boton_agregar.grid(row=2, column=0)
boton_eliminar = tk.Button(frame_modificar, text="Eliminar", command=eliminar_elemento)
boton_eliminar.grid(row=2, column=1)
boton_modificar = tk.Button(frame_modificar, text="Modificar", command=modificar_elemento)
boton_modificar.grid(row=2, column=2)

lista_box = tk.Listbox(root)
lista_box.pack(pady=10)
actualizar_lista()

mensaje_box = scrolledtext.ScrolledText(root, state=tk.DISABLED, height=10)
mensaje_box.pack(pady=10)

# Nueva funcionalidad para contar líneas y mostrar un resumen
def procesar_archivos(archivos):
    agregar_mensaje("Iniciando procesamiento de archivos...")
    fecha_actual = datetime.now().strftime("%d%m%Y")
    lineas_por_categoria = {categoria: set() for _, categoria in extraer}
    total_lineas_procesadas = 0  # Contador de líneas procesadas

    for archivo in archivos:
        agregar_mensaje(f"Procesando archivo: {archivo}")
        archivo_procesado = False
        for encoding in ['utf-8', 'cp1252', 'latin1', 'ISO-8859-1', 'utf-16']:
            try:
                with open(archivo, 'r', encoding=encoding) as file:
                    for linea in file:
                        # Aquí iría el resto de tu lógica de procesamiento de archivo
                        pass
            except UnicodeDecodeError:
                print(f"Error de codificación con {encoding}, intentando con otra...")
            except Exception as e:
                print(f"No se pudo procesar el archivo {archivo} con la codificación {encoding}: {e}")

def agregar_mensaje(mensaje):
    mensaje_box.config(state=tk.NORMAL)  # Habilitar la caja de texto para editar
    mensaje_box.insert(tk.END, mensaje + "\n")
    mensaje_box.see(tk.END)
    mensaje_box.config(state=tk.DISABLED)  # Deshabilitar la caja de texto para evitar edición

def procesar_archivos(archivos):
    agregar_mensaje("Iniciando procesamiento de archivos...")
    fecha_actual = datetime.now().strftime("%d%m%Y")
    lineas_por_categoria = {categoria: set() for _, categoria in extraer}
    total_lineas_procesadas = 0  # Contador de líneas procesadas

    for archivo in archivos:
        agregar_mensaje(f"Procesando archivo: {archivo}")
        archivo_procesado = False
        for encoding in ['utf-8', 'cp1252', 'latin1', 'ISO-8859-1', 'utf-16']:
            try:
                with open(archivo, 'r', encoding=encoding) as file:
                    for linea in file:
                        total_lineas_procesadas += 1
                        if '@' in linea or ':' in linea:
                            for clave, categoria in extraer:
                                if clave in linea:
                                    lineas_por_categoria[categoria].add(linea)
                                    agregar_mensaje(f"Encontrada coincidencia: '{clave}' en archivo {archivo}")
                        else:
                            continue
                    archivo_procesado = True
                    break
            except UnicodeDecodeError:
                agregar_mensaje(f"Error de codificación con {encoding}, intentando con otra...")
                continue
            except Exception as e:
                agregar_mensaje(f"No se pudo procesar el archivo {archivo} con la codificación {encoding}: {e}")
                break

        if not archivo_procesado:
            agregar_mensaje(f"No se pudo procesar el archivo {archivo} con ninguna de las codificaciones probadas.")

    for categoria, lineas in lineas_por_categoria.items():
        if lineas:
            archivo_salida = f"{categoria}{fecha_actual}.txt"
            with open(archivo_salida, 'w', encoding='utf-8') as file:
                for linea in sorted(lineas):
                    file.write(linea)
            agregar_mensaje(f"Archivo '{archivo_salida}' creado con {len(lineas)} líneas.")
        else:
            agregar_mensaje(f"No se encontraron coincidencias para la categoría '{categoria}'.")

    agregar_mensaje(f"Procesamiento completo. Total de líneas revisadas: {total_lineas_procesadas}")

def seleccionar_archivos():
    archivos = filedialog.askopenfilenames()
    if archivos:
        agregar_mensaje(f"Archivos seleccionados: {archivos}")
        return archivos
    return []

def iniciar_proceso():
    archivos = seleccionar_archivos()
    if archivos:
        procesar_archivos(archivos)

def drop(event):
    archivos = root.tk.splitlist(event.data)
    if archivos:
        agregar_mensaje(f"Archivos arrastrados: {archivos}")
        procesar_archivos(archivos)

boton_seleccionar = tk.Button(root, text="Seleccionar Archivos", command=iniciar_proceso)
boton_seleccionar.pack(pady=10)

root.drop_target_register(DND_FILES)
root.dnd_bind('<<Drop>>', drop)

root.geometry("500x400")
root.mainloop()