import requests
import logging
import sys
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
from src.config.Headers import headers
from src.Scrapper.Amazon.URL_Builder import AmazonURLSearch
from src.Scrapper.Amazon.models.AmazonModelsEnums import CATEGORY, LANGUAGE, CONDITION


class RangoPaginasInvalido(Exception):
    """Excepción personalizada para manejar errores en el rango de páginas."""
    pass


class AmazonScraper:
    # Se reutiliza una sesión para aprovechar la persistencia de conexiones
    session = requests.Session()

    @classmethod
    def obtener_productos_de_pagina(cls, busqueda: str, categoria: CATEGORY, idioma: LANGUAGE,
                                    marca: str, descuento: int, min_price: int, max_price: int,
                                    free_shipping: bool, condicion: CONDITION, page: int) -> dict:
        """
        Obtiene los productos de una sola página.
        Retorna un diccionario con la lista de productos y el total de productos encontrados.
        """
        try:
            url = AmazonURLSearch.build_url(
                busqueda=busqueda,
                categoria=categoria,
                idioma=idioma,
                marca=marca,
                descuento=descuento,
                pagina=page,
                min_price=min_price,
                max_price=max_price,
                free_shipping=free_shipping,
                condicion=condicion
            )
            logging.info(f"Revisando la página {page}: {url}")
            response = cls.session.get(url, headers=headers())
            if response.status_code != 200:
                logging.warning(f"⚠️ No se pudo obtener la página {page}, código {response.status_code}")
                return {"productos": [], "total": 0}

            soup = BeautifulSoup(response.text, "html.parser")
            # Combinar las clases de los enlaces de productos en un único selector CSS
            clases = ["s-line-clamp-4", "s-line-clamp-2", "s-line-clamp-6"]
            selector = ", ".join([f"a.a-link-normal.{clase}.s-link-style.a-text-normal" for clase in clases])
            productos = soup.select(selector)
            logging.info(f"✅ Se encontraron {len(productos)} productos en la página {page}")

            productos_encontrados = []
            for producto in productos:
                nombre = producto.get_text(strip=True) or "Nombre no disponible"
                enlace = producto.get("href", "")
                if enlace and not enlace.startswith("http"):
                    enlace = "https://www.amazon.com" + enlace
                productos_encontrados.append({"nombre": nombre, "url": enlace})

            return {"productos": productos_encontrados, "total": len(productos_encontrados)}
        except Exception as e:
            logging.error(f"❌ Error en la página {page}: {e}")
            return {"productos": [], "total": 0}

    @classmethod
    def obtener_productos_rango(cls, busqueda: str, categoria: CATEGORY = None, idioma: LANGUAGE = None,
                                marca: str = None, descuento: int = 0, min_price: int = 100,
                                max_price: int = sys.maxsize, free_shipping: bool = False,
                                condicion: CONDITION = None, start_page: int = 1, end_page: int = 3) -> list[dict[str, str]]:
        """
        Busca productos en Amazon en un rango de páginas de forma concurrente y devuelve una lista
        con su nombre y URL.
        """
        if end_page < start_page:
            raise RangoPaginasInvalido(
                f"⚠ Error: `end_page` ({end_page}) no puede ser menor que `start_page` ({start_page})."
            )

        productos_encontrados = []
        total_productos_revisados = 0

        # Usar ThreadPoolExecutor para obtener cada página en un hilo distinto
        num_paginas = end_page - start_page + 1
        with ThreadPoolExecutor(max_workers=num_paginas) as executor:
            futures = {
                executor.submit(
                    cls.obtener_productos_de_pagina,
                    busqueda,
                    categoria,
                    idioma,
                    marca,
                    descuento,
                    min_price,
                    max_price,
                    free_shipping,
                    condicion,
                    page
                ): page
                for page in range(start_page, end_page + 1)
            }
            for future in as_completed(futures):
                page = futures[future]
                result = future.result()
                productos_encontrados.extend(result["productos"])
                total_productos_revisados += result["total"]

        logging.info(f"🔍 Total de productos revisados en todas las páginas: {total_productos_revisados}")
        return productos_encontrados

    @classmethod
    def obtener_especificaciones_producto(cls, productos: list[dict[str, str]]) -> list[dict[str, str]]:
        """
        Obtiene las especificaciones de una lista de productos en Amazon de forma concurrente.
        Extrae detalles como precio, descripción, detalles técnicos, estrellas, ratings, comentarios
        y descuento.
        """
        productos_detallados = []
        total_productos = len(productos)
        productos_procesados = 0
        productos_fallidos = 0

        def obtener_detalles(producto: dict[str, str]) -> dict[str, str] | None:
            try:
                response = cls.session.get(producto["url"], headers=headers())
                if response.status_code != 200:
                    logging.warning(
                        f"⚠️ No se pudo obtener el producto {producto['nombre']}, código {response.status_code}"
                    )
                    return None

                soup = BeautifulSoup(response.text, "html.parser")

                # Extraer la parte entera y la parte decimal del precio
                precio_whole = soup.find("span", class_="a-price-whole")
                precio_fraction = soup.find("span", class_="a-price-fraction")
                if precio_whole:
                    precio_text = precio_whole.get_text(strip=True)
                    if precio_fraction:
                        precio_text = f"{precio_text}{precio_fraction.get_text(strip=True)}"
                else:
                    precio_text = "No disponible"

                # Extraer otros datos básicos
                descripcion = soup.find("div", id="productDescription")
                detalles_tecnicos = soup.find("table", id="productDetails_techSpec_section_1")
                estrellas = soup.find("span", class_="a-icon-alt")
                ratings = soup.find("span", id="acrCustomerReviewText")

                # Extraer comentarios
                comentarios_tags = soup.select(
                    "div.a-expander-content.reviewText.review-text-content.a-expander-partial-collapse-content"
                )
                comentarios = [tag.get_text(strip=True) for tag in comentarios_tags]

                # Extraer el porcentaje de descuento utilizando un selector CSS
                descuento_tag = soup.select_one(
                    "span.a-size-large.a-color-price.savingPriceOverride.aok-align-center.reinventPriceSavingsPercentageMargin.savingsPercentage"
                )
                descuento_text = descuento_tag.get_text(strip=True) if descuento_tag else "No disponible"

                return {
                    "nombre": producto["nombre"],
                    "url": producto["url"],
                    "precio": precio_text,
                    "descripcion": descripcion.get_text(strip=True) if descripcion else "No disponible",
                    "detalles_tecnicos": detalles_tecnicos.get_text(strip=True) if detalles_tecnicos else "No disponible",
                    "estrellas": estrellas.get_text(strip=True) if estrellas else "No disponible",
                    "ratings": ratings.get_text(strip=True) if ratings else "No disponible",
                    "comentarios": comentarios if comentarios else "No disponibles",
                    "descuento": descuento_text
                }
            except Exception as e:
                logging.error(f"❌ Error al obtener detalles del producto {producto['nombre']}: {e}")
                return None

        # Usar ThreadPoolExecutor para obtener detalles de los productos en paralelo
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {executor.submit(obtener_detalles, producto): producto for producto in productos}
            for future in as_completed(futures):
                detalles = future.result()
                if detalles:
                    productos_detallados.append(detalles)
                    productos_procesados += 1
                    logging.info(f"✅ Procesado: {detalles['nombre']} (Total procesados: {productos_procesados}/{total_productos})")
                else:
                    productos_fallidos += 1

        logging.info(f"🔎 Resumen: {productos_procesados} productos procesados exitosamente, {productos_fallidos} fallos de {total_productos} revisados.")
        return productos_detallados


# ✅ Ejemplo de Uso
if __name__ == "__main__":
    try:
        # Primero, obtenemos los productos de las páginas concurrentemente
        productos = AmazonScraper.obtener_productos_rango(
            busqueda="monitor",
            categoria=CATEGORY.Computers,
            idioma=LANGUAGE.English,
            marca="acer",
            start_page=1,
            end_page=10
        )

        # Luego, obtenemos los detalles de cada producto también de forma concurrente
        productos_detallados = AmazonScraper.obtener_especificaciones_producto(productos)

        if productos_detallados:
            print("\n🔹 Productos encontrados con detalles:")
            for producto in productos_detallados:
                print(f"- {producto['nombre']} → {producto['url']}")
                print(f"  💲 Precio: {producto['precio']}")
                print(f"  📉 Descuento: {producto['descuento']}")
                print(f"  ⭐ Estrellas: {producto['estrellas']} ({producto['ratings']})")
                print(f"  📄 Descripción: {producto['descripcion'][:100]}...")
                print(f"  🔧 Detalles Técnicos: {producto['detalles_tecnicos'][:100]}...")
                print(f"  💬 Comentarios: {producto['comentarios']}\n")
        else:
            print("⚠️ No se encontraron especificaciones.")

    except RangoPaginasInvalido as e:
        logging.error(f"❌ {e}")
