import polib


# Este Script de Python sirve para "fusionar" los .po
# Mantiene la traduccion existente y añade las nuevas entradas sin reemplazar lo existente

# ==========================
# Variables
# Aqui debes poner la ruta de los archivos
# ==========================

# La ruta del archivo español actual
ruta_es = r"C:\Users\telec\Downloads\MVZ2-Spanish-addon-main\MVZ2-Spanish-addon-main\addon\assets\mvz2\en-US\general.po"

# La ruta del archivo chino-ingles actualizado
ruta_en = r"C:\Users\telec\Downloads\MVZ2-Spanish-addon-main\MVZ2-Spanish-addon-main\generalingles.po"

# La ruta donde se guardara el archivo resultante
ruta_salida = r"C:\Users\telec\Downloads\MVZ2-Spanish-addon-main\MVZ2-Spanish-addon-main\scripts\general2v.po"

# ==========================


# Archivo español actual
es = polib.pofile(ruta_es)

# Archivo chino-ingles actualizado
en = polib.pofile(ruta_en)


# ==========================
# Crear indices del archivo español
# ==========================

# (comentario, contexto, texto chino)
indice_completo = {}

# (comentario, contexto)
indice_comentario = {}

# (contexto, texto chino)
indice_msgid = {}


for entry in es:

    comentario = entry.comment.strip()
    contexto = entry.msgctxt
    texto_chino = entry.msgid

    indice_completo[(comentario, contexto, texto_chino)] = entry

    if (comentario, contexto) not in indice_comentario:
        indice_comentario[(comentario, contexto)] = []

    indice_comentario[(comentario, contexto)].append(entry)

    indice_msgid[(contexto, texto_chino)] = entry


# ==========================
# Listas para clasificar
# ==========================

viejos = []
modificados = []
comentario_cambiado = []
nuevos = []


# ==========================
# Clasificar las entradas
# ==========================

for entry in en:

    comentario = entry.comment.strip()
    contexto = entry.msgctxt
    texto_chino = entry.msgid


    # Caso 1
    # Coincide comentario y texto chino
    if (comentario, contexto, texto_chino) in indice_completo:

        viejos.append(
            indice_completo[(comentario, contexto, texto_chino)]
        )

        continue


    # Caso 2
    # Coincide comentario pero no el texto chino

    if (comentario, contexto) in indice_comentario:

        posibles_viejos = indice_comentario[(comentario, contexto)]

        encontrado = False

        for viejo in posibles_viejos:

            # Si ambos tienen referencias, comparar referencias
            if viejo.occurrences and entry.occurrences:

                if viejo.occurrences == entry.occurrences:

                    modificados.append(
                        {
                            "nuevo": entry,
                            "viejo": viejo
                        }
                    )

                    encontrado = True
                    break


            # Si no tienen referencias, usar el comentario como antes
            else:

                if viejo.msgid != texto_chino:

                    modificados.append(
                        {
                            "nuevo": entry,
                            "viejo": viejo
                        }
                    )

                    encontrado = True
                    break


        # Si encontró el comentario pero ninguna coincidencia real
        # entonces es una entrada nueva
        if not encontrado:

            nuevos.append(entry)

        continue


    # Caso 2.5
    # No coincide comentario, pero si el texto chino
    if (contexto, texto_chino) in indice_msgid:

        comentario_cambiado.append(
            {
                "nuevo": entry,
                "viejo": indice_msgid[(contexto, texto_chino)]
            }
        )

        continue


    # Caso 3
    # No coincide comentario ni texto chino
    nuevos.append(entry)



# ==========================
# Mostrar resultado
# ==========================

print()
print("Resultado de la comparacion")
print("---------------------------")
print(f"Viejos               : {len(viejos)}")
print(f"Modificados          : {len(modificados)}")
print(f"Cambio comentario    : {len(comentario_cambiado)}")
print(f"Nuevos               : {len(nuevos)}")

# ==========================
# Crear archivo resultado
# ==========================

def escribir_entrada(archivo, entrada):
    archivo.write(str(entrada))
    archivo.write("\n")

# ==========================
# Mezclar traduccion usando el chino como referencia
# ==========================

def mezclar_traduccion(viejo, nuevo):

    chino_viejo = viejo.msgid.split("\n")
    espanol_viejo = viejo.msgstr.split("\n")

    chino_nuevo = nuevo.msgid.split("\n")
    ingles_nuevo = nuevo.msgstr.split("\n")

    resultado = []

    cantidad = max(len(chino_viejo), len(chino_nuevo))

    for i in range(cantidad):

        # Si existe la linea en ambos idiomas
        if i < len(chino_viejo) and i < len(chino_nuevo):

            if chino_viejo[i] == chino_nuevo[i]:

                # El chino no cambio, mantener español
                if i < len(espanol_viejo):
                    resultado.append(espanol_viejo[i])
                else:
                    resultado.append(ingles_nuevo[i])

            else:

                # El chino cambio, usar ingles nuevo
                if i < len(ingles_nuevo):
                    resultado.append(ingles_nuevo[i])


        # Si es una linea nueva
        elif i < len(ingles_nuevo):

            resultado.append(ingles_nuevo[i])


    entrada_final = polib.POEntry(
        msgid=nuevo.msgid,
        msgstr="\n".join(resultado),
        msgctxt=nuevo.msgctxt
    )

    entrada_final.comment = nuevo.comment
    entrada_final.tcomment = nuevo.tcomment
    entrada_final.occurrences = list(nuevo.occurrences)

    return entrada_final

with open(ruta_salida, "w", encoding="utf-8") as archivo:

    # ==========================
    # Metadatos
    # ==========================

    resultado = polib.POFile()
    resultado.metadata = es.metadata.copy()

    archivo.write(str(resultado))
    archivo.write("\n")


    # ==========================
    # Entradas viejas
    # ==========================

    archivo.write(
        "#==================\n"
        "# Traducciones existentes\n"
        "#==================\n\n"
    )

    for entry in viejos:
        escribir_entrada(archivo, entry)


    # ==========================
    # Modificados
    # ==========================

    archivo.write(
        "\n#==================\n"
        "# Modificados\n"
        "#==================\n\n"
    )

    for cambio in modificados:

        nuevo = cambio["nuevo"]
        viejo = cambio["viejo"]

        archivo.write("# Traduccion anterior:\n")

        for linea in viejo.msgstr.split("\n"):
            archivo.write("# " + linea + "\n")

        entrada_mezclada = mezclar_traduccion(viejo, nuevo)

        escribir_entrada(archivo, entrada_mezclada)


    # ==========================
    # Cambio de comentario
    # ==========================

    archivo.write(
        "\n#==================\n"
        "# Cambio de comentario\n"
        "#==================\n\n"
    )

    for cambio in comentario_cambiado:

        nuevo = cambio["nuevo"]

        escribir_entrada(archivo, nuevo)


    # ==========================
    # Nuevos
    # ==========================

    archivo.write(
        "\n#==================\n"
        "# Nuevos\n"
        "#==================\n\n"
    )

    for entry in nuevos:
        archivo.write("#nuevoR\n")
        escribir_entrada(archivo, entry)


print()
print(f"Archivo guardado en: {ruta_salida}")
