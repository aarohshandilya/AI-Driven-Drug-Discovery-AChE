# Machine Learning-Assisted Virtual Screening and Molecular Docking of Potential Acetylcholinesterase Inhibitors for Alzheimer's Disease

**Independent Computational Research Project · Aaroh Shandilya · 2026**  
**Designed and developed by Aaroh Shandilya | 2026**

## Abstract

This project implements an evidence-aware workflow for investigating acetylcholinesterase (AChE) inhibitors using curated bioactivity records, molecular features, and scaffold-based machine-learning evaluation, with specified docking and ADMET follow-up. A Kaggle-hosted snapshot of ChEMBL human AChE measurements was retrieved and processed. From 15,542 source rows, the stated curation retained 5,196 activity records. Random Forest and SVM models were tuned on training scaffolds and evaluated on one held-out scaffold split of 1,106 records. Random Forest achieved ROC-AUC 0.898 and PR-AUC 0.907; SVM achieved ROC-AUC 0.876 and PR-AUC 0.884 on that split. No docking or external ADMET prediction has been performed. These model outputs are dataset-specific computational estimates, not candidate efficacy evidence.

## Introduction and literature context

Alzheimer's disease is a progressive neurodegenerative disorder. The cholinergic hypothesis motivated symptomatic treatments that inhibit AChE and increase acetylcholine availability. AChE is a validated molecular target, while computational screening offers a way to organize candidate hypotheses. Predictive modeling can be confounded by assay differences, chemical-series bias, and leakage between close analogues. Docking scores are approximations and ADMET predictors have domain limits.

## Objectives and research question

Can machine learning models trained on experimentally reported AChE inhibitor data identify compounds with promising predicted binding interactions and pharmacokinetic properties? Objectives are to retrieve and curate activity records, compute molecular features, evaluate classifiers with scaffold separation, specify a donepezil redocking protocol using PDB 4EY7, and document ADMET assessment without conflating predictions with measurements.

## Materials and methods

### Dataset

The input was Kaggle's [Human acetylcholinesterase Dataset from ChEMBL](https://www.kaggle.com/datasets/gauravan/human-acetylcholinesterase-dataset-from-chembl), uploaded by Gauravan. Its first CSV has 15,542 rows and includes activity, assay, document, target, relation, units, structure, and molecule identifiers. Records identify human target CHEMBL220. Kaggle's license field is Unknown; the source files and processed compound table are excluded from this repository. See `docs/KAGGLE_DATA.md` for retrieval and provenance. The data are a third-party snapshot and not a live ChEMBL query.

### Curation and molecular features

The analysis selected human CHEMBL220 rows with standard type IC50, exact relation, nM units, and nonmissing canonical SMILES, then retained binding assay type B, positive numeric values, and blank ChEMBL data-validity comments. This yielded 5,705 eligible source records. RDKit Cleanup, largest-fragment selection, uncharging, sanitization, canonicalization, descriptor/fingerprint calculation, and removal of duplicate canonical-SMILES/pIC50 pairs yielded 5,196 records, 4,483 unique structures, and 1,953 Bemis–Murcko scaffolds. The operational threshold pIC50 ≥ 6 produced 2,796 active and 2,400 inactive records. Morgan radius-2 1024-bit fingerprints and molecular weight, calculated LogP, TPSA, H-bond donor/acceptor, and rotatable-bond descriptors were used. These counts are from this Kaggle snapshot and curation code; they are not universal database totals.

### Machine learning

Random Forest and RBF-kernel SVM models were evaluated. GroupShuffleSplit with random seed 42 held out 1,106 records by Bemis–Murcko scaffold; 4,090 records were used for training. Five-fold GroupKFold grid search optimized average precision using only training data. Class weighting was enabled. Reported test metrics are accuracy, precision, recall, F1, ROC-AUC, PR-AUC, and confusion matrices. This is one split; no repeated split or external validation set was evaluated. Applicability-domain assessment is recommended using training-set fingerprint similarity before screening.

### Docking and ADMET

PDB 4EY7 is the human AChE structure reference; donepezil is the crystallographic control. The documented protocol prepares the receptor and ligand, defines a search box from the bound ligand, redocks, checks pose RMSD, and then docks shortlisted compounds. Vina score is a pose-ranking estimate, not biological potency. Local ADMET code computes descriptors and Lipinski rule flags only. GI absorption, BBB, CYP and toxicity are external predictions that must carry tool/source/version provenance and must not be presented as experimental or definitive safety evidence.

## Results

### Held-out scaffold evaluation

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC | PR-AUC |
|---|---:|---:|---:|---:|---:|---:|
| Random Forest | 0.812 | 0.858 | 0.781 | 0.818 | 0.898 | 0.907 |
| RBF SVM | 0.802 | 0.807 | 0.833 | 0.820 | 0.876 | 0.884 |

Random Forest confusion matrix (true labels by rows, predicted labels by columns): `[[431, 77], [131, 467]]`. SVM: `[[389, 119], [100, 498]]`. These are actual outputs from the fixed seed scaffold holdout and the included training script. The dataset has 5,196 curated records; raw data and fitted model artifacts remain local and are not distributed. Docking scores, candidate rankings, and external ADMET predictions have not been generated.

## Discussion

The measured dataset is nearly balanced after the 1 μM operational classification threshold, but that balance reflects the available curated records rather than population prevalence. The observed score difference between classifiers should not be treated as a reliable ranking from one split. Assay and source selection, standardization, duplicate policy, and scaffold diversity influence results. Docking and ADMET outputs may help formulate follow-up experiments but cannot establish binding, exposure, safety, or treatment effect.

## Limitations

The Kaggle dataset's declared license is Unknown, so raw data are not republished; upstream curation and ChEMBL release details are limited. Assay heterogeneity, remaining label uncertainty, molecular representation limits, scaffold split variance, model domain shift, lack of external validation, approximate receptor/ligand preparation, docking scoring limitations, external ADMET uncertainty, and the absence of experimental validation limit interpretation.

## Conclusion

The implemented pipeline and this single scaffold-held-out run provide an initial computational baseline for AChE activity classification. Additional scaffold or temporal validation, careful source harmonization, prospective docking validation, ADMET evaluation, and experimental testing are needed before candidate claims. No therapeutic claim is made.

## References

1. ChEMBL database. European Molecular Biology Laboratory, European Bioinformatics Institute. https://www.ebi.ac.uk/chembl/
2. PubChem. National Center for Biotechnology Information. https://pubchem.ncbi.nlm.nih.gov/
3. RCSB Protein Data Bank, entry 4EY7. https://www.rcsb.org/structure/4EY7
4. Therapeutics Data Commons. https://tdcommons.ai/
5. RDKit documentation. https://www.rdkit.org/docs/
6. AutoDock Vina documentation. https://autodock-vina.readthedocs.io/
7. SwissADME. https://www.swissadme.ch/
8. ProTox 3.0. https://tox.charite.de/protox3/
9. Bemis GW, Murcko MA. The properties of known drugs. 1. Molecular frameworks. J Med Chem. 1996;39(15):2887–2893. doi:10.1021/jm9602928.
10. Gauravan. Human acetylcholinesterase Dataset from ChEMBL. Kaggle dataset. Retrieved 2026-11-16. https://www.kaggle.com/datasets/gauravan/human-acetylcholinesterase-dataset-from-chembl. Kaggle lists the dataset license as Unknown.

**Designed and developed by Aaroh Shandilya | 2026**
