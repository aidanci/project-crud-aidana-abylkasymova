def validate_planet(data):
    required_fields = ["name", "system", "climate", "population", "surfaceType", "temperature", "terrainType"]
    
    for field in required_fields:
        if field not in data:
            return f"Field '{field}' is required"
    
    if not isinstance(data["name"], str) or not data["name"].strip():
        return "Field 'name' must be a non-empty string"
    if not isinstance(data["system"], str) or not data["system"].strip():
        return "Field 'system' must be a non-empty string"
    if not isinstance(data["climate"], str):
        return "Field 'climate' must be a string"
    if not isinstance(data["surfaceType"], str):
        return "Field 'surfaceType' must be a string"
    if not isinstance(data["temperature"], str):
        return "Field 'temperature' must be a string"
    if not isinstance(data["terrainType"], str):
        return "Field 'terrainType' must be a string"
    
    try:
        data["population"] = int(data["population"])
        if data["population"] < 0:
            return "Population must be >= 0"
    except ValueError:
        return "Population must be an integer"
    
    return None
