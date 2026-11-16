"""Download the public Kaggle human AChE/ChEMBL dataset into ignored raw data."""
from pathlib import Path
from zipfile import ZipFile
import io
import requests

REF='gauravan/human-acetylcholinesterase-dataset-from-chembl'
URL=f'https://www.kaggle.com/api/v1/datasets/download/{REF}'
EXPECTED={'AChE_Bioactivity_data_1.csv','AChE_Bioactivity_data_2.csv'}

def main():
    response=requests.get(URL,timeout=120);response.raise_for_status()
    archive=ZipFile(io.BytesIO(response.content));names={Path(n).name for n in archive.namelist() if not n.endswith('/')}
    if not EXPECTED.issubset(names): raise SystemExit(f'Unexpected Kaggle archive contents: {sorted(names)}')
    out=Path('data/raw/kaggle_ache_dataset');out.mkdir(parents=True,exist_ok=True)
    for name in EXPECTED:
        (out/name).write_bytes(archive.read(next(n for n in archive.namelist() if Path(n).name==name)))
    print(f'Downloaded {sorted(EXPECTED)} from Kaggle dataset {REF} to {out}. Check current license terms before reuse or redistribution.')
if __name__=='__main__': main()
