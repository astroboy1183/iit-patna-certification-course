"""Entry point for the call-transcript QA pipeline.

    python main.py                          # all transcripts -> data/output.xlsx
    python main.py --output results.csv     # save somewhere else
    python main.py --transcript "..."       # one transcript, printed

The pipeline itself lives in src/; this file only starts it.
"""

import os
from pathlib import Path

# config/config.json, .env and data/ are read with paths relative to the project folder,
# so work from here no matter which folder the command was started in.
os.chdir(Path(__file__).resolve().parent)

from src.pipeline.inference import main  # noqa: E402

if __name__ == "__main__":
    main()
