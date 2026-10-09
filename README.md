# Patient Triage System

An intelligent, multi-agent patient triage system built around the concept of the "Strands Decider" orchestrator. This system evaluates unstructured clinical notes and automatically assigns a triage level (1 to 5) based on the ABCDE rule, expected hospital resources, and vital signs.

## Architecture

The system is broken down into clean, modular components:

1. **Intake Extractor (`src/extractor.py`)**: Uses **Gemini 3.5 Flash** (via native structured outputs) to parse unstructured clinical notes and convert them into a structured `Patient` schema.
2. **Models (`src/models.py`)**: Defines the Pydantic data schemas, specifically the `Patient` object.
3. **Decider (`src/decider.py`)**: A mock implementation of the `StrandsDecider` model that acts as a fast-routing mechanism for the system to pick from defined triage levels.
4. **Orchestrator (`src/orchestrator.py`)**: The `TriageOrchestrator` agent coordinates the state of the patient and passes it to the Decider to make the final clinical ruling.

## Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **API Configuration**:
   Create a `config.json` file in the root directory (you can copy `config.example.json`):
   ```json
   {
       "GEMINI_API_KEY": "your_actual_api_key_here"
   }
   ```

3. **Download the Dataset**:
   Fetch the `AGBonnet/augmented-clinical-notes` dataset from HuggingFace to generate the `data/dataset.jsonl` file:
   ```bash
   python data/loader.py
   ```

## Running the Demo

The demo script runs three fixed triage scenarios directly through the orchestrator, followed by pulling a random patient clinical note from the dataset to be extracted and triaged.

```bash
python src/demo.py
```
