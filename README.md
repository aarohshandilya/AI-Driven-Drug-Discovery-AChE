# AI-Driven Identification of Potential Acetylcholinesterase Inhibitors

Independent computational research project by **Aaroh Shandilya** · 2026.

An evidence-aware research website and reproducible pipeline for exploring experimentally reported AChE activity data using molecular descriptors, machine learning, docking, and ADMET resources. **All computational predictions are preliminary hypotheses and do not establish therapeutic efficacy.** This repository contains no fabricated dataset, metrics, docking scores, or ADMET outputs.

> Designed and developed by Aaroh Shandilya | 2026

## Website

Responsive React + Vite site. Run `npm install` and `npm run dev`; build with `npm run build`. GitHub Pages deployment is configured in `.github/workflows/pages.yml` for pushes to `main` once the repository is published and Pages is enabled for GitHub Actions.

## Research pipeline

1. `python -m pip install -r requirements.txt`
2. `python backend/data_processing/fetch_kaggle_dataset.py` downloads the Kaggle-hosted human AChE dataset to ignored `data/raw/` files. The Kaggle license field is unknown; see [`docs/KAGGLE_DATA.md`](docs/KAGGLE_DATA.md) and do not redistribute the raw files.
3. `python backend/data_processing/prepare_dataset.py` selects human CHEMBL220 exact IC50 binding-assay rows, nM units, valid ChEMBL flags, cleans structures with RDKit, and writes the processed table locally.
4. `python backend/machine_learning/train_models.py` trains Random Forest and SVM using scaffold-group holdout, train-only grouped CV/grid search, class weights, and common classification metrics.
5. `python backend/data_processing/build_dashboard_summary.py` writes the compact, provenance-labeled results snapshot consumed by the website.
6. `python backend/admet/descriptors.py 'SMILES'` computes RDKit descriptors and Lipinski flags. GI, BBB, CYP, and toxicity predictions require external prediction services and are not included as fabricated values.
7. Follow [`docs/DOCKING.md`](docs/DOCKING.md) for 4EY7/donepezil redocking and Vina setup. Docking tools are optional external dependencies.

The binary label uses pIC50 = −log10(IC50 in molar units), active at pIC50 ≥ 6. This is an operational threshold. The current snapshot yielded 5,196 processed records from 15,542 raw rows; 4,090/1,106 records were used in the training/held-out scaffold split. Current model metrics and caveats appear in the website and [`docs/REPORT.md`](docs/REPORT.md). Metrics are a single split and should not be treated as prospective performance guarantees. Inspect applicability domain before prioritizing predictions.

## Repository map

- `frontend/` — research website
- `backend/` — data acquisition, curation, ML and descriptor modules
- `data/` — Kaggle raw and RDKit-processed records (not committed)
- `docking/` — docking configuration and instructions
- `docs/` — methods, docking and report
- `.github/workflows/` — Pages build and deployment

## Deployment

GitHub CLI (`gh`) is not installed in the initial environment, and no remote is configured. After authenticating/installing GitHub CLI, create and push the repository using the commands in `docs/DEPLOYMENT.md`. The workflow deploys Pages on a push to `main`; enable Pages with GitHub Actions in repository settings if needed. No repository URL or live URL is claimed until deployment is verified.

## Attribution

Designed and developed by Aaroh Shandilya | 2026. No institutional affiliation, supervisor endorsement, publication acceptance, or experimental validation is claimed.
