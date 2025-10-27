# Ontbo — Alex Persona & Evaluation

Ontbo’s **Alex** persona and a small set of assets to help you run basic, local evaluations of a role-played AI assistant. The repository currently contains an `HTML/` demo folder, a `Python/` folder, and a `Persona.zip` bundle with the core persona materials.


## What’s in this repo

- `HTML/` — a static, local demo you can open in your browser to explore or sanity-check the Alex persona.
- `Python/` — minimal Python utilities intended for simple, scriptable evaluations.
- `Persona.zip` — a compressed bundle that contains the Alex persona specification (and possibly supporting prompts/data). Unzip this in the repository root to use.

---

## Quick start

### Option A — HTML demo

1. **Clone or download** this repository.
2. **Open the demo**:
   - Double-click the main entry file inside `HTML/` (commonly `index.html`).  
   - If there’s no `index.html`, open the most relevant HTML file in that folder and follow on-screen instructions.

> The repository is predominantly HTML (≈86.5%), so the browser demo is the most direct way to poke at the persona. :contentReference[oaicite:4]{index=4}

### Option B — Python utilities

1. Ensure you have **Python 3.10+** installed.
2. (If a `requirements.txt` or `pyproject.toml` is present) create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements.txt

## Analyze

A simple answer analyzer is available in Python folder, calculating the means of each type of answer.

## Persona

Persona used in this experiment is available in a ZIP folder in repository root. 
