# Technical complexity measure

Python implementation of the technical complexity measure described in
the main README. The measure quantifies how specialised a policy
document is, using WordNet synsets as a proxy for vocabulary
specialisation.

## Files

- `compute_technical_complexity.py` — Main script. Provides
  `complexity_score()` for single documents and `complexity_score_batch()`
  for folders of documents.
- `requirements.txt` — Python dependencies.

## Installation

```bash
pip install -r requirements.txt
```

The NLTK resources (`punkt`, `wordnet`, `stopwords`) will be downloaded
automatically on first use. To download them in advance:

```bash
python -m nltk.downloader punkt wordnet stopwords
```

## Usage

**From the command line**, on a single document or a folder of `.txt` files:

```bash
python compute_technical_complexity.py path/to/document.txt
python compute_technical_complexity.py path/to/folder/
```

**From Python**:

```python
from compute_technical_complexity import complexity_score, complexity_score_batch

# Single document
ratio = complexity_score("path/to/document.txt")
print(f"Complexity ratio: {ratio:.3f}")

# Folder of documents
results = complexity_score_batch("path/to/folder")
for filename, ratio in results.items():
    print(f"{filename}: {ratio:.3f}")
```

A lower ratio indicates higher technical complexity. See the main
project README for the full methodology.
