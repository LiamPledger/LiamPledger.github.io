# Liam Pledger Academic Website

This repository contains:

- `site/`: static frontend deployed with GitHub Pages.
- `api/`: Python inference API that loads the exact Colab-trained model artifacts (`pretrained_model.pkl`).

End users visiting the website do **not** need Python installed. Only the deployed API host runs Python.

Place the exact trained model files in:

- `api/models/column/pretrained_model.pkl`
- `api/models/wall/pretrained_model.pkl`

## Run Locally

1. Start API (from repo root):

```powershell
.\scripts\start-model-api.ps1
```

2. Serve website (separate terminal):

```powershell
cd site
python -m http.server 8080
```

3. Open:

- Website: `http://localhost:8080/`
- API health: `http://127.0.0.1:8000/health`

## Configure API URL for Production

Set your deployed API URL in:

- `site/assets/js/model-api-config.js`

Example:

```javascript
window.MODEL_API_BASE = "https://your-api-domain.example";
```

Then commit and push to GitHub.

## Deploy

- GitHub Pages deploys `site/` via `.github/workflows/deploy-pages.yml`.
- Deploy `api/` separately (Render, Railway, Fly.io, VM, etc.).

## Push Changes

```powershell
git add .
git commit -m "Update website and model API wiring"
git push
```
