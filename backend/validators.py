def validate_planet(data: dict):
    if not isinstance(data, dict):
        return "Invalid JSON body"

    name = data.get("name")
    system = data.get("system")
    climate = data.get("climate")
    population = data.get("population")
    surface_type = data.get("surfaceType")

    if not name or not isinstance(name, str):
        return "Field 'name' is required"
    if not system or not isinstance(system, str):
        return "Field 'system' is required"
    if not climate or not isinstance(climate, str):
        return "Field 'climate' is required"

    try:
        population = int(population)
    except (TypeError, ValueError):
        return "Field 'population' must be an integer"

    if population < 0:
        return "Field 'population' must be >= 0"

    if not surface_type or not isinstance(surface_type, str):
        return "Field 'surfaceType' is required"

    return None
