from urllib.parse import quote_plus
from src.Scrapper.Shein.models.SheinAttributesEnums import SheinAttrValues
from src.Scrapper.Shein.models.SheinCategoryIdEnums import SheinChildCatID


class SheinURLSearch:
    """
    Clase para construir URLs de búsqueda en SHEIN utilizando únicamente
    los siguientes parámetros básicos:
      - busqueda: Término de búsqueda.
      - attr_values: Lista de atributos (opcional).
      - child_cat_id: ID de la subcategoría.
      - page: Número de página.
      - min_price y max_price: Filtros de precio.

    La URL generada tendrá la siguiente estructura (con el mismo orden de parámetros):

      https://es.shein.com/pdsearch/<busqueda>/?ici=s1`EditSearch`<busqueda>`_fb`d0`PageSearchNoResult&
      search_source=1&search_type=all&source=search&
      src_identifier=st%3D2`sc%3D<busqueda>`sr%3D0`ps%3D1&
      src_identifier_pre_search=null&
      src_module=search&
      src_tab_page_id=page_search1738876362318&
      child_cat_id=<child_cat_id>&page=<page>&min_price=<min_price>&max_price=<max_price>
    """

    @classmethod
    def build_url(
        cls,
        busqueda: str,
        attr_values: list = None,
        child_cat_id: int = None,
        page: int = 1,
        min_price: int = None,
        max_price: int = None,
        src_tab_page_id: str = None
    ) -> str:
        # URL base: el término de búsqueda se incorpora en la ruta
        base_url = f"https://es.shein.com/pdsearch/{quote_plus(busqueda)}/"

        # Lista de parámetros, en el orden requerido:
        params = []

        # 1. ici (usando "PageSearchNoResult")
        params.append(f"ici=s1`EditSearch`{quote_plus(busqueda)}`_fb`d0`PageSearchNoResult")

        # 2. search_source
        params.append("search_source=1")

        # 3. search_type
        params.append("search_type=all")

        # 4. source
        params.append("source=search")

        # 5. src_identifier
        params.append(f"src_identifier=st%3D2`sc%3D{quote_plus(busqueda)}`sr%3D0`ps%3D1")

        # 6. src_identifier_pre_search
        params.append("src_identifier_pre_search=null")

        # 7. src_module
        params.append("src_module=search")

        # 8. src_tab_page_id (valor por defecto si no se pasa)
        if not src_tab_page_id:
            src_tab_page_id = "page_search1738876362318"
        params.append(f"src_tab_page_id={src_tab_page_id}")

        # 9. Si se proporcionan, se agrega attr_values (por ejemplo, "L" o "1001")
        if attr_values:
            joined_attrs = "-".join(str(attr) for attr in attr_values)
            params.append(f"attr_values={quote_plus(joined_attrs)}")

        # 10. child_cat_id (obligatorio para especificar la subcategoría)
        if child_cat_id is not None:
            params.append(f"child_cat_id={child_cat_id}")

        # 11. Página
        params.append(f"page={page}")

        # 12. Filtros de precio
        if min_price is not None:
            params.append(f"min_price={min_price}")
        if max_price is not None:
            params.append(f"max_price={max_price}")

        # Se unen los parámetros con "&"
        query_string = "&".join(params)
        return base_url + "?" + query_string


if __name__ == "__main__":
    # Ejemplo de uso:
    # Búsqueda "camisa" sin atributos (o con atributos opcionales),
    # usando la subcategoría CAMISAS_FEMENINAS, página 1, con precio mínimo 0 y máximo 64.
    url = SheinURLSearch.build_url(
        busqueda="pantalon",
        attr_values=[SheinAttrValues.COLOR_VERDE.value],  # O bien [] si no se desea pasar atributo
        child_cat_id=SheinChildCatID.PANTALONES_EXTRA_GRANDE_FEMENINOS.value,
        page=1,
        min_price=14,
        max_price=64
    )
    print(url)


#https://es.shein.com/pdsearch/pantalon/?ici=s1`EditSearch`pantalon`_fb`d0`PageSearchNoResult&search_source=1&search_type=all&source=search&src_identifier=st=2`sc=pantalon`sr=0`ps=1&src_identifier_pre_search=null&src_module=search&src_tab_page_id=page_search1738876362318&attr_values=Verde&child_cat_id=1893&page=1&min_price=14&max_price=64
#9:00PM