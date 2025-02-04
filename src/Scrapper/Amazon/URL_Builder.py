from sys import maxsize
from urllib.parse import quote_plus
from src.Scrapper.Amazon.models.AmazonModelsEnums import CATEGORY, LANGUAGE, CONDITION


class AmazonURLSearch:
    """
    Clase encargada de construir URLs de búsqueda de Amazon con distintos parámetros y filtros.
    Utiliza los valores definidos en las enumeraciones `CATEGORY`, `LANGUAGE` y `CONDITION`
    para representar la categoría, el idioma y la condición de los productos respectivamente.
    """

    @classmethod
    def build_url(
            cls,
            busqueda: str,
            categoria: CATEGORY = None,
            idioma: LANGUAGE = None,
            marca: str = None,
            descuento: int = 0,
            pagina: int = 1,
            min_price: int = 100,
            max_price: int = maxsize,
            free_shipping: bool = False,
            condicion: CONDITION = None
    ) -> str:
        """
        Construye la URL de búsqueda para Amazon aplicando los filtros especificados.

        :param busqueda: Término de búsqueda principal (keywords).
        :param categoria: Categoría de Amazon, representada en la enumeración `CATEGORY`.
        :param idioma: Idioma a utilizar en la búsqueda, definido en la enumeración `LANGUAGE`.
        :param marca: Marca del producto (por ejemplo "samsung").
        :param descuento: Porcentaje de descuento mínimo (p. ej. 50 = 50%).
        :param pagina: Página de resultados a mostrar (paginación).
        :param min_price: Precio mínimo del rango de búsqueda.
        :param max_price: Precio máximo del rango de búsqueda.
        :param free_shipping: Indica si se debe filtrar por envío gratis.
        :param condicion: Condición del producto (`CONDITION.New`, `CONDITION.Used`, etc.).
        :return: Una cadena que representa la URL final de búsqueda en Amazon.
        """
        # Validación de los límites de precios
        cls._validar_precios(min_price, max_price)

        # Construcción de los parámetros base
        params = [
            f"k={quote_plus(busqueda)}",   # Término de búsqueda
            f"i={categoria}",              # Categoría (si se especifica)
            f"language={idioma}",          # Idioma de la búsqueda (si se especifica)
            "__mk_es_US=ÅMÅŽÕÑ",           # Parámetro de Amazon para búsquedas en español
            f"page={pagina}" if pagina > 1 else "",  # Paginación (solo si la página es mayor a 1)
            cls._construir_filtros(
                min_price,
                max_price,
                free_shipping,
                descuento,
                condicion,
                marca
            )
        ]

        # Devuelve la URL concatenando los parámetros no vacíos con el carácter '&'
        return "https://www.amazon.com/s?" + "&".join(filter(None, params))

    @classmethod
    def _validar_precios(cls, min_price: int, max_price: int):
        """
        Valida que el precio mínimo no sea mayor que el precio máximo.
        Si la validación falla, se lanza un ValueError.

        :param min_price: Precio mínimo especificado.
        :param max_price: Precio máximo especificado.
        :raises ValueError: Si `min_price` es mayor que `max_price`.
        """
        if min_price > max_price:
            raise ValueError("ERROR: El precio mínimo no puede ser mayor al máximo")

    @classmethod
    def _construir_filtros(
            cls,
            min_price: int,
            max_price: int,
            free_shipping: bool,
            descuento: int,
            condicion: CONDITION,
            marca: str
    ) -> str:
        """
        Construye la sección de filtros para la búsqueda en Amazon (parámetro 'rh' en la URL).
        Incluye filtros de rango de precio, envío gratis, descuento, condición y marca.

        :param min_price: Precio mínimo.
        :param max_price: Precio máximo.
        :param free_shipping: Indica si el filtro de "envío gratis" está activo.
        :param descuento: Porcentaje de descuento a aplicar.
        :param condicion: Condición del producto.
        :param marca: Marca del producto.
        :return: Cadena con el formato 'rh=...' que contiene los filtros,
                 o una cadena vacía si no hay filtros.
        """
        filtros = []

        # Filtro de precios
        if min_price or max_price != maxsize:
            # p_36 se usa para rango de precios: p_36:minPrice-maxPrice
            filtros.append(f"p_36:{min_price}-{max_price}")

        # Filtro de envío gratis
        if free_shipping:
            filtros.append("p_n_is_free_shipping:10236242011")

        # Filtro de descuento
        if descuento > 0:
            filtros.append(f"p_n_pct-off-with-tax:{descuento}-")

        # Filtro de condición (nuevo, usado, etc.)
        if condicion:
            filtros.append(f"p_n_condition-type:{condicion.value}")

        # Filtro de marca
        if marca:
            filtros.append(f"p_89:{quote_plus(marca)}")

        # Si existen filtros, se concatenan con '%2C' (la codificación del carácter coma en URLs)
        return f"rh={'%2C'.join(filtros)}" if filtros else ""


if __name__ == "__main__":
    # Ejemplo de uso: Se construye la URL para la búsqueda de "monitor", en la categoría "Electronics",
    # con marca "samsung" y rango de precios default (100 - maxsize).
    print(
        AmazonURLSearch.build_url(
            busqueda="monitor",
            categoria=CATEGORY.Electronics,
            marca="samsung"
        )
    )
