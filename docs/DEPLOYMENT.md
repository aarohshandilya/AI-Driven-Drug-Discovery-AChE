# GitHub Pages deployment

The repository is locally initialized, but the initial environment had no `gh` executable, GitHub authentication, or configured remote. After installing GitHub CLI and authenticating (`gh auth login`), from the repository root run:

```powershell
gh repo create AI-Driven-Drug-Discovery-AChE --public --description "AI-assisted computational drug discovery integrating machine learning, molecular docking, cheminformatics and ADMET profiling for Alzheimer's disease research." --source . --remote origin --push
git branch -M main
git push -u origin main
```

The GitHub Actions workflow builds the Vite site and deploys on pushes to `main`. In repository Settings → Pages, set the source to **GitHub Actions** if not selected. Check the Actions run and Pages deployment before sharing a live URL. The workflow supports a project-site base path derived from the repository name.
