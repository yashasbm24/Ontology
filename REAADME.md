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

The sample data currently includes a course with `"Three"` as its credits value. This is a string, not an integer, so it violates the SHACL constraints and causes the pipeline to stop at validation.

To let the sample reach the SPARQL query stage, change that course's credits value in `main.py` to an integer from 1 to 4, for example:

```python
"ECE554_Embedded_ML": {"credits": 3}
```

Also ensure `extract.rq` contains only SPARQL: remove any `%%writefile extract.rq` line if present. That line is a Jupyter notebook magic command, not part of a SPARQL query file.

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