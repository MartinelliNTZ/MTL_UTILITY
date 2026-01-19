from PySide6.QtGui import QPixmap, QColor
from PySide6.QtCore import QByteArray
from utils.ToolKey import ToolKey
from utils.LogUtils import logger

TOOL_KEY = ToolKey.ICON_GENERATOR


def create_icon_pixmap(icon_name: str, size: int = 24, color: str = "#0e639c") -> QPixmap:
    """Cria um ícone SVG em formato QPixmap com estilo moderno."""
    
    svg_icons = {
        "calculator": f'''
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="{size}" height="{size}">
                <defs>
                    <linearGradient id="calcGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" style="stop-color:{color};stop-opacity:1" />
                        <stop offset="100%" style="stop-color:#0a4a7a;stop-opacity:1" />
                    </linearGradient>
                </defs>
                <rect x="2" y="2" width="20" height="20" rx="2" fill="url(#calcGrad)"/>
                <rect x="3" y="3" width="18" height="18" rx="1.5" stroke="rgba(255,255,255,0.2)" stroke-width="0.5" fill="none"/>
                <line x1="3" y1="8" x2="21" y2="8" stroke="rgba(255,255,255,0.15)" stroke-width="1"/>
                <circle cx="7" cy="13" r="1.2" fill="white" opacity="0.9"/>
                <circle cx="12" cy="13" r="1.2" fill="white" opacity="0.9"/>
                <circle cx="17" cy="13" r="1.2" fill="white" opacity="0.9"/>
                <circle cx="7" cy="18" r="1.2" fill="white" opacity="0.9"/>
                <circle cx="12" cy="18" r="1.2" fill="white" opacity="0.9"/>
                <circle cx="17" cy="18" r="1.2" fill="white" opacity="0.9"/>
            </svg>
        ''',
        "checklist": f'''
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="{size}" height="{size}">
                <defs>
                    <linearGradient id="checkGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" style="stop-color:#4ec9b0;stop-opacity:1" />
                        <stop offset="100%" style="stop-color:#2fa48f;stop-opacity:1" />
                    </linearGradient>
                </defs>
                <rect x="3" y="3" width="18" height="18" rx="2" fill="url(#checkGrad)"/>
                <rect x="3.5" y="3.5" width="17" height="17" rx="1.5" stroke="rgba(255,255,255,0.2)" stroke-width="0.5" fill="none"/>
                <path d="M8 12L11 15L17 8" stroke="white" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        ''',
        "browser": f'''
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="{size}" height="{size}">
                <defs>
                    <linearGradient id="browserGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" style="stop-color:#f48771;stop-opacity:1" />
                        <stop offset="100%" style="stop-color:#d84630;stop-opacity:1" />
                    </linearGradient>
                </defs>
                <rect x="2" y="3" width="20" height="18" rx="2" fill="url(#browserGrad)"/>
                <rect x="2.5" y="3.5" width="19" height="17.5" rx="1.5" stroke="rgba(255,255,255,0.2)" stroke-width="0.5" fill="none"/>
                <line x1="2" y1="9" x2="22" y2="9" stroke="rgba(255,255,255,0.15)" stroke-width="1"/>
                <circle cx="6" cy="6" r="0.8" fill="white" opacity="0.9"/>
                <circle cx="10" cy="6" r="0.8" fill="white" opacity="0.9"/>
                <circle cx="14" cy="6" r="0.8" fill="white" opacity="0.9"/>
            </svg>
        ''',
        "text": f'''
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="{size}" height="{size}">
                <defs>
                    <linearGradient id="textGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" style="stop-color:#ce9178;stop-opacity:1" />
                        <stop offset="100%" style="stop-color:#a75a3f;stop-opacity:1" />
                    </linearGradient>
                </defs>
                <rect x="2" y="2" width="20" height="20" rx="2" fill="url(#textGrad)"/>
                <rect x="2.5" y="2.5" width="19" height="19" rx="1.5" stroke="rgba(255,255,255,0.2)" stroke-width="0.5" fill="none"/>
                <line x1="6" y1="8" x2="18" y2="8" stroke="white" stroke-width="1.2" stroke-linecap="round" opacity="0.9"/>
                <line x1="6" y1="12" x2="18" y2="12" stroke="white" stroke-width="1.2" stroke-linecap="round" opacity="0.9"/>
                <line x1="6" y1="16" x2="14" y2="16" stroke="white" stroke-width="1.2" stroke-linecap="round" opacity="0.9"/>
            </svg>
        ''',
        "plugins": f'''
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="{size}" height="{size}">
                <defs>
                    <linearGradient id="pluginsGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" style="stop-color:#9cdcfe;stop-opacity:1" />
                        <stop offset="100%" style="stop-color:#5a9fb5;stop-opacity:1" />
                    </linearGradient>
                </defs>
                <rect x="3" y="5" width="8" height="8" rx="1" fill="url(#pluginsGrad)" opacity="0.8"/>
                <rect x="13" y="5" width="8" height="8" rx="1" fill="url(#pluginsGrad)"/>
                <rect x="3" y="15" width="8" height="4" rx="1" fill="url(#pluginsGrad)" opacity="0.8"/>
                <rect x="13" y="15" width="8" height="4" rx="1" fill="url(#pluginsGrad)"/>
                <rect x="3" y="5" width="8" height="8" rx="1" stroke="rgba(255,255,255,0.15)" stroke-width="0.5" fill="none"/>
                <rect x="13" y="5" width="8" height="8" rx="1" stroke="rgba(255,255,255,0.15)" stroke-width="0.5" fill="none"/>
                <rect x="3" y="15" width="8" height="4" rx="1" stroke="rgba(255,255,255,0.15)" stroke-width="0.5" fill="none"/>
                <rect x="13" y="15" width="8" height="4" rx="1" stroke="rgba(255,255,255,0.15)" stroke-width="0.5" fill="none"/>
            </svg>
        ''',
        "ico_converter": f'''
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="{size}" height="{size}">
                <defs>
                    <linearGradient id="icoGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" style="stop-color:#dcdcaa;stop-opacity:1" />
                        <stop offset="100%" style="stop-color:#b8a85a;stop-opacity:1" />
                    </linearGradient>
                </defs>
                <rect x="2" y="2" width="20" height="20" rx="2" fill="url(#icoGrad)"/>
                <rect x="2.5" y="2.5" width="19" height="19" rx="1.5" stroke="rgba(255,255,255,0.2)" stroke-width="0.5" fill="none"/>
                <circle cx="8" cy="8" r="2" fill="white" opacity="0.9"/>
                <circle cx="16" cy="8" r="2" fill="white" opacity="0.9"/>
                <circle cx="8" cy="16" r="2" fill="white" opacity="0.9"/>
                <circle cx="16" cy="16" r="2" fill="white" opacity="0.9"/>
                <text x="12" y="14" text-anchor="middle" fill="white" font-size="6" font-weight="bold">ICO</text>
            </svg>
        ''',
        "image": f'''
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="{size}" height="{size}">
                <defs>
                    <linearGradient id="imageGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" style="stop-color:#9cdcfe;stop-opacity:1" />
                        <stop offset="100%" style="stop-color:#4a9dd4;stop-opacity:1" />
                    </linearGradient>
                </defs>
                <rect x="2" y="2" width="20" height="20" rx="2" fill="url(#imageGrad)"/>
                <rect x="2.5" y="2.5" width="19" height="19" rx="1.5" stroke="rgba(255,255,255,0.2)" stroke-width="0.5" fill="none"/>
                <circle cx="8" cy="9" r="2" fill="white" opacity="0.9"/>
                <path d="M2 18L9 11L15 17L22 10" stroke="white" stroke-width="1.5" fill="none" stroke-linecap="round" stroke-linejoin="round" opacity="0.9"/>
                <path d="M15 17L22 10" stroke="white" stroke-width="1.5" fill="none" stroke-linecap="round" stroke-linejoin="round" opacity="0.9"/>
            </svg>
        '''
    }
    
    svg_data = svg_icons.get(icon_name, svg_icons["plugins"])
    
    pixmap = QPixmap(size, size)
    pixmap.fill(QColor(255, 255, 255, 0))
    
    from PySide6.QtSvg import QSvgRenderer
    from PySide6.QtGui import QPainter
    
    renderer = QSvgRenderer(QByteArray(svg_data.encode()))
    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.end()
    
    return pixmap
