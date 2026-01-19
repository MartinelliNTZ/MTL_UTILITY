"""
RasterUtils - Utilitários para arquivos raster (TIFF, ECW, HDF, etc)
"""

from typing import List

# Formatos de arquivo raster suportados
RASTER_FORMATS: List[str] = [
    '.tif',      # Tagged Image File
    '.tiff',     # Tagged Image File Format
    '.ecw',      # Enhanced Compressed Wavelet
    '.img',      # ERDAS Imagine
    '.hdf',      # Hierarchical Data Format
    '.jp2',      # JPEG 2000
    '.sid',      # MrSID (Multi-resolution Seamless Image Database)
    '.ers',      # Erdas LAN
    '.j2k',      # JPEG 2000 Codestream
    '.h5',       # HDF5
    '.vrt',      # GDAL Virtual Raster
    '.asc',      # ASCII Grid
]

# Mapeamento de extensões para descrições amigáveis
RASTER_FORMAT_NAMES = {
    '.tif': 'Tagged Image File',
    '.tiff': 'Tagged Image File Format',
    '.ecw': 'Enhanced Compressed Wavelet',
    '.img': 'ERDAS Imagine',
    '.hdf': 'Hierarchical Data Format',
    '.jp2': 'JPEG 2000',
    '.sid': 'MrSID',
    '.ers': 'Erdas LAN',
    '.j2k': 'JPEG 2000 Codestream',
    '.h5': 'HDF5',
    '.vrt': 'GDAL Virtual Raster',
    '.asc': 'ASCII Grid',
}

def get_supported_extensions() -> List[str]:
    """Retorna lista de extensões raster suportadas."""
    return RASTER_FORMATS

def is_raster_file(filename: str) -> bool:
    """Verifica se um arquivo é formato raster suportado."""
    import os
    ext = os.path.splitext(filename)[1].lower()
    return ext in RASTER_FORMATS

def get_format_name(extension: str) -> str:
    """Retorna nome amigável da extensão."""
    return RASTER_FORMAT_NAMES.get(extension.lower(), extension)
