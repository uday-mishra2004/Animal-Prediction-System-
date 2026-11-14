# Wildlife Insights & Detection Demo
A runnable Python portfolio starter using NumPy, Pandas, scikit-learn, Streamlit and optional MySQL.
**This is a new demonstration project, not an upgrade of an inspected existing repository.**
All included observations are synthetic. No real-world wildlife prediction claims are supported.

## Run in VS Code (Windows PowerShell)
Extract this folder, open it in VS Code, open Terminal, then run:
```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m src.train
.\.venv\Scripts\python.exe -m streamlit run app.py
```
Using the environment's Python directly avoids PowerShell activation-policy problems.
For macOS/Linux replace `.\.venv\Scripts\python.exe` with `.venv/bin/python`.
Training generates demo CSV, fits models and writes reports. Open the localhost URL Streamlit prints.

## Checks
```powershell
.\.venv\Scripts\python.exe -m pytest -q
```
Features: strict survey validation, data profiling, site-grouped evaluation, dummy baseline,
logistic regression and random forest comparison, saved fitted pipeline, validated prediction inputs,
interactive analytics, optional geographic view, and model methodology.
Metrics are computed by training, never hardcoded.

## Real CSV
Read data/README.md first. Only compatible structured surveys with explicit outcomes are supported.
```powershell
.\.venv\Scripts\python.exe -m src.train --csv "path/to/surveys.csv" --confirm-survey-labels
```
This flag is your acknowledgement, not automatic verification of label validity.
The command replaces the demo model; retrain without arguments to return to demo mode.
Do not claim true presence, absence, population change or behaviour from this model.

## Optional MySQL
Install and start MySQL separately. Create a database using your administrator account:
```sql
CREATE DATABASE wildlife_db CHARACTER SET utf8mb4;
```
Create a local database user with access to that database, copy `.env.example` to `.env`, and fill in local credentials.
Never commit `.env`. Then run:
```powershell
.\.venv\Scripts\python.exe -m src.database
```
Species, sites and observations have keys and references. Imports are transactional and skip existing record IDs;
changed content under the same ID is NOT updated automatically. Review conflicts before re-importing.
Dashboard does not require MySQL or connect to it: SQL analytics are a separate optional workflow.
Queries in sql/analytics.sql target MySQL 8+. No database integration has been verified in this delivery environment.

## Architecture
CSV → validation → profile/analytics → training-site CV → final holdout → saved pipeline → Streamlit.
Validated CSV → optional MySQL → SQL analytics.

## Troubleshooting
Missing model: run training first. Missing packages: install requirements using the same Python executable.
Database error: check MySQL service, database/user permissions and .env locally; do not share passwords.
Unsupported CSV: inspect the required schema and source labels; do not fabricate missing fields.
Never load untrusted joblib models.

## Portfolio use
Describe this version as a synthetic-data prototype. Replace with licensed, justified real survey data,
re-evaluate, and document actual results before presenting it as a wildlife study.
Do not list optional MySQL as verified until you run it. No deployment has been performed.
See reports/verification.md for actual delivered checks and docs/roadmap.md for the next 14 days.

## Windows shortcut
Double-click run_windows.bat after installing Python (with the Python launcher). It creates the environment, installs dependencies, retrains the synthetic demo and starts Streamlit. First run needs internet. For reproducibility, requirements-tested.txt records tested direct versions; requirements.txt provides compatible ranges. Use Python 3.11 or 3.12.
