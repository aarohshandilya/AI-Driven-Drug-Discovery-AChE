# Machine Learning-Assisted Virtual Screening and Molecular Docking of Potential Acetylcholinesterase Inhibitors for Alzheimer's Disease

**Independent Computational Research Project · Aaroh Shandilya · 2026**  
**Designed and developed by Aaroh Shandilya | 2026**

## Abstract

This project implements an evidence-aware workflow for investigating acetylcholinesterase (AChE) inhibitors using curated bioactivity records, molecular features, scaffold-based machine-learning evaluation, structure-based docking, and ADMET resources. The software can retrieve ChEMBL activity records and prepare a reproducible classification dataset. At the time of writing, no dataset has been retrieved, no model has been executed, and no docking or external ADMET prediction has been performed. Consequently, no empirical performance or candidate result is reported. Outputs, when generated, are computational hypotheses that require independent experimental validation.

## Introduction and literature context

Alzheimer's disease is a progressive neurodegenerative disorder. The cholinergic hypothesis motivated symptomatic treatments that inhibit AChE and increase acetylcholine availability. AChE is a validated molecular target, while computational screening offers a way to organize candidate hypotheses. Predictive modeling can be confounded by assay differences, chemical-series bias, and leakage between close analogues. Docking scores are approximations and ADMET predictors have domain limits.

## Objectives and research question

Can machine learning models trained on experimentally reported AChE inhibitor data identify compounds with promising predicted binding interactions and pharmacokinetic properties? Objectives are to retrieve and curate activity records, compute molecular features, evaluate classifiers with scaffold separation, specify a donepezil redocking protocol using PDB 4EY7, and document ADMET assessment without conflating predictions with measurements.

## Materials and methods

### Dataset

The acquisition script queries ChEMBL target CHEMBL220 for IC50 activity records. Its CSV preserves activity, assay, document, target, relation, units, structure and molecule identifiers when present. It is a live source extract, not a curated dataset. PubChem identifiers and canonical structures may be used for library enrichment, while retaining source mapping. Data retrieval date and API response should be recorded for each analysis.

### Curation and molecular features

The preparation script accepts exact IC50 values in nM, μM or M, converts to molar units, calculates pIC50 = −log10(IC50 [M]), canonicalizes valid RDKit structures, and computes 1024-bit Morgan fingerprints (radius 2), molecular weight, calculated LogP, TPSA, H-bond donors/acceptors and rotatable bonds. The binary threshold pIC50 ≥ 6 is an operational choice, not a universal activity boundary. Manual review should address assay confidence, assay type, organism, relation qualifiers, replicate conflicts, duplicates, salts, and standardized units before treating rows as labels.

### Machine learning

Random Forest and RBF-kernel SVM models are implemented. A Bemis–Murcko scaffold group split reserves a test subset; grouped cross-validation and grid search operate only on the training portion. Class weights address imbalance. Test metrics include accuracy, precision, recall, F1, ROC-AUC, PR-AUC and confusion matrix. These metrics are absent until the script is run. Applicability-domain assessment is recommended using training-set fingerprint similarity; predictions outside the observed chemistry domain should be treated cautiously. The current site reports no model outputs.

### Docking and ADMET

PDB 4EY7 is the human AChE structure reference; donepezil is the crystallographic control. The documented protocol prepares the receptor and ligand, defines a search box from the bound ligand, redocks, checks pose RMSD, and then docks shortlisted compounds. Vina score is a pose-ranking estimate, not biological potency. Local ADMET code computes descriptors and Lipinski rule flags only. GI absorption, BBB, CYP and toxicity are external predictions that must carry tool/source/version provenance and must not be presented as experimental or definitive safety evidence.

## Results

No data acquisition, model run, docking, or ADMET service call has occurred in the delivered workspace. Dataset statistics, performance metrics, candidate rankings and docking scores are therefore not available. This is an explicit execution status, not a negative experimental result.

## Discussion

The implemented workflow is intended to make data provenance and evaluation boundaries visible. Any future ranking will depend on the selected assay subset and curation decisions. Scaffold separation is more demanding than random splitting but may still give optimistic estimates when scaffold groups are insufficiently diverse. Docking and ADMET outputs can help triage experiments but cannot establish binding, exposure, safety, or treatment effect.

## Limitations

Assay heterogeneity, sparse scaffolds, class imbalance, uncertain activity labels, molecular representation limits, scaffold split variance, model domain shift, approximate receptor/ligand preparation, docking scoring limitations, external ADMET uncertainty, and the absence of experimental validation limit interpretation.

## Conclusion

This repository provides an executable foundation for AChE inhibitor hypothesis prioritization. A scientific conclusion about predictive performance or candidate quality requires retrieval, curation, execution, transparent reporting, and ultimately experimental follow-up. No therapeutic claim is made.

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

**Designed and developed by Aaroh Shandilya | 2026**
