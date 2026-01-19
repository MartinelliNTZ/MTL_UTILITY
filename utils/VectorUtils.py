"""
VectorUtils - Utilitários para arquivos vetoriais (SHP, KML, GeoJSON, etc)
"""

from typing import List

# Formatos de arquivo vetorial suportados
VECTOR_FORMATS: List[str] = [
    '.shp',      # ESRI Shapefile
    '.kml',      # Keyhole Markup Language
    '.kmz',      # Compressed KML
    '.geojson',  # GeoJSON
    '.gpx',      # GPS Exchange Format
    '.gml',      # Geography Markup Language
    '.dxf',      # Drawing Exchange Format
    '.dgn',      # MicroStation Design
    '.gdb',      # FileGeoDatabase
    '.tab',      # MapInfo TAB
    '.mif',      # MapInfo MIF
]

# Mapeamento de extensões para descrições amigáveis
VECTOR_FORMAT_NAMES = {
    '.shp': 'ESRI Shapefile',
    '.kml': 'Keyhole Markup Language',
    '.kmz': 'Compressed KML',
    '.geojson': 'GeoJSON',
    '.gpx': 'GPS Exchange Format',
    '.gml': 'Geography Markup Language',
    '.dxf': 'Drawing Exchange Format',
    '.dgn': 'MicroStation Design',
    '.gdb': 'FileGeoDatabase',
    '.tab': 'MapInfo TAB',
    '.mif': 'MapInfo MIF',
}

def get_supported_extensions() -> List[str]:
    """Retorna lista de extensões vetoriais suportadas."""
    return VECTOR_FORMATS

def is_vector_file(filename: str) -> bool:
    """Verifica se um arquivo é formato vetorial suportado."""
    import os
    ext = os.path.splitext(filename)[1].lower()
    return ext in VECTOR_FORMATS

def get_format_name(extension: str) -> str:
    """Retorna nome amigável da extensão."""
    return VECTOR_FORMAT_NAMES.get(extension.lower(), extension)
