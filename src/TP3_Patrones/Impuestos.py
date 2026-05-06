class CalculadoraImpuestos:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(CalculadoraImpuestos, cls).__new__(cls)
        return cls._instancia

    def calcular(self, base_imponible):
        if base_imponible < 0:
            raise ValueError("La base imponible no puede ser negativa")

        iva = base_imponible * 0.21
        iibb = base_imponible * 0.05
        contribuciones = base_imponible * 0.012

        total_impuestos = iva + iibb + contribuciones
        return total_impuestos