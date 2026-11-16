"""Compute descriptors and Lipinski flags; no external ADMET predictions."""
import argparse,json
from rdkit import Chem
from rdkit.Chem import Descriptors,Crippen,Lipinski,rdMolDescriptors
def main():
 p=argparse.ArgumentParser();p.add_argument('smiles');a=p.parse_args();m=Chem.MolFromSmiles(a.smiles)
 if m is None: raise SystemExit('Invalid SMILES')
 x={'mw':Descriptors.MolWt(m),'logp':Crippen.MolLogP(m),'tpsa':rdMolDescriptors.CalcTPSA(m),'hbd':Lipinski.NumHDonors(m),'hba':Lipinski.NumHAcceptors(m),'rotatable_bonds':Lipinski.NumRotatableBonds(m)}
 violations=sum([x['mw']>500,x['logp']>5,x['hbd']>5,x['hba']>10]);x['lipinski_violations']=violations;x['lipinski_pass']=violations<=1
 print(json.dumps(x,indent=2));print('GI/BBB/CYP/toxicity predictions: NOT COMPUTED')
if __name__=='__main__':main()
