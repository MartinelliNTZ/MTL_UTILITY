# Mini-IDE inspirado no Visual Studio (PySide6)

Este projeto é um exemplo minimalista de uma aplicação estilo IDE construída com PySide6.

Principais features:
- Barra lateral com ícones que abre um painel lateral (Explorer).
- Área central com abas fecháveis onde cada plugin é exibido.
- Barra de tarefas inferior com ícones (placeholders).
- Sistema de plugins simples: coloque arquivos Python em `plugins/` que implementem `get_plugin()` retornando uma instância de `BasePlugin`.

Como executar:

1. Instale dependências:

```bash
pip install -r requirements.txt
```

2. Execute:

```bash
python main.py
```

Estrutura esperada:
- `main.py` - entrada da aplicação
- `src/` - implementação principal (UI e gerenciador de plugins)
- `plugins/` - plugins de exemplo e lugar para adicionar novos plugins
- `config/` - arquivos de configuração
- `docs/` - documentação e arquivos README

Como criar um plugin:

1. Crie um arquivo Python em `plugins/`.
2. Implemente uma classe que herde de `src.base_plugin.BasePlugin` e implemente `create_widget(self, parent)`.
3. Exponha uma função `get_plugin()` que retorne uma instância do plugin.
