import polib


# Este Script de Python sirve para "fusionar" los .po
# Mantiene la traduccion existente y añade las nuevas entradas sin reemplazar lo existente

# ==========================
# Variables
# Aqui debes poner la ruta de los archivos
# ==========================

# La ruta del archivo español actual
ruta_es = r"C:\Users\telec\Documents\MVZ2-Spanish-addon-main\addon\assets\mvz2\en-US\almanac.po"

# La ruta del archivo chino-ingles actualizado
ruta_en = r"C:\Users\telec\Downloads\almanac.po"

# La ruta donde se guardara el archivo resultante
ruta_salida = r"C:\Users\telec\Documents\MVZ2-Spanish-addon-main\resultado_almanac.po"

# ==========================


# Archivo español actual
es = polib.pofile(ruta_es)

# Archivo chino-ingles actualizado
en = polib.pofile(ruta_en)


# Guardar los textos en español existentes usando contexto + texto
es_ids = {
    (entry.msgctxt, entry.msgid)
    for entry in es
}


# Agregar solamente los textos nuevos usando el ingles
for entry in en:
    clave = (entry.msgctxt, entry.msgid)

    if clave not in es_ids:
        nueva_entrada = polib.POEntry(
            msgid=entry.msgid,
            msgstr=entry.msgstr,
            msgctxt=entry.msgctxt
        )

        # Mantener comentarios del archivo ingles para entradas nuevas
        nueva_entrada.comment = entry.comment
        nueva_entrada.tcomment = entry.tcomment

        es.append(nueva_entrada)

        es_ids.add(clave)


# Guardar archivo resultante
es.save(ruta_salida)

print(f"Archivo guardado en: {ruta_salida}")
