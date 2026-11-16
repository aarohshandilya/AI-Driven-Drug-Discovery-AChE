# AI-Driven Identification of Potential Acetylcholinesterase Inhibitors

Independent computational research project by **Aaroh Shandilya** · 2026.

An evidence-aware research website and reproducible pipeline for exploring experimentally reported AChE activity data using molecular descriptors, machine learning, docking, and ADMET resources. **All computational predictions are preliminary hypotheses and do not establish therapeutic efficacy.** This repository contains no fabricated dataset, metrics, docking scores, or ADMET outputs.

> Designed and developed by Aaroh Shandilya | 2026

## Website

Responsive React + Vite site. Run `npm install` and `npm run dev`; build with `npm run build`. GitHub Pages deployment is configured in `.github/workflows/pages.yml` for pushes to `main` once the repository is published and Pages is enabled for GitHub Actions.

## Research pipeline

1. `python -m pip install -r requirements.txt`
2. `python backend/data_processing/fetch_chembl.py` retrieves current ChEMBL human AChE (CHEMBL220) IC50 records to `data/raw/`.
3. Review source assay metadata and curation policy; then run `python backend/data_processing/prepare_dataset.py`.
4. Run `python backend/machine_learning/train_models.py` for Random Forest and SVM, scaffold-group holdout, train-only grouped cross-validation/grid search, class weighting, and accuracy/precision/recall/F1/ROC-AUC/PR-AUC/confusion matrices.
5. `python backend/admet/descriptors.py 'SMILES'` computes RDKit descriptors and Lipinski flags. GI, BBB, CYP, and toxicity predictions require external prediction services and are not included as fabricated values.
6. Follow [`docs/DOCKING.md`](docs/DOCKING.md) for 4EY7/donepezil redocking and Vina setup. Docking tools are optional external dependencies.

The binary label uses pIC50 = −log10(IC50 in molar units), active at pIC50 ≥ 6. This is an operational threshold. Assay type, relation, units, duplicate structures, assay heterogeneity, and provenance need review. Scaffold splitting reduces close-analogue leakage but does not ensure broad generalization. Inspect applicability domain before prioritizing predictions.

## Repository map

- `frontend/` — research website
- `backend/` — data acquisition, curation, ML and descriptor modules
- `data/` — generated local raw/processed data (not committed)
- `docking/` — docking configuration and instructions
- `docs/` — methods, docking and report
- `.github/workflows/` — Pages build and deployment

## Deployment

GitHub CLI (`gh`) is not installed in the initial environment, and no remote is configured. After authenticating/installing GitHub CLI, create and push the repository using the commands in `docs/DEPLOYMENT.md`. The workflow deploys Pages on a push to `main`; enable Pages with GitHub Actions in repository settings if needed. No repository URL or live URL is claimed until deployment is verified.

## Attribution

Designed and developed by Aaroh Shandilya | 2026. No institutional affiliation, supervisor endorsement, publication acceptance, or experimental validation is claimed.
