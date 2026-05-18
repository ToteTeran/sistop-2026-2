import struct
import os

class FiUnamFS:

    def __init__(self, ruta):
        self.ruta = ruta

    def listar_archivos(self):
        archivos = []

        with open(self.ruta, "rb") as disco:
            for i in range(256):
                offset = DIRECTORIO_OFFSET + (i * ENTRADA_SIZE)
                disco.seek(offset)
                entrada = disco.read(ENTRADA_SIZE)
                tipo = chr(entrada[0])
                if tipo == "-":
                    nombre = entrada[1:16].decode(
                        "ascii"
                    ).replace('\x00', '').strip()
                    tamaño = struct.unpack(
                        "<I",
                        entrada[16:20]
                    )[0]
                    cluster_inicial = struct.unpack(
                        "<I",
                        entrada[20:24]
                    )[0]
                    archivos.append({
                        "nombre": nombre,
                        "tamaño": tamaño,
                        "cluster": cluster_inicial,
                        "offset": offset
                    })

        return archivos

    def mostrar_archivos(self):
        archivos = self.listar_archivos()

        print("\n=== Archivos disponibles ===\n")

        for archivo in archivos:
            print(
                f"- {archivo['nombre']} "
                f"({archivo['tamaño']} bytes)"
            )

    def copiar_desde_fs(self):
        self.mostrar_archivos()

        nombre_archivo = input(
            "\nArchivo a copiar: "
        )

        archivos = self.listar_archivos()

        with open(self.ruta, "rb") as disco:
            for archivo in archivos:
                if archivo["nombre"] == nombre_archivo:
                    inicio = archivo["cluster"] * CLUSTER_SIZE
                    disco.seek(inicio)
                    datos = disco.read(archivo["tamaño"])
                    with open(nombre_archivo, "wb") as salida:
                        salida.write(datos)
                    print("\nArchivo copiado correctamente")
                    return

        print("\nArchivo no encontrado")
        cola_logs.put(
            f"Archivo copiado desde FiUnamFS: {nombre_archivo}"
        )


    def eliminar_archivo(self):
        self.mostrar_archivos()

        nombre_archivo = input(
            "\nArchivo a eliminar: "
        )

        archivos = self.listar_archivos()

        with open(self.ruta, "r+b") as disco:
            for archivo in archivos:
                if archivo["nombre"] == nombre_archivo:
                    disco.seek(archivo["offset"])
                    disco.write(b'/')
                    print("\nArchivo eliminado correctamente")
                    return

        print("\nArchivo no encontrado")
        cola_logs.put(
            f"Archivo eliminado: {nombre_archivo}"
        )