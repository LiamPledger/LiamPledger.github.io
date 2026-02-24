# Liam Pledger Academic Website

This repository contains a static website in `site/` deployed with GitHub Pages.

## LightGBM Models (Browser Inference)

The two drift-capacity pages now run LightGBM inference directly in the browser from exported Colab model text files.

Place these files in:

- `site/assets/models/column_model.txt`
- `site/assets/models/wall_model.txt`

The feature engineering/order in `site/assets/js/app.js` matches the Colab notebooks.

## Optional Model Path Overrides

Edit `site/assets/js/model-config.js` if your filenames are different.

## Local Preview

From repo root:

```powershell
python -m http.server 8080
```

Open: `http://localhost:8080/site/`

## Deploy

GitHub Pages deploys `site/` via `.github/workflows/deploy-pages.yml`.

## Push Updates

```powershell
git add .
git commit -m "Update website"
git push
```
