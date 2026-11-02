# Course RDF Validation Pipeline

A small Python project that builds a course knowledge graph, validates course data against SHACL rules, and queries the graph with SPARQL.

The pipeline demonstrates how to catch invalid data before passing it on to a query or another processing step.

## How it works

1. **Build an RDF graph** from the sample course data in `main.py`.
2. **Validate the graph** against the constraints in `rules.shacl`.
3. **Run a SPARQL query** from `extract.rq` only if the graph passes validation.

The SHACL rules require each course's credits to be an integer between 1 and 4, inclusive. If the graph fails validation, the script prints the validation report and stops before querying.

## Project files

| File | Purpose |
| --- | --- |
| `main.py` | Builds the RDF graph, runs SHACL validation, and conditionally runs the SPARQL query. |
| `rules.shacl` | Defines the SHACL constraints for course data. |
| `extract.rq` | Selects course names and credits from the graph. |

## Requirements

- Python 3
- `rdflib`
- `pyshacl`

## Setup

From the project directory, create and activate a virtual environment.

### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Windows Command Prompt

```bat
py -m venv .venv
.venv\Scripts\activate.bat
```

### macOS or Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Then install the dependencies:

```bash
python -m pip install rdflib pyshacl
```

## Run

Run the script from the directory containing `main.py`, `rules.shacl`, and `extract.rq`. The script reads the SHACL and SPARQL files using relative paths.

```bash
python main.py
```

If the data conforms to the SHACL rules, the script prints the query results. If it does not, it prints the validation report and halts before the query step.

## Sample validation behavior

The sample data in `main.py` is valid: both courses have integer credits within the allowed range, so the pipeline passes validation and reaches the SPARQL query.

To see the validation gate halt the pipeline, change a course's credits in `main.py` to an invalid value, for example a string:

```python
"ECE554_Embedded_ML": {"credits": "Three"}
```

or an integer outside the allowed range:

```python
"ECE554_Embedded_ML": {"credits": 5}
```

The script then prints `CRITICAL FAILURE: Pipeline Halted` along with the SHACL validation report, and does not run the query.
## Example output

With valid course data and a valid SPARQL file, output includes the validation and query stages, followed by results similar to:

```text
--- RUNNING PIPELINE GATE 1: SHACL AUDIT ---
Audit Passed! Opening query file...

--- RUNNING PIPELINE GATE 2: SPARQL ---
Valid Record: AIT626_NLP_Theory | Credits: 3
Valid Record: ECE554_Embedded_ML | Credits: 3
```

## License

No license has been specified yet.