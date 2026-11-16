# Kaggle AChE dataset provenance

**Dataset:** [Human acetylcholinesterase Dataset from ChEMBL](https://www.kaggle.com/datasets/gauravan/human-acetylcholinesterase-dataset-from-chembl)  
**Uploader:** Gauravan  
**Retrieval date:** 2026-11-16  
**Declared upstream source:** ChEMBL; the CSV records identify target CHEMBL220 and Homo sapiens.  
**Kaggle license field:** Unknown.

The two Kaggle files are downloaded locally by `backend/data_processing/fetch_kaggle_dataset.py` to `data/raw/kaggle_ache_dataset/`. Raw data are excluded from Git because the Kaggle license is unknown. Check the Kaggle dataset page and applicable source terms before redistribution or further reuse. The data are a third-party snapshot compiled from ChEMBL, not a newly performed experiment or a live ChEMBL query.

The analysis used `AChE_Bioactivity_data_1.csv` (15,542 rows). Curation selected human target CHEMBL220, exact IC50 values in nM with SMILES, binding assay type B, positive values, and blank ChEMBL data-validity comments. RDKit cleanup, largest-fragment selection, uncharging, canonical SMILES, and duplicate `(SMILES, pIC50)` removal produced the reported analysis table. `backend/data_processing/build_dashboard_summary.py` records actual counts and metrics for the website.
