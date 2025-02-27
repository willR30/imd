import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import requests
import threading
import time

# Diccionario con los códigos HTTP y sus significados
http_errors = {
    400: "Bad Request: La solicitud no pudo ser entendida por el servidor.",
    401: "Unauthorized: No está autorizado a acceder al recurso.",
    403: "Forbidden: El servidor entiende la solicitud, pero se niega a autorizarla.",
    404: "Not Found: El recurso solicitado no se encuentra en el servidor.",
    500: "Internal Server Error: El servidor encontró un error al intentar procesar la solicitud.",
    502: "Bad Gateway: El servidor actuó como una puerta de enlace y recibió una respuesta no válida del servidor de origen.",
    503: "Service Unavailable: El servidor no está disponible temporalmente.",
    504: "Gateway Timeout: El servidor actuó como una puerta de enlace y no recibió una respuesta a tiempo."
}

# Función para verificar las URLs
def verificar_urls_desde_archivo(archivo, table):
    def worker():
        try:
            with open(archivo, 'r') as file:
                urls = file.readlines()  # Leer todas las líneas del archivo
            
            # Limpiar la tabla antes de mostrar los resultados
            for row in table.get_children():
                table.delete(row)

            # Mostrar mensaje "Verificando URLs"
            status_label.config(text="Verificando URLs...")

            # Recorrer las URLs y verificar su estado
            for url in urls:
                url = url.strip()  # Eliminar saltos de línea y espacios
                if url:
                    try:
                        respuesta = requests.get(url)
                        if respuesta.status_code == 200:
                            estado = "Activa"
                        elif respuesta.status_code == 404:
                            estado = f"Caída (Código: 404 - No encontrado)"
                        else:
                            estado = f"Error HTTP (Código: {respuesta.status_code})"
                            estado += f" - {http_errors.get(respuesta.status_code, 'Descripción no disponible')}"
                    except requests.exceptions.RequestException as e:
                        estado = f"Caída - {str(e)}"
                    table.insert('', 'end', values=(url, estado))
                else:
                    table.insert('', 'end', values=("URL vacía", "Ignorada"))
                
                # Actualizar la UI después de cada URL
                time.sleep(0.5)
                root.update_idletasks()

            # Finalizar animación de carga
            progress_bar.stop()
            status_label.config(text="¡Verificación completada!")

        except FileNotFoundError:
            messagebox.showerror("Error", f"El archivo {archivo} no se encontró.")
            progress_bar.stop()
            status_label.config(text="Error al leer el archivo.")
        
    # Iniciar el hilo para evitar que la UI se congele
    threading.Thread(target=worker, daemon=True).start()

# Función para abrir el cuadro de diálogo de selección de archivo
def seleccionar_archivo():
    archivo = filedialog.askopenfilename(
        title="Seleccionar archivo de URLs",
        filetypes=[("Archivos de texto", "*.txt")]
    )
    if archivo:
        # Iniciar la animación de carga
        progress_bar.start()
        # Llamar a la función de verificación
        verificar_urls_desde_archivo(archivo, table)

# Crear la ventana principal
root = tk.Tk()
root.title("Verificador de URLs")

# Configurar el tamaño de la ventana
root.geometry("600x450")  # Tamaño fijo
root.resizable(False, False)  # Desactivar la redimensión
root.attributes('-topmost', True)  # Asegura que la ventana esté siempre encima

# Centrar la ventana en la pantalla
def centrar_ventana():
    ancho_ventana = 600
    alto_ventana = 450
    # Obtener las dimensiones de la pantalla
    ancho_pantalla = root.winfo_screenwidth()
    alto_pantalla = root.winfo_screenheight()
    # Calcular la posición de la ventana para centrarla
    x = (ancho_pantalla - ancho_ventana) // 2
    y = (alto_pantalla - alto_ventana) // 2
    # Mover la ventana a la posición calculada
    root.geometry(f'{ancho_ventana}x{alto_ventana}+{x}+{y}')

centrar_ventana()  # Llamar a la función para centrar la ventana

# Botón para seleccionar el archivo
boton_seleccionar = tk.Button(root, text="Seleccionar archivo de URLs", command=seleccionar_archivo)
boton_seleccionar.pack(pady=10)

# Animación de carga (barra de progreso)
progress_bar = ttk.Progressbar(root, mode='indeterminate')
progress_bar.pack(pady=20)

# Etiqueta para mostrar el estado de la verificación
status_label = tk.Label(root, text="", font=("Arial", 12))
status_label.pack(pady=10)

# Crear la tabla para mostrar las URLs y su estado
columns = ("URL", "Estado")
table = ttk.Treeview(root, columns=columns, show="headings")
table.heading("URL", text="URL")
table.heading("Estado", text="Estado")
table.pack(fill=tk.BOTH, expand=True)

# Ejecutar la aplicación
root.mainloop()
