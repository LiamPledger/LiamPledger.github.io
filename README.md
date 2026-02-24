# Liam Pledger Academic Website

This repository contains:

- `site/`: static frontend deployed to GitHub Pages.
- `api/`: Python inference API for the two drift-capacity models.

## Repository Structure

```text
.
|-- .github/
|   `-- workflows/
|       `-- deploy-pages.yml
|-- api/
|   |-- main.py
|   |-- requirements.txt
|   `-- models/
|       |-- column/
|       `-- wall/
|-- scripts/
|   |-- set-custom-domain.ps1
|   `-- start-model-api.ps1
`-- site/
    |-- index.html
    |-- about.html
    |-- publications.html
    |-- model-column.html
    |-- model-wall.html
    |-- resources.html
    `-- assets/
```

## Exact Colab Model Requirement

For identical results to Colab, place the exact exported model files in:

- `api/models/column/pretrained_model.pkl` (or `model.txt`)
- `api/models/wall/pretrained_model.pkl` (or `model.txt`)

Without these files, the API cannot serve exact Colab predictions.

## Run Locally

1. Start the model API:

```powershell
.\scripts\start-model-api.ps1
```

2. Serve the site locally (separate terminal):

```powershell
python -m http.server 8080
```

3. Open:

- Website: `http://localhost:8080/site/`
- API health: `http://127.0.0.1:8000/health`

## Deploy

- GitHub Pages deploys only `site/` via `.github/workflows/deploy-pages.yml`.
- The Python API must be deployed separately (for example Render/Railway/VM).
- Set `window.MODEL_API_BASE` in `site/assets/js/model-api-config.js`:

```javascript
window.MODEL_API_BASE = "https://your-api-domain.example";
```

Then commit and push.

## Push Updates to GitHub

```powershell
git add .
git commit -m "Update website/API"
git push
```
