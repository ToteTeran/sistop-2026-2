import struct

CLUSTER_SIZE = 2048
DIRECTORIO_OFFSET = CLUSTER_SIZE
ENTRADA_SIZE = 64

print("=== Archivos disponibles ===\n")

archivos = []

with open("fiunamfs.img", "rb") as disco:
    for i in range(256):
        offset = DIRECTORIO_OFFSET + (i * ENTRADA_SIZE)
        disco.seek(offset)
        entrada = disco.read(ENTRADA_SIZE)
        tipo = chr(entrada[0])
        if tipo == "-":
            nombre = entrada[1:16].decode("ascii").replace('\x00', ' ').strip()
            tamaño = struct.unpack("<I", entrada[16:20])[0]
            cluster_inicial = struct.unpack("<I", entrada[20:24])[0]
            archivos.append({
                "nombre": nombre,
                "tamaño": tamaño,
                "cluster": cluster_inicial
            })
            print(f"- {nombre} ({tamaño} bytes)")

print()

archivo_buscado = input("¿Qué archivo quieres copiar?: ")
encontrado = False

with open("fiunamfs.img", "rb") as disco:
    for archivo in archivos:
        if archivo["nombre"] == archivo_buscado:
            encontrado = True
            inicio = archivo["cluster"] * CLUSTER_SIZE
            disco.seek(inicio)
            datos = disco.read(archivo["tamaño"])
            with open(archivo["nombre"], "wb") as salida:
                salida.write(datos)
            print("\nArchivo copiado correctamente")
            break
    if not encontrado:
        print("\nEse archivo no existe")