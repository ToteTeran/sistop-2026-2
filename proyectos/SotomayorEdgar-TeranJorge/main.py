with open("fiunamfs.img", "rb") as disco:
    disco.seek(5)
    nombre = disco.read(8).decode("ascii")

print(nombre)