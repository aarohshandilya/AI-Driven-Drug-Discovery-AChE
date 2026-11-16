# Docking workflow (pending execution)

No docking software or results are bundled. Example setup assumes a separate Python environment with RDKit, Meeko and AutoDock Vina installed; Open Babel/PyMOL can support format conversion and inspection. Check each tool's official documentation for current installation requirements.

1. Download PDB 4EY7 from RCSB and record retrieval date. Inspect chain, waters, ions, missing atoms, alternate conformations, and the co-crystallized donepezil ligand. Preserve an untouched source structure.
2. Prepare receptor: choose the biologically appropriate chain, resolve missing atoms/protonation consistently, and convert using a documented preparation method. Save preparation settings and software versions.
3. Extract co-crystallized donepezil, generate protonation/tautomer state and prepare PDBQT with Meeko. Use its bound coordinates to center the search box with margin sufficient for ligand motion; document center and dimensions in `docking/config.txt`.
4. Redock donepezil into the prepared receptor with Vina. Compare best relevant predicted pose with crystallographic ligand after atom mapping/alignment; report heavy-atom RMSD and mapping method. A low RMSD is a protocol check, not proof of prospective accuracy.
5. Prepare candidate ligands consistently. Run Vina with fixed versions and random seeds where supported; preserve logs and poses. Review protonation, stereochemistry, strain and pocket contacts.
6. Use PyMOL or other tools to inspect hydrogen bonds, hydrophobic contacts and aromatic interactions. Avoid presenting inferred contacts as experimentally verified.

Vina scores are not measured binding free energies or potency. More negative scores alone do not establish stronger inhibition. Report failed preparations and pose validation alongside any scores. See [AutoDock Vina](https://autodock-vina.readthedocs.io/), [Meeko](https://meeko.readthedocs.io/) and [RCSB 4EY7](https://www.rcsb.org/structure/4EY7).
