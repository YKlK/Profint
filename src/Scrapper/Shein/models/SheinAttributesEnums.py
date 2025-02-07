from enum import Enum

class SheinAttrValues(Enum):
    """
    Enumeración con una amplia variedad de posibles valores de atributos (attr_values)
    para filtrar búsquedas en SHEIN.

    Estos valores representan características de los productos, como talla, estilo,
    detalles de diseño, siluetas, colores, materiales y ocasiones, entre otros.
    """

    # --- Tallas ---
    TALLA_XXS = "XXS"
    TALLA_XS = "XS"
    TALLA_S = "S"
    TALLA_M = "M"
    TALLA_L = "L"
    TALLA_XL = "XL"
    TALLA_XXL = "XXL"

    # --- Ajustes y cortes ---
    AJUSTE_SLIM = "Slim Fit"
    AJUSTE_REGULAR = "Regular Fit"
    AJUSTE_LOOSE = "Loose Fit"
    AJUSTE_OVERSIZE = "Oversize"
    CORTE_CROP = "Crop"
    CORTE_ASIMÉTRICO = "Corte asimétrico"

    # --- Estilos ---
    ESTILO_CASUAL = "Casual"
    ESTILO_ELEGANTE = "Elegante"
    ESTILO_BOHO = "Bohemio"
    ESTILO_DEPORTIVO = "Deportivo"
    ESTILO_URBANO = "Urbano"
    ESTILO_MINIMALISTA = "Minimalista"
    ESTILO_FESTIVO = "Festivo"
    ESTILO_VINTAGE = "Vintage"
    ESTILO_MODERNO = "Moderno"
    ESTILO_ROMANTICO = "Romántico"

    # --- Mangas ---
    MANGA_CORTA = "manga corta"
    MANGA_MEDIA = "manga media"
    MANGA_LARGA = "manga larga"
    MANGA_3_4 = "manga 3/4"
    SIN_MANGAS = "sin mangas"
    MANGA_BOMBAY = "manga tipo bombín"

    # --- Escotes ---
    ESCOTE_V = "escote en V"
    ESCOTE_REDONDO = "escote redondo"
    ESCOTE_SIRENA = "escote sirena"
    ESCOTE_CUADRADO = "escote cuadrado"
    ESCOTE_ASIMÉTRICO = "escote asimétrico"
    ESCOTE_ENTRECIERRE = "escote de entrepierna"  # Ejemplo, si aplica a ciertos estilos

    # --- Detalles de diseño ---
    BOTON = "Botón"
    SIN_BOTON = "Sin Botón"
    ESTAMPADO = "Estampado"
    LISO = "Liso"
    RAYADO = "Rayado"
    CON_LACITOS = "Con lacitos"
    CON_CINTURON = "Con cinturón"
    PLISADO = "Plisado"
    CON_VOLANTES = "Con volantes"
    BORDADO = "Bordado"
    CON_ENCAJE = "Con encaje"
    CON_TRANSPARENCIA = "Con transparencia"
    CON_LENTEJUELAS = "Con lentejuelas"
    CON_DETALLES_METÁLICOS = "Con detalles metálicos"
    CON_APLICACIONES = "Con aplicaciones"
    CON_AJUSTE_ELÁSTICO = "Con ajuste elástico"
    CON_CORTE_ASIMÉTRICO = "Con corte asimétrico"

    # --- Cortes y siluetas ---
    SILUETA_A_LINEA = "Silueta A-line"
    SILUETA_RECTA = "Silueta recta"
    SILUETA_EMPERADOR = "Silueta emperador"
    PIERNA_ANCHA = "Pierna ancha"
    PIERNA_ESTÁNDAR = "Pierna estándar"
    PIERNA_ESTRUCTURADA = "Pierna estructurada"

    # --- Colores ---
    COLOR_NEGRO = "Negro"
    COLOR_BLANCO = "Blanco"
    COLOR_ROJO = "Rojo"
    COLOR_AZUL = "Azul"
    COLOR_VERDE = "Verde"
    COLOR_AMARILLO = "Amarillo"
    COLOR_GRIS = "Gris"
    COLOR_MARRÓN = "Marrón"
    COLOR_ROSA = "Rosa"
    COLOR_VIOLETA = "Violeta"
    COLOR_NARANJA = "Naranja"
    COLOR_BEIGE = "Beige"
    COLOR_TURQUESA = "Turquesa"
    COLOR_MULTICOLOR = "Multicolor"

    # --- Materiales ---
    MATERIAL_ALGODÓN = "Algodón"
    MATERIAL_POLIÉSTER = "Poliéster"
    MATERIAL_LINO = "Lino"
    MATERIAL_SEDA = "Seda"
    MATERIAL_DENIM = "Denim"
    MATERIAL_CUERO = "Cuero"
    MATERIAL_SIMIL_CUERO = "Símil cuero"
    MATERIAL_SATÉN = "Satén"
    MATERIAL_VELVET = "Velvet"  # Terciopelo
    MATERIAL_FRENCH_TWILL = "French twill"

    # --- Ocasiones ---
    OCASION_COTIDIANA = "Cotidiana"
    OCASION_FIESTA = "Fiesta"
    OCASION_TRABAJO = "Trabajo"
    OCASION_EVENTO = "Evento"
    OCASION_DEPORTIVA = "Deportiva"
    OCASION_FORMAL = "Formal"
    OCASION_INFORMAL = "Informal"

    # --- Estampados adicionales ---
    ESTAMPADO_FLORAL = "Estampado floral"
    ESTAMPADO_ANIMAL = "Estampado animal"
    ESTAMPADO_GEOMÉTRICO = "Estampado geométrico"
    ESTAMPADO_ABSTRACTO = "Estampado abstracto"


