def calcular_tiempo_verde_peatonal(cantidad_peatones, velocidad_promedio=1.2, margen_seguridad=2.0):
    """
    Calcula el tiempo verde para peatones en segundos.

    cantidad_peatones: número de peatones que cruzan simultáneamente.
    velocidad_promedio: velocidad promedio de peatones en m/s.
    margen_seguridad: segundos extra de margen de seguridad.

    Retorna: tiempo sugerido en segundos.
    """

    ancho_cruce_metros = 5.0  # ejemplo: ancho del cruce peatonal

    # Tiempo base = distancia / velocidad
    tiempo_base = ancho_cruce_metros / velocidad_promedio

    # Ajuste extra por cada peatón adicional (simulación simple)
    extra_por_persona = 0.2  # segundos extra por peatón adicional

    tiempo = tiempo_base + (cantidad_peatones - 1) * extra_por_persona + margen_seguridad

    # Restringe un mínimo y máximo razonables
    tiempo = max(tiempo, 10.0)  # mínimo 10 segundos
    tiempo = min(tiempo, 60.0)  # máximo 60 segundos

    return tiempo

if __name__ == "__main__":
    cantidad = 8
    tiempo = calcular_tiempo_verde_peatonal(cantidad)
    print(f"Tiempo verde sugerido para {cantidad} peatones: {tiempo:.1f} segundos")
