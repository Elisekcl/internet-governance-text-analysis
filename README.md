# Tools for Studying Policy Production

A web-scraping and text-analysis pipeline for collecting and analysing
policy discussions in internet governance venues. Originally developed
for the research paper *Lobbying global venues: Sitting in or speaking
out?*, published in *Governance*.

## About this project

The regulation of the internet is shaped in venues that look very different
from traditional policymaking. Venues like the IETF (Internet Engineering
Task Force) operate through technical working groups, open mailing lists,
and informal standards processes. Understanding who participates in these
venues and how technical the rules they produce are matters for questions
about accountability, representation and influence.

This repository contains two components developed for the paper, each
addressing a different side of the policymaking process in these venues:

1. **A web scraper** (R) that collects messages from IETF working group
   mailing list archives, extracting message bodies and senders (in particular
   the email addresses as a way to capture professional affiliations).
   This component is about *who is involved* in the policymaking
   process — identifying participants in discussions that shape the rules,
   beyond formal authorship of the final documents.
3. **A technical complexity measure** (Python) that quantifies how
   specialised a policy document is, using WordNet synsets as a proxy for
   vocabulary specialisation. This component is about *the policy documents
   produced* — characterising their substantive content and the degree of
   technical expertise required to engage with them.

Together they allow researchers to study large corpora of governance
discussions from both angles — the people shaping policy and the policy
itself.

## The technical complexity measure

A central methodological contribution of the paper is operationalising
**technical complexity** of policy documents in a way that is comparable
across texts and avoids relying on hand-coded glossaries of jargon.

The intuition is simple. Common words have many synonyms: *good*, *use*,
*help* all map to multiple WordNet synsets. Specialised vocabulary tends
to have few or no synonyms: terms like *encryption*, *authenticated*,
*hostname*, and *concatenate* appear with one or no general-language
equivalents in WordNet, because they carry domain-specific meaning that
ordinary vocabulary does not capture.

For each document, the measure:

1. Tokenises the text and removes stopwords and punctuation.
2. Counts the number of words with fewer than two WordNet synsets (i.e.,
   highly specialised or domain-specific terms).
3. Computes the ratio of total tokens to specialised tokens.

A lower ratio indicates a higher density of specialised vocabulary, and
therefore a more technically complex document.

The approach is fast, language-aware, fully reproducible, and requires no
manual coding — making it suitable for large corpora of governance
documents across multiple venues.

## Repository structure

```
.
├── README.md
├── scraping/
│   ├── scrape_ietf_archive.R          # Main scraping script
│  
├── complexity_measure/
│   ├── compute_technical_complexity.py # Compute complexity score
│   ├── requirements.txt                # Python dependencies
│  
├── examples/
│   ├── example_document.txt            # Sample IETF document
│   └── example_output.csv              # Example complexity scores
└── LICENSE
```

## Requirements

**Scraping pipeline (R):**
- R ≥ 4.0
- Packages: `rvest`, `XML`, `stringr`, `robotstxt`, `curl`, `reshape2`

**Complexity measure (Python):**
- Python ≥ 3.8
- Packages: `nltk` (with `wordnet` and `stopwords` corpora downloaded)

Install Python dependencies with:

```bash
pip install -r complexity_measure/requirements.txt
python -m nltk.downloader wordnet stopwords punkt
```

## Quick start

**Scrape messages from an IETF working group archive:**

```r
source("scraping/scrape_ietf_archive.R")
# Edit the URL at the top of the script to point at a different working group.
# Output: a CSV of cleaned message metadata and bodies.
```

**Compute technical complexity for a document:**

```python
from complexity_measure.compute_technical_complexity import complexity_score

score = complexity_score("examples/example_document.txt")
print(f"Technical complexity ratio: {score:.2f}")
```

## Example: low vs high complexity policies

Applied to documents from the IETF and W3C corpora, the measure
distinguishes general-audience policy documents from those that are
heavily technical. Two examples in each category:

**Lower technical complexity** — documents discussing privacy and
governance in more general policy language:

- *Privacy Considerations for Internet Protocols*
- *Privacy best practices for web applications*

> "Furthermore, privacy as a legal concept is understood differently in
> different jurisdictions. The guidance provided in this document is
> generic and can be used to inform the design of any protocol to be
> used anywhere in the world, without reference to specific legal
> frameworks."

> "The end user should have enough information about a service and how
> it will use their personal information to make an informed decision
> on whether to share information with that service."

**Higher technical complexity** — documents specifying technical
mechanisms in domain-specific vocabulary:

- *Decentralized identifiers*
- *XML Encryption Requirements*

> "This design eliminates dependence on centralized registries for
> identifiers as well as centralized certificate authorities for key
> management — the standard pattern in hierarchical PKI (public key
> infrastructure)."

> "If the application scenario requires all of the information to be
> encrypted, the whole document is encrypted as an octet sequence.
> This applies to arbitrary data including XML documents."

The first pair uses recognisable policy and legal vocabulary; the
second pair is dense with terms like *PKI*, *octet sequence*,
*decentralized identifiers* that have few or no general-language
synonyms — exactly the difference the measure is designed to capture.

## Ethical scraping

The scraping pipeline uses the `robotstxt` package to verify that
target paths are permitted by the venue's robots.txt before requesting
content. IETF mailing list archives are publicly accessible and intended
for public reference. Researchers using this code on other venues should
check the relevant terms of service and rate-limit requests appropriately.

## Citing this work

If you use this code in your own research, please cite:

> Antoine, E. (2025). Lobbying global venues: Sitting in or speaking out?
> *Governance*, 38(2), e12903. https://doi.org/10.1111/gove.12903

```bibtex
@article{antoine_lobbying_global_venues_2025,
  author  = {Antoine, Elise},
  title   = {Lobbying global venues: Sitting in or speaking out?},
  journal = {Governance},
  year    = {2025},
  volume  = {38},
  number  = {2},
  pages   = {e12903},
  doi     = {10.1111/gove.12903}
}
```

## License

This code is released under the MIT License. See `LICENSE` for details.

