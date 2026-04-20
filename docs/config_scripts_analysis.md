# Análise Técnica dos Scripts da Pasta config/

Ei! Vou explicar **tudo** de forma bem simples, como se você fosse uma criança de 5 anos aprendendo a programar pela primeira vez. Nada de termos complicados sem explicação. Vamos devagar e com exemplos!

A pasta `config/` tem **2 scripts Python importantes**:
1. `log_viewer.py` 
2. `preferences.py`

Os outros arquivos são: `config.json` (configurações em formato texto), e logs (arquivos de diário da aplicação). Só vou falar dos **scripts** (códigos Python).

## 1. log_viewer.py - O \"Espião dos Logs\"

### Classe `LogEntry` 
**O que é?** É como uma **ficha de identidade** para cada linha de log (diário do programa).

**O que ela faz?** 
- Guarda 6 coisas básicas de cada mensagem do log:
  | Campo | O que é? | Exemplo |
  |-------|----------|---------|
  | `timestamp` | Hora exata | \"2024-01-18 12:46:49\" |
  | `level` | Gravidade | \"INFO\", \"ERROR\" |
  | `tool_key` | Quem falou | \"calculator\" |
  | `class_name` | De qual parte | \"CalculatorUI\" |
  | `message` | O que aconteceu | \"Botão clicado!\" |
  | `extra_data` | Detalhes extras | {\"user\": \"marti\"} |

**Por que existe?** Para organizar as mensagens bagunçadas do log em \"pacotinhos\" fáceis de usar.

**Como funciona?** 
```python
# Imagina assim:
entrada = LogEntry({
    'timestamp': '10:00',
    'level': 'INFO', 
    'tool_key': 'calculator',
    'message': 'Olá mundo!'
})
print(entrada.message)  # \"Olá mundo!\"
```
É só um \"guarda-chuva\" que junta tudo.

---

### Classe `LogViewer` (A principal - estrela do show!)
**O que é?** Uma **janela bonita** (usando PySide6/Qt) que mostra **TODOS os logs** da aplicação de forma organizada.

**O que ela faz? (Passo a passo burro):**
1. **Carrega logs**: Pega arquivos `.log` da pasta `%LOCALAPPDATA%/MTL_UTIL/logs/`
2. **Mostra em tabela**: Como uma planilha Excel com 5 colunas:
   - Data/Hora | ToolKey | Classe | Nível | Mensagem
3. **Pinta de cores** (legal!):
   - Cada `tool_key` tem cor diferente (ex: calculator=azul, todo_list=verde)
   - Níveis: INFO=verde, ERROR=vermelho
4. **Filtra tudo**:
   - Combo de ToolKey (\"Todos\", \"calculator\", etc.)
   - Combo de Classe
   - Combo de Nível (DEBUG, INFO, WARNING...)
   - Caixa de busca (digita qualquer palavra)
5. **Detalhes**: Clica numa linha → mostra tudo embaixo (incluindo extras)

**Interface (imagine):**
```
[Seletor de arquivo log]  <- Escolhe qual log ver

Filtros:
ToolKey: [Todos ▼]  Classe: [Todos ▼]  Nível: [Todos ▼]  Pesquisar: [____] [Limpar]

Tabela colorida:
10:00 | calculator (azul) | CalcUI | INFO (verde) | \"2+2=4\"

Detalhes:
Timestamp: 10:00
Tool: calculator
...
```

**Cores fixas** (hardcoded):
- calculator: azul claro
- preferences: amarelo ouro
- etc. (20+ cores)

**Por que importante?** Sem isso, logs são texto bagunçado. Com isso, é **detetive fácil** pra achar erros!

---

## 2. preferences.py - O \"Caderno de Anotações\" da App

### Classe `Preferences` (única classe)
**O que é?** Um **gerenciador de configurações** que salva preferências em `preferences.json` na pasta `%LOCALAPPDATA%/MTL_UTIL/preferences/`.

**O que ela faz? (Super simples):**
- **Salva** qualquer coisa em um arquivo JSON (como um dicionário)
- **Carrega** quando a app inicia
- **Padrão**: `{\"base_path\": \"C:/\"}`

**Métodos (funções) explicados:**
| Método | O que faz? | Exemplo |
|--------|------------|---------|
| `__init__` | Cria e carrega o arquivo | `prefs = Preferences()` |
| `get(key, default)` | Pega valor OU default | `prefs.get('cor', 'azul')` → 'azul' |
| `set(key, value)` | Salva e **AUTO-SALVA** no disco | `prefs.set('base_path', 'D:/')` |
| `get_base_path()` | Pega caminho base | `'C:/'` |
| `set_base_path(path)` | Define caminho base | `prefs.set_base_path('D:/Projetos')` |
| `reset()` | Volta pro padrão | Tudo vira `{\"base_path\": \"C:/\"}` |

**Onde salva?** 
```
C:\Users\marti\AppData\Local\MTL_UTIL\preferences\preferences.json
```

**Exemplo de uso burro:**
```python
prefs = Preferences()

# Salva onde você quer navegar
prefs.set_base_path('C:/Users/marti/Desktop')

# Na próxima vez que abrir app, já lembra!
caminho = prefs.get_base_path()  # 'C:/Users/marti/Desktop'
```

**Por que existe?** Pra app **lembrar suas escolhas** (tipo pasta favorita) sem você configurar toda vez.

---

## Resumo Final (pra gravar na cabeça):
- **`LogEntry`**: Ficha de cada mensagem de log ✅
- **`LogViewer`**: Janela pra ESPIONAR logs com filtros e cores 🎨
- **`Preferences`**: Caderno que SALVA suas preferências pra sempre 📝

**Total: 3 classes.** Tudo roda no Windows, usa JSON pros logs/configs, e PySide6 pra janelas bonitas.

Se tiver dúvida, pergunta qual parte! 😊

