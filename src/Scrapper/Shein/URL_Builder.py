from urllib.parse import quote_plus
from src.Scrapper.Shein.models.SheinAttributesEnums import SheinAttrValues
from src.Scrapper.Shein.models.SheinCategoryIdEnums import SheinChildCatID


class SheinURLSearch:
    """
    Clase para construir URLs de búsqueda en SHEIN utilizando únicamente
    los siguientes parámetros básicos:
      - busqueda: Término de búsqueda.
      - attr_values: Lista de atributos (opcional). Se usarán para generar filtros avanzados.
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
      [parámetros de filtros avanzados]&
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
        # URL base: se incorpora el término de búsqueda en la ruta.
        base_url = f"https://es.shein.com/pdsearch/{quote_plus(busqueda)}/"

        # Lista de parámetros, en el orden requerido.
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

        # 9. Filtros avanzados a partir de attr_values:
        # Se invoca get_combined_filters y se agregan los parámetros correspondientes.
        if attr_values:
            combined_filters = SheinAttrValues.get_combined_filters(attr_values)
            if combined_filters.get("attr_ids"):
                params.append(f"attr_ids={quote_plus(combined_filters['attr_ids'])}")
            if combined_filters.get("selectAttributeGroup"):
                params.append(f"selectAttributeGroup={quote_plus(combined_filters['selectAttributeGroup'])}")
            if combined_filters.get("exc_attr_id") is not None:
                params.append(f"exc_attr_id={combined_filters['exc_attr_id']}")
            if combined_filters.get("attr_node_ids"):
                params.append(f"attr_node_ids={quote_plus(combined_filters['attr_node_ids'])}")

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

        # Se unen los parámetros con "&" y se devuelve la URL completa.
        query_string = "&".join(params)
        return base_url + "?" + query_string


if __name__ == "__main__":
    # Ejemplo de uso:
    # Al pasar SheinAttrValues.COLOR_VERDE, get_combined_filters devolverá:
    # {'attr_ids': '27_81-27_334-27_2436-27_2566', 'selectAttributeGroup': '27_3', 'exc_attr_id': 27, 'attr_node_ids': '27_3'}
    # y estos se incluirán en la URL.
    url = SheinURLSearch.build_url(
        busqueda="pantalon",
        attr_values=[SheinAttrValues.COLOR_ROJO,SheinAttrValues.ESTILO_ELEGANTE],  # Se pasan los atributos avanzados.
        child_cat_id=SheinChildCatID.PANTALONES_EXTRA_GRANDE_FEMENINOS.value,
        page=1,
        min_price=14,
        max_price=64
    )
    print(url)
