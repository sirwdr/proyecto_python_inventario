import sqlite3
from colorama import init, Fore, Style

init(autoreset=True)

# Conectar a la base de datos (o crearla si no existe)
conn = sqlite3.connect('inventario.db')
cursor = conn.cursor()

# Crear la tabla de productos
cursor.execute('''
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    descripcion TEXT,
    cantidad INTEGER NOT NULL,
    precio REAL NOT NULL,
    categoria TEXT
)
''')

# Guardar los cambios y cerrar la conexión
conn.commit()
conn.close()



def menu_principal():
    print(Fore.GREEN + "Gestión de Inventario")
    print(Fore.YELLOW + "1. Registrar producto")
    print(Fore.YELLOW + "2. Actualizar producto")
    print(Fore.YELLOW + "3. Eliminar producto")
    print(Fore.YELLOW + "4. Mostrar productos")
    print(Fore.YELLOW + "5. Buscar producto")
    print(Fore.YELLOW + "6. Generar reporte de bajo stock")
    print(Fore.RED + "7. Salir")

def registrar_producto():
    nombre = input("Nombre del producto: ")
    descripcion = input("Descripción del producto: ")
    cantidad = int(input("Cantidad disponible: "))
    precio = float(input("Precio del producto: "))
    categoria = input("Categoría del producto: ")

    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria)
    VALUES (?, ?, ?, ?, ?)
    ''', (nombre, descripcion, cantidad, precio, categoria))
    conn.commit()
    conn.close()
    print(Fore.GREEN + "Producto registrado exitosamente.")

def actualizar_producto():
    id_producto = int(input("ID del producto a actualizar: "))
    nueva_cantidad = int(input("Nueva cantidad disponible: "))

    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE productos
    SET cantidad = ?
    WHERE id = ?
    ''', (nueva_cantidad, id_producto))
    conn.commit()
    conn.close()
    print(Fore.GREEN + "Producto actualizado exitosamente.")

def eliminar_producto():
    id_producto = int(input("ID del producto a eliminar: "))

    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()
    cursor.execute('''
    DELETE FROM productos
    WHERE id = ?
    ''', (id_producto,))
    conn.commit()
    conn.close()
    print(Fore.GREEN + "Producto eliminado exitosamente.")

def mostrar_productos():
    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM productos')
    productos = cursor.fetchall()
    conn.close()

    for producto in productos:
        print(f"ID: {producto[0]}, Nombre: {producto[1]}, Descripción: {producto[2]}, Cantidad: {producto[3]}, Precio: {producto[4]}, Categoría: {producto[5]}")

def buscar_producto():
    id_producto = int(input("ID del producto a buscar: "))

    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM productos WHERE id = ?', (id_producto,))
    producto = cursor.fetchone()
    conn.close()

    if producto:
        print(f"ID: {producto[0]}, Nombre: {producto[1]}, Descripción: {producto[2]}, Cantidad: {producto[3]}, Precio: {producto[4]}, Categoría: {producto[5]}")
    else:
        print(Fore.RED + "Producto no encontrado.")

def reporte_bajo_stock():
    limite = int(input("Ingrese el límite de stock: "))

    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM productos WHERE cantidad <= ?', (limite,))
    productos = cursor.fetchall()
    conn.close()

    print(Fore.RED + "Reporte de productos con bajo stock:")
    for producto in productos:
        print(f"ID: {producto[0]}, Nombre: {producto[1]}, Descripción: {producto[2]}, Cantidad: {producto[3]}, Precio: {producto[4]}, Categoría: {producto[5]}")

if __name__ == "__main__":
    while True:
        menu_principal()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_producto()
        elif opcion == "2":
            actualizar_producto()
        elif opcion == "3":
            eliminar_producto()
        elif opcion == "4":
            mostrar_productos()
        elif opcion == "5":
            buscar_producto()
        elif opcion == "6":
            reporte_bajo_stock()
        elif opcion == "7":
            print(Fore.GREEN + "Saliendo del programa...")
            break
        else:
            print(Fore.RED + "Opción no válida. Intente nuevamente.")
