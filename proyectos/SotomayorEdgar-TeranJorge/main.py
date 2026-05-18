import struct

CLUSTER_SIZE = 2048
DIRECTORIO_OFFSET = CLUSTER_SIZE
ENTRADA_SIZE = 64

with open("fiunamfs.img", "rb") as disco:
    for i in range(256):
        offset = DIRECTORIO_OFFSET + (i * ENTRADA_SIZE)
        disco.seek(offset)
        entrada = disco.read(ENTRADA_SIZE)
        tipo = chr(entrada[0])
        
        if tipo == "-":
            nombre = entrada[1:16].decode("ascii").strip()
            tamaño = struct.unpack("<I", entrada[16:20])[0]
            cluster_inicial = struct.unpack("<I", entrada[20:24])[0]
            
            print("---")
            print("Archivo:", nombre)
            print("Tamaño:", tamaño, "bytes")
            print("Cluster inicial:", cluster_inicial)