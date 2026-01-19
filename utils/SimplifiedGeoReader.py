"""
Leitor simplificado de formatos geográficos sem GDAL.
Usa XML parsing e bibliotecas padrão do Python.
"""

import os
import json
import xml.etree.ElementTree as ET
from typing import Dict, Any, Optional


def read_kml_simple(file_path: str) -> Optional[Dict[str, Any]]:
    """
    Lê metadados básicos de arquivo KML sem driver GDAL.
    Extrai: número de features, tipos de geometria, bounds.
    """
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        # Namespace KML
        ns = {'kml': 'http://www.opengis.net/kml/2.2'}
        
        # Contar Placemarks (features)
        placemarks = root.findall('.//kml:Placemark', ns)
        num_features = len(placemarks)
        
        # Detectar tipos de geometria
        geom_types = set()
        
        for placemark in placemarks:
            # Point
            if placemark.find('kml:Point', ns) is not None:
                geom_types.add('Point')
            # LineString
            elif placemark.find('kml:LineString', ns) is not None:
                geom_types.add('LineString')
            # Polygon
            elif placemark.find('kml:Polygon', ns) is not None:
                geom_types.add('Polygon')
            # MultiGeometry
            elif placemark.find('kml:MultiGeometry', ns) is not None:
                geom_types.add('MultiGeometry')
        
        # Mapear tipos
        type_map = {
            'Point': '📍 Ponto',
            'LineString': '📏 Linha',
            'Polygon': '📦 Polígono',
            'MultiGeometry': '🔹 Multi',
        }
        
        geom_types_str = ', '.join(
            type_map.get(gt, gt) for gt in sorted(geom_types)
        ) or 'Desconhecido'
        
        return {
            'num_features': num_features,
            'geometry_types': geom_types_str,
            'epsg': 4326,  # KML é sempre WGS84
            'crs_name': 'WGS 84',
            'is_sirgas': False,
            'type': 'Vetor',
            'note': '(Leitura simplificada sem GDAL)'
        }
        
    except Exception as e:
        return None


def read_geojson_simple(file_path: str) -> Optional[Dict[str, Any]]:
    """
    Lê metadados de arquivo GeoJSON.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Contar features
        num_features = len(data.get('features', []))
        
        # Detectar tipos
        geom_types = set()
        for feature in data.get('features', []):
            if feature.get('geometry'):
                geom_type = feature['geometry'].get('type')
                if geom_type:
                    geom_types.add(geom_type)
        
        # Mapear tipos
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
        ) or 'Desconhecido'
        
        # CRS (geralmente WGS84 se não especificado)
        crs = data.get('crs', {}).get('properties', {}).get('name', 'WGS 84')
        epsg = 4326
        
        return {
            'num_features': num_features,
            'geometry_types': geom_types_str,
            'epsg': epsg,
            'crs_name': crs,
            'is_sirgas': False,
            'type': 'Vetor'
        }
        
    except Exception as e:
        return None


def read_gpx_simple(file_path: str) -> Optional[Dict[str, Any]]:
    """
    Lê metadados básicos de arquivo GPX (XML).
    GPX sempre é WGS84.
    """
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        # Namespace GPX
        ns = {'gpx': 'http://www.topografix.com/GPX/1/1'}
        
        # Contar waypoints, tracks e routes
        waypoints = root.findall('gpx:wpt', ns)
        tracks = root.findall('gpx:trk', ns)
        routes = root.findall('gpx:rte', ns)
        
        num_features = len(waypoints) + len(tracks) + len(routes)
        
        # Tipos de geometria
        geom_types = []
        if waypoints:
            geom_types.append('📍 Ponto')
        if tracks:
            geom_types.append('📏 Linha')
        if routes:
            geom_types.append('📏 Rota')
        
        geom_types_str = ', '.join(geom_types) if geom_types else 'Desconhecido'
        
        return {
            'num_features': num_features,
            'geometry_types': geom_types_str,
            'epsg': 4326,  # GPX é sempre WGS84
            'crs_name': 'WGS 84',
            'is_sirgas': False,
            'type': 'Vetor'
        }
        
    except Exception as e:
        return None


def get_simple_metadata(file_path: str) -> Optional[Dict[str, Any]]:
    """
    Tenta ler metadados usando parsers simplificados quando GDAL não está disponível.
    """
    if not os.path.exists(file_path):
        return None
    
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == '.kml':
        return read_kml_simple(file_path)
    elif ext == '.geojson':
        return read_geojson_simple(file_path)
    elif ext == '.gpx':
        return read_gpx_simple(file_path)
    
    return None
