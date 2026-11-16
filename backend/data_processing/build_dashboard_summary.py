"""Export a compact provenance and metric snapshot for the static website."""
import json
from pathlib import Path
import pandas as pd

def main():
    raw=Path('data/raw/kaggle_ache_dataset/AChE_Bioactivity_data_1.csv')
    curated=Path('data/processed/ache_curated.csv')
    metrics=Path('results/metrics.json')
    if not all(p.exists() for p in (raw,curated,metrics)):
        raise SystemExit('Run Kaggle acquisition, curation, and model training first.')
    source=pd.read_csv(raw, usecols=['target_chembl_id','target_organism','standard_type','standard_relation','standard_units','canonical_smiles','data_validity_comment','assay_type','standard_value'])
    selection=(source.target_chembl_id.eq('CHEMBL220') & source.target_organism.eq('Homo sapiens') & source.standard_type.eq('IC50') & source.standard_relation.eq('=') & source.standard_units.eq('nM') & source.canonical_smiles.notna())
    base=source[selection]
    eligible=base[(base.assay_type=='B') & (base.data_validity_comment.isna() | base.data_validity_comment.eq('')) & pd.to_numeric(base.standard_value,errors='coerce').gt(0)]
    data=pd.read_csv(curated)
    payload={
      'source':{'name':'Human acetylcholinesterase Dataset from ChEMBL','publisher':'Gauravan on Kaggle','url':'https://www.kaggle.com/datasets/gauravan/human-acetylcholinesterase-dataset-from-chembl','original_source':'ChEMBL target CHEMBL220 · Homo sapiens','retrieved':'2026-11-16','license':'Unknown on Kaggle; raw files are not redistributed'},
      'curation':{'raw_records':int(len(source)),'exact_ic50_nM_with_smiles':int(len(base)),'binding_assay_unflagged_positive_records':int(len(eligible)),'curated_records':int(len(data)),'unique_compounds':int(data.smiles.nunique()),'unique_scaffolds':int(data.scaffold.nunique()),'active_records':int(data.active.sum()),'inactive_records':int((data.active==0).sum()),'threshold':'pIC50 ≥ 6; IC50 ≤ 1 μM'},
      'validation':{'split':'Bemis–Murcko scaffold-group holdout','train_n':int(json.loads(metrics.read_text())['RandomForest']['train_n']),'test_n':int(json.loads(metrics.read_text())['RandomForest']['test_n']),'seed':42,'tuning':'5-fold GroupKFold grid search on training data; average precision selection','models':json.loads(metrics.read_text())},
      'caveat':'Single scaffold-group holdout evaluation; estimates depend on this dataset, curation policy and split. Predictions are hypotheses, not therapeutic efficacy evidence.'}
    out=Path('frontend/src/data/research_results.json');out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(payload,indent=2),encoding='utf-8')
    print(f'Wrote {out}: {len(data)} curated rows and {len(payload["validation"]["models"])} evaluated models.')
if __name__=='__main__': main()
