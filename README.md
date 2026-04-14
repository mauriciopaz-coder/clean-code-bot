# Clean Code Bot

CLI tool that accepts a "dirty" or undocumented code file and returns an optimized version that follows **SOLID principles** and includes comprehensive technical documentation (docstrings, type hints, etc.) using LLM-powered analysis.

## Features

- **Chain of Thought analysis** — The LLM first identifies problems, then plans the refactoring, then produces clean code
- **SOLID principles enforcement** — Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion
- **Prompt Injection prevention** — Input validation and sanitization to block malicious commands embedded in code
- **Multi-provider support** — Works with Groq (free) or OpenAI (paid)
- **Multi-language support** — Python, JavaScript, TypeScript, Java, C#, C++, Go, Ruby, PHP, Rust, and more

## Project Structure

```
clean-code-bot/
├── clean_code_bot/
│   ├── __init__.py          # Package definition
│   ├── __main__.py          # Entry point for python -m
│   ├── cli.py               # CLI interface using click
│   ├── analyzer.py          # LLM API connection (OpenAI/Groq)
│   ├── prompts.py           # Chain of Thought prompt templates
│   └── sanitizer.py         # Input validation & security
├── examples/
│   ├── before/              # Dirty code samples
│   │   ├── dirty_calculator.py
│   │   └── dirty_user_service.py
│   └── after/               # Clean code samples (reference)
│       ├── clean_calculator.py
│       └── clean_user_service.py
├── .env.example             # Environment variables template
├── requirements.txt         # Python dependencies
├── LICENSE                  # MIT License
└── README.md
```

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/mauriciopaz-coder/clean-code-bot.git
cd clean-code-bot
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure your API key

```bash
cp .env.example .env
```

Edit the `.env` file and add your API key:

**Option A — Groq (Free)**

Get your key at [console.groq.com](https://console.groq.com)

```
LLM_PROVIDER=groq
GROQ_API_KEY=gsk_your-key-here
```

**Option B — OpenAI (Paid, ~$5 USD minimum)**

Get your key at [platform.openai.com](https://platform.openai.com)

```
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-key-here
```

## Usage

### Basic usage

```bash
python -m clean_code_bot path/to/dirty_code.py
```

### Full analysis with detailed output

```bash
python -m clean_code_bot path/to/dirty_code.py --full
```

### Save refactored code to a file

```bash
python -m clean_code_bot path/to/dirty_code.py -o clean_output.py
```

### Choose a specific provider

```bash
python -m clean_code_bot path/to/dirty_code.py --provider openai
```

### CLI Options

| Option | Description |
|---|---|
| `--provider [openai\|groq]` | LLM provider (default: `groq`) |
| `--output, -o FILE` | Save refactored code to a file |
| `--full` | Show full analysis + changes summary |
| `--help` | Show help message |

## Example

### Input (dirty code)

```python
def calc(a,b,op):
    if op == "add":
        return a+b
    elif op == "sub":
        return a-b
    elif op == "mul":
        return a*b
    elif op == "div":
        return a/b
```

### Output (after running the bot with `--full`)

```
=== ANALYSIS ===
1. Magic strings for operations — violates Open/Closed Principle
2. No error handling for division by zero
3. No type hints or docstrings
...

=== REFACTORED CODE ===
# Clean version with Strategy pattern, type hints, docstrings, error handling

=== CHANGES SUMMARY ===
- Extracted operations into separate classes (SRP)
- Added Operation enum to replace magic strings (OCP)
- Added ZeroDivisionError handling
- Added type hints and docstrings
```

See the full before/after examples in the [`examples/`](examples/) folder.

## Security

The tool includes input validation to prevent **Prompt Injection** attacks:

- **File extension validation** — Only accepts known code file extensions
- **File size limit** — Maximum 100 KB per file
- **Injection pattern detection** — Scans for common prompt injection patterns like "ignore previous instructions", special model tokens, etc.
- **System prompt protection** — The LLM is instructed to ignore any directives embedded in the user's code

## Technologies

- **Python 3.12+**
- **click** — CLI framework
- **openai** — API client (compatible with both OpenAI and Groq)
- **python-dotenv** — Environment variable management
- **Groq Cloud / Llama 3.3 70B** — Free LLM inference

## License

MIT
