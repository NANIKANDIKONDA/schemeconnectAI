# SchemeConnect AI

An AI-powered Government Scheme Discovery and Eligibility Platform.

## Project Structure

- `backend/models`: Contains the data models for Citizen Profile and Schemes.
- `backend/data`: Contains the sample schemes database (`schemes.json`).
- `backend/eligibility`: Contains the deterministic rule-based eligibility engine.
- `backend/services`: Contains logic for filtering and ranking the schemes based on matches.
- `backend/tests`: Contains pytest cases to verify eligibility logic.

## Setup

1. Create and activate a virtual environment (optional but recommended).
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the backend pipeline:
   ```bash
   python backend/main.py
   ```
4. Run tests:
   ```bash
   pytest backend/tests/
   ```
