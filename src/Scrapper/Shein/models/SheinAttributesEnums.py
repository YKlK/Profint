class SheinAttrValues:
    """
    Enumeración con una amplia variedad de posibles valores de atributos (colores, estilos, etc.)
    para filtrar búsquedas en SHEIN.
    """

    # --- Estilos ---
    ESTILO_BOHEMIO = "Bohemio"
    ESTILO_TRABAJO = "Trabajo"
    ESTILO_FIESTA = "Fiesta"
    ESTILO_DULCE = "Dulce"
    ESTILO_CASUAL = "Casual"
    ESTILO_SEXY = "Sexy"
    ESTILO_CALLE = "Calle"
    ESTILO_VINTAGE = "Vintage"
    ESTILO_ELEGANTE = "Elegante"

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
    COLOR_MORADO = "Morado"
    COLOR_CAQUI = "Caqui"
    COLOR_MULTICOLOR = "Multicolor"

    # Diccionario con los filtros avanzados para cada atributo
    ATTRIBUTE_FILTERS = {
        # --- Estilos ---
        "Bohemio": {"attr_ids": "101_725", "selectAttributeGroup": "101_725", "exc_attr_id": 101, "attr_node_ids": "101_725"},
        "Trabajo": {"attr_ids": "101_2490", "selectAttributeGroup": "101_2490", "exc_attr_id": 101, "attr_node_ids": "101_2490"},
        "Fiesta": {"attr_ids": "101_2491", "selectAttributeGroup": "101_2491", "exc_attr_id": 101, "attr_node_ids": "101_2491"},
        "Dulce": {"attr_ids": "101_231", "selectAttributeGroup": "101_231", "exc_attr_id": 101, "attr_node_ids": "101_231"},
        "Casual": {"attr_ids": "101_167", "selectAttributeGroup": "101_167", "exc_attr_id": 101, "attr_node_ids": "101_167"},
        "Sexy": {"attr_ids": "101_580", "selectAttributeGroup": "101_580", "exc_attr_id": 101, "attr_node_ids": "101_580"},
        "Calle": {"attr_ids": "101_648", "selectAttributeGroup": "101_648", "exc_attr_id": 101, "attr_node_ids": "101_648"},
        "Vintage": {"attr_ids": "101_730", "selectAttributeGroup": "101_730", "exc_attr_id": 101, "attr_node_ids": "101_730"},
        "Elegante": {"attr_ids": "101_257", "selectAttributeGroup": "101_257", "exc_attr_id": 101, "attr_node_ids": "101_257"},

        # --- Colores ---
        "Rojo": {"attr_ids": "27_144-27_544", "selectAttributeGroup": "27_5", "exc_attr_id": 27, "attr_node_ids": "27_5"},
        "Negro": {"attr_ids": "27_112", "selectAttributeGroup": "27_6", "exc_attr_id": 27, "attr_node_ids": "27_6"},
        "Blanco": {"attr_ids": "27_103-27_739", "selectAttributeGroup": "27_7", "exc_attr_id": 27, "attr_node_ids": "27_7"},
        "Azul": {"attr_ids": "27_118-27_562-27_1000112-27_1000114-27_1000116", "selectAttributeGroup": "27_8", "exc_attr_id": 27, "attr_node_ids": "27_8"},
        "Verde": {"attr_ids": "27_81-27_334-27_2436-27_2566", "selectAttributeGroup": "27_3", "exc_attr_id": 27, "attr_node_ids": "27_3"},
        "Multicolor": {"attr_ids": "27_113-27_447-27_1000135", "selectAttributeGroup": "27_14", "exc_attr_id": 27, "attr_node_ids": "27_14"},
        "Gris": {
            "attr_ids": "27_336-27_601-27_2486-27_2493-27_1007832",
            "selectAttributeGroup": "27_10",
            "exc_attr_id": 27,
            "attr_node_ids": "27_10"
        },
        "Amarillo": {
            "attr_ids": "27_171-27_330-27_762-27_1000111",
            "selectAttributeGroup": "27_12",
            "exc_attr_id": 27,
            "attr_node_ids": "27_12"
        },
        "Marrón": {
            "attr_ids": "27_137-27_140-27_322-27_1000119-27_1000121-27_1000130-27_1000131",
            "selectAttributeGroup": "27_11",
            "exc_attr_id": 27,
            "attr_node_ids": "27_11"
        },
        "Rosa": {
            "attr_ids": "27_364-27_513-27_1000115-27_1000123",
            "selectAttributeGroup": "27_2",
            "exc_attr_id": 27,
            "attr_node_ids": "27_2"
        },
        "Morado": {
            "attr_ids": "27_536-27_2431-27_1000117-27_1000126-27_1000127-27_1000129",
            "selectAttributeGroup": "27_9",
            "exc_attr_id": 27,
            "attr_node_ids": "27_9"
        },
        "Caqui": {
            "attr_ids": "27_78-27_152-27_379",
            "selectAttributeGroup": "27_13",
            "exc_attr_id": 27,
            "attr_node_ids": "27_13"
        }
    }

    @classmethod
    def get_combined_filters(cls, attributes):
        """
        Combina los filtros avanzados de múltiples atributos seleccionados.
        """

        combined_filters = {"attr_ids": [], "selectAttributeGroup": [], "exc_attr_id": None, "attr_node_ids": []}

        for attr in attributes:
            if attr in cls.ATTRIBUTE_FILTERS:
                attr_filters = cls.ATTRIBUTE_FILTERS[attr]
                if "attr_ids" in attr_filters:
                    combined_filters["attr_ids"].append(attr_filters["attr_ids"])
                if "selectAttributeGroup" in attr_filters:
                    combined_filters["selectAttributeGroup"].append(attr_filters["selectAttributeGroup"])
                if "attr_node_ids" in attr_filters:
                    combined_filters["attr_node_ids"].append(attr_filters["attr_node_ids"])
                if "exc_attr_id" in attr_filters and not combined_filters["exc_attr_id"]:
                    combined_filters["exc_attr_id"] = attr_filters["exc_attr_id"]

        combined_filters["attr_ids"] = "-".join(combined_filters["attr_ids"]) if combined_filters["attr_ids"] else None
        combined_filters["selectAttributeGroup"] = "-".join(combined_filters["selectAttributeGroup"]) if combined_filters["selectAttributeGroup"] else None
        combined_filters["attr_node_ids"] = "-".join(combined_filters["attr_node_ids"]) if combined_filters["attr_node_ids"] else None

        return combined_filters


if __name__ == "__main__":
    print(SheinAttrValues.get_combined_filters([SheinAttrValues.COLOR_VERDE,SheinAttrValues.COLOR_GRIS]))
