from sys import maxsize
from urllib.parse import quote_plus
# Supongamos que tienes definidas estas enumeraciones para AliExpress (puedes adaptarlas o reutilizar las de Amazon si tienen sentido)
from src.models.AliExpressModels import CATEGORY, LANGUAGE, CONDITION


class AliExpressURLSearch:
    """
    Clase encargada de construir URLs de búsqueda de AliExpress con distintos parámetros y filtros.
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
            min_price: int = 0,
            max_price: int = maxsize,
            free_shipping: bool = False,
            condicion: CONDITION = None
    ) -> str:
        """
        Construye la URL de búsqueda para AliExpress aplicando los filtros especificados.

        :param busqueda: Término de búsqueda principal (keywords).
        :param categoria: Categoría de AliExpress, representada en la enumeración `CATEGORY`.
        :param idioma: Idioma a utilizar en la búsqueda, definido en la enumeración `LANGUAGE`.
        :param marca: Marca del producto (por ejemplo "samsung").
        :param descuento: Porcentaje de descuento mínimo (p. ej. 50 = 50%).
        :param pagina: Página de resultados a mostrar (paginación).
        :param min_price: Precio mínimo del rango de búsqueda.
        :param max_price: Precio máximo del rango de búsqueda.
        :param free_shipping: Indica si se debe filtrar por envío gratis.
        :param condicion: Condición del producto (`CONDITION.New`, `CONDITION.Used`, etc.).
        :return: Una cadena que representa la URL final de búsqueda en AliExpress.
        """
        # Validación de los límites de precios
        cls._validar_precios(min_price, max_price)

        # Construcción de los parámetros base
        params = [
            f"SearchText={quote_plus(busqueda)}",       # Término de búsqueda
            f"CatId={categoria}" if categoria else "",    # Categoría (si se especifica)
            f"language={idioma}" if idioma else "",       # Idioma (si se especifica)
            f"page={pagina}" if pagina > 1 else "",         # Paginación (solo si la página es mayor a 1)
            cls._construir_filtros(
                min_price,
                max_price,
                free_shipping,
                descuento,
                condicion,
                marca
            )
        ]

        # Se unen los parámetros no vacíos con '&'
        return "https://www.aliexpress.com/wholesale?" + "&".join(filter(None, params))

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
        Construye la sección de filtros para la búsqueda en AliExpress.
        Incluye filtros de rango de precio, envío gratis, descuento, condición y marca.

        :param min_price: Precio mínimo.
        :param max_price: Precio máximo.
        :param free_shipping: Indica si se debe filtrar por envío gratis.
        :param descuento: Porcentaje de descuento mínimo.
        :param condicion: Condición del producto.
        :param marca: Marca del producto.
        :return: Cadena con los parámetros de filtro en formato 'clave=valor'
                 concatenados con '&', o una cadena vacía si no hay filtros.
        """
        filtros = []

        # Filtro de precios: Usamos parámetros minPrice y maxPrice.
        if min_price or max_price != maxsize:
            filtros.append(f"minPrice={min_price}")
            if max_price != maxsize:
                filtros.append(f"maxPrice={max_price}")

        # Filtro de envío gratis
        if free_shipping:
            filtros.append("freeShipping=true")

        # Filtro de descuento
        if descuento > 0:
            filtros.append(f"minDiscount={descuento}")

        # Filtro de condición
        if condicion:
            filtros.append(f"condition={condicion.value}")

        # Filtro de marca
        if marca:
            filtros.append(f"brand={quote_plus(marca)}")

        # Se unen los filtros con '&'
        return "&".join(filtros) if filtros else ""


if __name__ == "__main__":
    # Ejemplo de uso: Construir la URL para la búsqueda de "monitor",
    # en la categoría Electronics, con idioma English, y marca "samsung".
    print(
        AliExpressURLSearch.build_url(
            busqueda="monitor",
            categoria=CATEGORY.Electronics,
            idioma=LANGUAGE.English,
            marca="samsung"
        )
    )
