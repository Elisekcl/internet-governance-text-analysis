"""
Compute technical complexity of policy documents using WordNet synsets.

This module operationalises 'technical complexity' as the ratio of total
content tokens to specialised tokens, where specialised tokens are words
with fewer than two synsets in WordNet. The intuition is that common
words have many synonyms while technical or domain-specific terms have
few or none.

A lower ratio indicates higher technical complexity (more specialised
vocabulary as a proportion of total content words).

Developed for:
    Antoine, E. (2025). Lobbying global venues: Sitting in or speaking out?
    Governance, 38(2), e12903. https://doi.org/10.1111/gove.12903
"""

import argparse
import string
from pathlib import Path

import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn


def _ensure_nltk_resources():
    """Download NLTK resources required by the measure if not already present."""
    for resource, path in [
        ("punkt", "tokenizers/punkt"),
        ("wordnet", "corpora/wordnet"),
        ("stopwords", "corpora/stopwords"),
    ]:
        try:
            nltk.data.find(path)
        except LookupError:
            nltk.download(resource, quiet=True)


def complexity_score(filepath):
    """
    Compute the technical complexity ratio for a single document.

    The measure is defined as:

        ratio = total content tokens / tokens with fewer than 2 WordNet synsets

    Lower values indicate higher technical complexity.

    Parameters
    ----------
    filepath : str or Path
        Path to a plain-text document.

    Returns
    -------
    float
        The technical complexity ratio.

    Raises
    ------
    ValueError
        If the document contains no content tokens, or no specialised
        tokens (which would produce a division by zero).
    """
    _ensure_nltk_resources()

    # Read the document.
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    # Tokenise, then strip punctuation and stopwords to keep only
    # content words. Note: stopwords.words() with no language argument
    # filters against stopwords across all available languages, matching
    # the implementation used in the original analysis.
    tokens = word_tokenize(text)
    punctuation = set(string.punctuation)
    stop_words = set(stopwords.words())

    content_tokens = [
        w for w in tokens
        if w not in punctuation and w not in stop_words
    ]

    if not content_tokens:
        raise ValueError(f"No content tokens found in {filepath}.")

    # Identify specialised tokens: words with fewer than 2 WordNet synsets.
    specialised_tokens = [w for w in content_tokens if len(wn.synsets(w)) < 2]

    if not specialised_tokens:
        raise ValueError(f"No specialised tokens found in {filepath}.")

    return len(content_tokens) / len(specialised_tokens)


def complexity_score_batch(folder):
    """
    Compute the technical complexity ratio for every .txt file in a folder.

    Parameters
    ----------
    folder : str or Path
        Path to a folder containing plain-text documents.

    Returns
    -------
    dict
        A mapping from filename to complexity ratio. Documents that
        cannot be scored (e.g., empty files) are skipped with a warning.
    """
    folder = Path(folder)
    if not folder.is_dir():
        raise ValueError(f"{folder} is not a directory.")

    results = {}
    for filepath in sorted(folder.glob("*.txt")):
        try:
            results[filepath.name] = complexity_score(filepath)
        except ValueError as e:
            print(f"Skipping {filepath.name}: {e}")

    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Compute the technical complexity ratio for a policy document "
            "or a folder of documents. Lower values indicate higher "
            "technical complexity."
        )
    )
    parser.add_argument(
        "path",
        help="Path to a .txt file or to a folder containing .txt files.",
    )
    args = parser.parse_args()

    target = Path(args.path)

    if target.is_dir():
        results = complexity_score_batch(target)
        for filename, ratio in results.items():
            print(f"{filename}: {ratio:.3f}")
    else:
        ratio = complexity_score(target)
        print(f"{target.name}: {ratio:.3f}")
