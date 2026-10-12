# Patient Triage System

An intelligent, multi-agent patient triage system built around the concept of the "Strands Decider" orchestrator. The system extracts structured medical data from unstructured clinical notes and automatically assigns an Emergency Severity Index (ESI) triage level (1 to 5) based on the ABCDE rule, vital signs, and expected hospital resource utilization.

---

## Architecture & Components

The application follows a modular, decoupled design:

1. **Intake Extractor (`src/extractor.py`)**: Uses Google Gemini models with native structured outputs to parse raw, unstructured clinical notes into a strongly-typed `Patient` schema. Supports multiple Gemini model variants and handles API rate-limit/quota errors.
2. **Models (`src/models.py`)**: Defines Pydantic data schemas, specifically the `Patient` model (demographics, vital signs, ABCDE status, and clinical notes).
3. **Decider (`src/decider.py`)**: Mock implementation of the `StrandsDecider` routing mechanism that evaluates triage rules and assigns priority levels (Levels 1–5).
4. **Orchestrator (`src/orchestrator.py`)**: Coordinates patient state evaluation and interfaces with the Decider to output final triage rulings and clinical reasoning.
5. **Streamlit UI (`src/app.py`)**: Interactive web application featuring note input/sample loading, model switching, reactive state management, and real-time triage evaluation.
6. **CLI Triage Demo (`src/triage.py`)**: CLI script executing 3 fixed test cases followed by an automated random extraction test from the dataset.

---

## Supported Extraction Models

The system supports hot-swapping between multiple Gemini models directly from the UI or via code:

- **Gemini 3.5 Flash** (`models/gemini-3.5-flash`) *(Default)*
- **Gemini 3.0 Flash** (`models/gemini-3.0-flash`)
- **Gemini 2.5 Flash** (`models/gemini-2.5-flash`)
- **Gemini 2.5 Pro** (`models/gemini-2.5-pro`)

*Note: Rate limit (`429 Quota Exceeded`) errors are caught and surfaced via notification toasts in the UI without crashing the application.*

---

## Setup & Installation

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. API Configuration
Create a `config.json` file in the root directory (copy from `config.example.json`):
```json
{
    "GEMINI_API_KEY": "your_actual_api_key_here"
}
```
*(Make sure not to commit `config.json` — it is excluded in `.gitignore`.)*

### 3. Download Sample Dataset
Fetch the `AGBonnet/augmented-clinical-notes` dataset from Hugging Face to populate `data/dataset.jsonl`:
```bash
python data/loader.py
```

---

## Usage

### Interactive Web Application (Streamlit)
Launch the triage web interface:
```bash
streamlit run src/app.py
```

**Features:**
- **Sample Note Loader**: Automatically loads random clinical notes from `data/dataset.jsonl` or pre-filled clinical scenarios.
- **Model Switcher**: Easily toggle between Gemini 2.5/3.0/3.5 Flash and 2.5 Pro models in the sidebar.
- **State Preservation & Responsive UI**: Disables inputs and the run button while triage inference is in progress to avoid double-submissions.
- **Structured Output**: Displays extracted patient vitals, ABCDE evaluation, and assigned triage level with clinical rationale.

### Command-Line Interface (CLI)
Run the automated triage evaluation suite:
```bash
python src/triage.py
```
This runs:
- **Case 1 (Level 1)**: Severe respiratory arrest / unresponsiveness (Immediate resuscitation).
- **Case 2 (Level 2)**: High-risk acute coronary syndrome / severe chest pain (Emergent).
- **Case 3 (Level 4)**: Mild ankle sprain requiring simple X-ray (Less urgent).
- **Random Sample**: A randomly pulled clinical note parsed via Gemini and routed through the orchestrator.
