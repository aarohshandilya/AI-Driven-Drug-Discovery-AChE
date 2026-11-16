# Processed data

Generated locally by `backend/data_processing/prepare_dataset.py` from the Kaggle snapshot. Curation keeps human CHEMBL220, exact IC50 in nM, binding assay type B, positive values and blank ChEMBL data-validity comments; RDKit cleanup, largest-fragment selection, uncharging, canonicalization, descriptor/fingerprint calculation and duplicate removal follow. Threshold pIC50 >= 6 is an operational research choice, not a clinical cutoff. The processed data are excluded from Git.
