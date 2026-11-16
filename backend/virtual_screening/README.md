# Virtual screening

Model scores are prioritization hypotheses. First obtain an explicitly documented compound library, standardize it using `prepare_dataset.py`, and apply an applicability-domain check (e.g. nearest-neighbor fingerprint similarity to training compounds). Do not interpret low similarity candidates as reliable predictions. See `../../docs/DOCKING.md` for structure-based follow-up.
