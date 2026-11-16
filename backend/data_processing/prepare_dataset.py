"""Standardize structures and derive an explicitly operational IC50 label."""
import argparse
import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors, Crippen, Lipinski, rdMolDescriptors
from rdkit.Chem.Scaffolds import MurckoScaffold
from rdkit.Chem.MolStandardize import rdMolStandardize
from rdkit.Chem.rdFingerprintGenerator import GetMorganGenerator

def main():
    p=argparse.ArgumentParser(); p.add_argument("--input",default="data/raw/kaggle_ache_dataset/AChE_Bioactivity_data_1.csv"); p.add_argument("--out",default="data/processed/ache_curated.csv"); a=p.parse_args()
    df=pd.read_csv(a.input); rows=[]; fpgen=GetMorganGenerator(radius=2,fpSize=1024)
    for _,r in df.iterrows():
        if r.get("target_chembl_id")!="CHEMBL220" or r.get("target_organism")!="Homo sapiens": continue
        if r.get("assay_type")!="B" or pd.notna(r.get("data_validity_comment")): continue
        if r.get("standard_type")!="IC50" or r.get("standard_relation")!="=" or r.get("standard_units") not in ("nM","uM","µM","M"):
            continue
        try: value=float(r["standard_value"])
        except (ValueError,TypeError): continue
        molar=value*{"nM":1e-9,"uM":1e-6,"µM":1e-6,"M":1}[r["standard_units"]]
        if molar<=0 or pd.isna(r.get("canonical_smiles")): continue
        mol=Chem.MolFromSmiles(r["canonical_smiles"])
        if mol is None: continue
        mol=rdMolStandardize.Cleanup(mol)
        mol=rdMolStandardize.FragmentParent(mol)
        mol=rdMolStandardize.Uncharger().uncharge(mol)
        Chem.SanitizeMol(mol)
        smi=Chem.MolToSmiles(mol,canonical=True)
        fp=fpgen.GetFingerprint(mol)
        d={"smiles":smi,"pIC50":-np.log10(molar),"active":int(-np.log10(molar)>=6),"scaffold":Chem.MolToSmiles(MurckoScaffold.GetScaffoldForMol(mol)),
           "mw":Descriptors.MolWt(mol),"logp":Crippen.MolLogP(mol),"tpsa":rdMolDescriptors.CalcTPSA(mol),"hbd":Lipinski.NumHDonors(mol),"hba":Lipinski.NumHAcceptors(mol),"rotatable_bonds":Lipinski.NumRotatableBonds(mol)}
        d.update({f"fp_{i}":int(x) for i,x in enumerate(fp)}); rows.append(d)
    out=pd.DataFrame(rows).drop_duplicates(["smiles","pIC50"])
    if out.empty: raise SystemExit("No eligible exact IC50 rows; check source schema and filters.")
    import os; os.makedirs(os.path.dirname(a.out),exist_ok=True); out.to_csv(a.out,index=False)
    print(f"Prepared {len(out)} rows. Threshold: pIC50 >= 6. Inspect assay heterogeneity before interpretation.")
if __name__=="__main__": main()
