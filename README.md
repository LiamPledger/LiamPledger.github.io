# Liam Pledger Academic Website

This repository contains:

- `site/`: static frontend deployed with GitHub Pages.
- `api/`: Python inference API that loads the exact Colab-trained model artifacts (`pretrained_model.pkl`).

End users visiting the website do **not** need Python installed. Only the deployed API host runs Python.

Model artifacts:

- API supports `pretrained_model.pkl` or `model.txt`.
- The Render blueprint in `render.yaml` uses:
  - `site/assets/models/column_model.txt`
  - `site/assets/models/wall_model.txt`

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

## Deploy API on Render

This repo includes `render.yaml` for one-click API deployment.

1. Push this repo to GitHub.
2. In Render, click `New +` -> `Blueprint`.
3. Select this GitHub repo and deploy.
4. When deployment finishes, open:
   - `https://<your-render-service>.onrender.com/health`
5. Confirm both models are loaded:
   - `"column_model_loaded": true`
   - `"wall_model_loaded": true`
6. Set the website API URL in `site/assets/js/model-api-config.js`:

```javascript
window.MODEL_API_BASE = "https://<your-render-service>.onrender.com";
```

7. Commit and push that file so GitHub Pages uses the live API.

## Push Changes

```powershell
git add .
git commit -m "Update website and model API wiring"
git push
```
