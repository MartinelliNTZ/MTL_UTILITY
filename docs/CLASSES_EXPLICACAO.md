# Classes em src/ - Explicação Básica

Este documento explica rapidamente o que cada classe em `src/` faz, para iniciantes em Python.

## BasePlugin
Classe base que todos os plugins devem herdar. Define métodos como `create_widget()` (cria a interface do plugin) e `on_base_path_changed()` (chamado quando a pasta muda).

## PluginManager
Gerencia o carregamento de plugins. Procura arquivos Python na pasta `plugins/`, importa e armazena as instâncias. Permite criar widgets dos plugins quando necessário.

## MainWindow
A janela principal da aplicação. Contém menus, barras de ferramentas, área de abas e painel lateral. Coordena tudo: abre plugins, muda configurações, etc.

## Preferences (agora em config/)
Salva e carrega configurações em um arquivo JSON (como a pasta base). Permite get/set de valores, salvando automaticamente.

## SignalManager
Sistema de comunicação entre partes da app. Usa sinais Qt para notificar quando algo muda (ex: pasta base alterada), permitindo plugins reagirem.

## Theme
Contém estilos CSS para a interface dark mode. Define cores, fontes e aparência de botões, abas, etc.

## IconGenerator
Cria ícones SVG como imagens (QPixmap). Tem ícones prontos para calculadora, lista, etc., com gradientes e cores customizáveis.

## PluginUIHelper
Ajuda plugins a criar componentes UI padronizados, como botões, campos de texto, títulos. Reduz código repetido nos plugins.

## Animations
Fornece animações para a interface: hover (passar mouse), click, fade-in. Classes como AnimatedButton fazem botões animados automaticamente.

## DraggableTabWidget / DraggableTabBar
Permite arrastar abas para reordená-las. DraggableTabWidget é o container de abas, DraggableTabBar lida com o drag dos títulos das abas.

## DraggableToolBar
Barra de ferramentas que permite reordenar ícones arrastando. Suporta drag and drop de ações.