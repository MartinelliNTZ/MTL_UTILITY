"""
Leitor de metadados de arquivos geográficos (vetor e raster).

Extrai informações de:
- Arquivos vetoriais (SHP, GeoJSON, GML, etc) usando Fiona
- Arquivos raster (TIFF, ECW, JP2, etc) usando Rasterio
"""

import os
import re
from typing import Dict, Any, Optional, List
from pathlib import Path

try:
    import fiona
    FIONA_AVAILABLE = True
except ImportError:
    FIONA_AVAILABLE = False

try:
    import rasterio
    RASTERIO_AVAILABLE = True
except ImportError:
    RASTERIO_AVAILABLE = False

try:
    from shapely.geometry import shape
    SHAPELY_AVAILABLE = True
except ImportError:
    SHAPELY_AVAILABLE = False


def extract_epsg_from_crs(crs_string: str) -> Optional[int]:
    """Extrai EPSG de uma string CRS usando regex."""
    if not crs_string:
        return None
    
    # Tenta padrões comuns
    patterns = [
        r'EPSG["\']?\s*[,:]?\s*["\']?(\d{4,5})',  # EPSG:4674 ou EPSG,"4674"
        r'AUTHORITY\s*\[\s*["\']EPSG["\']\s*,\s*["\'](\d{4,5})["\']',  # AUTHORITY["EPSG","4674"]
    ]
    
    for pattern in patterns:
        match = re.search(pattern, crs_string, re.IGNORECASE)
        if match:
            return int(match.group(1))
    
    return None


def simplify_crs_name(crs_string: str) -> str:
    """Simplifica string CRS longa para nome curto."""
    if not crs_string:
        return "Desconhecido"
    
    # Se for LOCAL_CS["SIRGAS 2000 / UTM zone 23S"...], extrai a parte em quotes
    match = re.search(r'LOCAL_CS\s*\[\s*"([^"]+)"', crs_string)
    if match:
        return match.group(1)
    
    # Se for PROJCS ou GEOGCS, tenta extrair o nome
    match = re.search(r'(?:PROJCS|GEOGCS)\s*\[\s*"([^"]+)"', crs_string)
    if match:
        return match.group(1)
    
    # Fallback: retorna os primeiros 50 caracteres
    return crs_string[:50] + "..." if len(crs_string) > 50 else crs_string
def get_vector_metadata(file_path: str) -> Optional[Dict[str, Any]]:
    """
    Extrai metadados de arquivo vetorial.
    
    Returns:
        Dict com: num_features, geometry_types, epsg, is_sirgas, crs_name
    """
    if not FIONA_AVAILABLE:
        # Fallback para leitura simplificada
        from utils.SimplifiedGeoReader import get_simple_metadata
        return get_simple_metadata(file_path)
    
    try:
        with fiona.open(file_path) as src:
            # CRS info
            crs = src.crs
            crs_string = crs.to_string() if crs else ""
            
            # Tenta obter EPSG, senão extrai da string
            epsg = crs.to_epsg() if crs else None
            if not epsg:
                epsg = extract_epsg_from_crs(crs_string)
            
            # Nome CRS simplificado
            if crs:
                crs_name = simplify_crs_name(crs_string)
            else:
                crs_name = "Desconhecido"
            
            # Check if SIRGAS
            is_sirgas = False
            if epsg:
                is_sirgas = 4674 <= epsg <= 4680
            
            # Count geometries and types
            num_features = len(src)
            geom_types = set()
            
            for feature in src:
                geom_type = feature['geometry']['type']
                geom_types.add(geom_type)
            
            # Translate geometry types
            type_map = {
                'Point': '📍 Ponto',
                'LineString': '📏 Linha',
                'Polygon': '📦 Polígono',
                'MultiPoint': '📍 Multiponto',
                'MultiLineString': '📏 Multilinha',
                'MultiPolygon': '📦 Multipolígono',
            }
            
            geom_types_str = ', '.join(
                type_map.get(gt, gt) for gt in sorted(geom_types)
            )
            
            return {
                'num_features': num_features,
                'geometry_types': geom_types_str,
                'epsg': epsg,
                'crs_name': crs_name,
                'is_sirgas': is_sirgas,
                'type': 'Vetor'
            }
            
    except Exception as e:
        from utils.LogUtils import logger
        logger.error("GeoMetadataReader", "get_vector_metadata", f"Erro ao ler {file_path}: {e}")
        # Tenta fallback simplificado
        from utils.SimplifiedGeoReader import get_simple_metadata
        result = get_simple_metadata(file_path)
        if result:
            return result
        return {'error': str(e), 'type': 'Vetor'}


def get_raster_metadata(file_path: str) -> Optional[Dict[str, Any]]:
    """
    Extrai metadados de arquivo raster.
    
    Returns:
        Dict com: width, height, pixel_size, epsg, is_sirgas, crs_name, bands
    """
    if not RASTERIO_AVAILABLE:
        return None
    
    try:
        with rasterio.open(file_path) as src:
            # Dimensões
            width = src.width
            height = src.height
            
            # CRS info
            crs = src.crs
            crs_string = crs.to_string() if crs else ""
            
            # Tenta obter EPSG, senão extrai da string CRS
            epsg = crs.to_epsg() if crs else None
            if not epsg:
                epsg = extract_epsg_from_crs(crs_string)
            
            # Nome CRS simplificado
            if crs:
                crs_name = simplify_crs_name(crs_string)
            else:
                crs_name = "Desconhecido"
            
            # Check if SIRGAS
            is_sirgas = False
            if epsg:
                is_sirgas = 4674 <= epsg <= 4680 or epsg == 31983  # SIRGAS 2000 / UTM zone 23S
            
            # Tamanho do pixel (resolução)
            transform = src.transform
            pixel_size_x = abs(transform.a)
            pixel_size_y = abs(transform.e)
            pixel_size = f"{pixel_size_x:.6f} × {pixel_size_y:.6f}"
            
            # Bandas (apenas contar, não carregar dados)
            num_bands = src.count
            
            return {
                'width': width,
                'height': height,
                'pixel_size': pixel_size,
                'epsg': epsg,
                'crs_name': crs_name,
                'is_sirgas': is_sirgas,
                'num_bands': num_bands,
                'type': 'Raster'
            }
            
    except Exception as e:
        from utils.LogUtils import logger
        logger.error("GeoMetadataReader", "get_raster_metadata", f"Erro ao ler {file_path}: {e}")
        return {'error': str(e), 'type': 'Raster'}


def get_file_metadata(file_path: str) -> Optional[Dict[str, Any]]:
    """Detecta tipo e extrai metadados apropriados."""
    from utils.VectorUtils import VECTOR_FORMATS
    from utils.RasterUtils import RASTER_FORMATS
    
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext in VECTOR_FORMATS:
        return get_vector_metadata(file_path)
    elif ext in RASTER_FORMATS:
        return get_raster_metadata(file_path)
    
    return None


def format_metadata_text(metadata: Dict[str, Any]) -> str:
    """Formata metadados em texto legível."""
    if not metadata:
        return "Sem metadados disponíveis"
    
    if 'error' in metadata:
        return f"❌ Erro ao ler: {metadata['error']}"
    
    if metadata['type'] == 'Vetor':
        epsg_text = f"EPSG:{metadata['epsg']}" if metadata['epsg'] else "Sem EPSG"
        sirgas_text = "(SIRGAS)" if metadata['is_sirgas'] else "(WGS84/Outro)"
        
        text = f"""📍 ARQUIVO VETORIAL

Feições: {metadata['num_features']}
Tipos: {metadata['geometry_types']}

CRS: {metadata['crs_name']}
{epsg_text} {sirgas_text}
"""
        return text.strip()
    
    elif metadata['type'] == 'Raster':
        epsg_text = f"EPSG:{metadata['epsg']}" if metadata['epsg'] else "Sem EPSG"
        sirgas_text = "(SIRGAS)" if metadata['is_sirgas'] else "(WGS84/Outro)"
        
        text = f"""🗺️ ARQUIVO RASTER

Dimensões: {metadata['width']} × {metadata['height']} pixels
Pixel: {metadata['pixel_size']}

CRS: {metadata['crs_name']}
{epsg_text} {sirgas_text}

Bandas: {metadata['num_bands']}
"""
        return text.strip()
    
    return "Tipo desconhecido"
