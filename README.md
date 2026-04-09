Language: [Spanish](README.md) | [简体中文](README-ZH.md) | **Español**

**Estado de traducción (8 de abril de 2026)**
**almanac.po:**
Total de entradas: 897
Traducidas: 896
Sin traducir (vacías): 1

**general.po:**
Total de entradas: 873
Traducidas: 873
Sin traducir (vacías): 0

**talk.po:**
Total de entradas: 2130
Traducidas: 2117
Sin traducir (vacías): 13
====================
[Cosas por corregir](Cosas-por-corregir.md)


**==Articulo de cómo crear un paquete de idioma para MVZ2==**
Este artículo explica cómo crear un paquete de idioma para MVZ2.

Dentro del cliente del juego MVZ2, puedes exportar paquetes de idioma integrados y estudiar sus estructuras de archivos.

Puedes descargar la carpeta `template` de este repositorio, la cual contiene las plantillas de texturas necesarias, plantillas de texto de traducción y traducciones al inglés como referencia.

# Archivo de Información
El archivo de información se encuentra en el directorio raíz del paquete de idioma y se llama `pack.json`.

 Su formato de contenido es típicamente:

```json
{
    "name": "Nombre del Paquete de Idioma",
    "author": "Nombre del Autor",
    "description": "Descripción del Paquete de Idioma",
    "dataVersion": 0
}
```

El campo `dataVersion` representa la versión de datos del paquete de idioma, utilizada para la validación de formato en diferentes versiones del juego.

**Un paquete de idioma debe incluir este archivo de información para ser reconocido por el juego. Los paquetes de idioma sin este archivo son inválidos.**

# Icono
El archivo de icono se encuentra en el directorio raíz del paquete de idioma y se llama `pack.png`.

Se recomienda una textura de forma cuadrada para el icono del paquete de idioma.

# Estructura de Archivos
Aparte de `pack.json` (archivo de información) y `pack.png` (icono), el contenido del paquete de idioma se almacena generalmente en la carpeta `assets`.

Las subcarpetas bajo `assets` corresponden a diferentes namespaces (espacios de nombres) en el juego. El contenido original (vanilla) utiliza el namespace `mvz2`.

Dentro de una carpeta de namespace, las subcarpetas representan diferentes idiomas. Por ejemplo:
- `zh-Hans`: Chino Simplificado
- `en-US`: Inglés (Estados Unidos)
- `es-ES`: Español (España)

Las carpetas de idioma contienen:
- `*.mo` (archivos de traducción compilados)
- `sprite_manifest.json` (catálogo de texturas)
- Carpeta `sprites` (texturas de una sola pieza)
- Carpeta `spritesheets` (texturas de múltiples piezas)

Una estructura típica de un paquete de idioma se ve así:

    pack.json
    pack.png
    assets/
        mvz2/
            zh-Hans/
                almanac.mo
                general.mo
                talk.mo
                sprite_manifest.json
                sprites/
                spritesheets/
            en-US/
                almanac.mo
                general.mo
                talk.mo
                sprite_manifest.json
                sprites/
                spritesheets/

# Traducción de Texto
Las traducciones de texto del juego utilizan el formato [GNU Gettext](https://www.gnu.org/software/gettext/), que incluye tres tipos de archivos:
* `*.pot`: Plantilla de traducción que contiene solo el texto original.
* `*.po`: Archivo de texto traducido para un idioma específico.
* `*.mo`: Versión binaria compilada del archivo `*.po`.

MVZ2 utiliza archivos `*.mo` para las traducciones. Para crear archivos `*.mo`, utiliza herramientas como [Poedit](https://poedit.net/).

Flujo de trabajo:
1. Crea un nuevo archivo `*.po` para las traducciones.
2. Carga las plantillas de traducción desde el `*.pot` al archivo `*.po`.
3. Traduce el texto.
4. Guarda y compila el archivo `*.po` en un `*.mo`.
5. Coloca los archivos `*.mo` compilados en `assets/<namespace>/<language>/`.

# Traducción de Texturas
El archivo `sprite_manifest.json` en `assets/<namespace>/<language>/` controla la carga de texturas. Solo se cargarán las texturas listadas aquí.

Formato de ejemplo:

```json
{
    "sprites": [
        {
            "name": "archive/castle_note",
            "texture": "archive/castle_note.png",
            "pivotX": 0.5,
            "pivotY": 0.5
        },
        ...
    ],
    "spritesheets": [
        {
            "name": "ready_set_build",
            "texture": "ready_set_build.png",
            "slices": [
                {
                    "x": 0.0,
                    "y": 148.0,
                    "width": 165.0,
                    "height": 74.0,
                    "pivotX": 0.5,
                    "pivotY": 0.5
                },
                ...
            ]
        },
        ...
    ]
}
```

### Estructura de Archivos:
- **sprites**: Texturas de una sola pieza (un archivo de imagen = una textura).
  - `name`: Nombre interno (debe coincidir con el nombre original del juego).
  - `texture`: Ruta relativa a la carpeta `sprites`.
  - `pivotX/Y`: Coordenadas del punto de anclaje (0=izquierda/abajo, 1=derecha/arriba).

- **spritesheets**: Texturas de múltiples piezas (un archivo de imagen dividido en varias texturas).
  - `slices`: Subdivisiones de la textura.
    - `x/y`: Coordenadas de inicio (píxeles, origen en la esquina inferior izquierda).
    - `width/height`: Dimensiones del recorte (píxeles).
    - `pivotX/Y`: Coordenadas del punto de anclaje.

Coloca los archivos `.png` correspondientes en las rutas especificadas después de configurar el archivo `sprite_manifest.json`.

# Añadir Nuevos Idiomas
Para añadir un nuevo idioma:
1. Crea una carpeta con el código del idioma (ej. `es-ES`) bajo `assets/<namespace>/`.
2. Añade el contenido traducido en esta carpeta.

El juego detecta automáticamente los nombres de idiomas estándar basados en los códigos de idioma. Para idiomas personalizados, añade una entrada de traducción con el contexto `"language_name"` en tu archivo `.po` para mostrar el nombre del idioma correctamente.

# Instalación
**Ruta en Windows**:  
`%HOMEPATH%\AppData\LocalLow\Cuerzor\MinecraftVSZombies2\language_packs`  
Coloca las carpetas de los paquetes de idioma o los archivos `.zip` comprimidos aquí.

También puedes gestionar los paquetes de idioma mediante las operaciones dentro del juego: Importar, Exportar y Eliminar.

