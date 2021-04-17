## Motivation

The project clones a few popular open-source repositories, and counts the
variable names.

## Setup

Create a virtual environment: `python -m venv env`. Activate it with
`source env/bin/activate`. Then, `pip install -r requirements.txt`.

Run `python process.py` to clone and process the repositories yourself. Once
finished, it'll store the data in `stats.pkl`, and you can use `analysis.py`
to poke around.
