# Liam Pledger Academic Website

This repository is structured for GitHub Pages deployment of the academic website.

## Repository Structure

```text
.
|-- .github/
|   `-- workflows/
|       `-- deploy-pages.yml
|-- site/
|   |-- index.html
|   |-- publications.html
|   |-- model-column.html
|   |-- model-wall.html
|   |-- resources.html
|   `-- assets/
|       |-- css/
|       |-- js/
|       |-- fonts/
|       |-- data/
|       |-- docs/
|       `-- models/
`-- README.md
```

## Local Preview

From the repository root:

```powershell
python -m http.server 8000
```

Open `http://localhost:8000/site/`.

## Deploy on GitHub

1. Create a new GitHub repository (for example `liam-pledger-site`).
2. Push this folder to the `main` branch.
3. In GitHub, go to `Settings -> Pages`.
4. Set `Source` to `GitHub Actions`.
5. The `Deploy GitHub Pages` workflow will publish the `site/` directory.

```powershell
git init
git add .
git commit -m "Initial academic website"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```

## Configure Custom Domain

1. Set your domain in `site/CNAME` by running:

```powershell
.\scripts\set-custom-domain.ps1 -Domain "www.yourdomain.com"
```

2. Commit and push the `site/CNAME` file.
3. In GitHub, open `Settings -> Pages` and confirm the custom domain.
4. Add DNS records at your registrar:
- `A` record for root (`@`) -> `185.199.108.153`
- `A` record for root (`@`) -> `185.199.109.153`
- `A` record for root (`@`) -> `185.199.110.153`
- `A` record for root (`@`) -> `185.199.111.153`
- `CNAME` record for `www` -> `<your-username>.github.io`
5. Enable HTTPS in GitHub Pages after DNS propagates.

## Edit Your About Section

Your About text is in `site/index.html` under the first `<section class="panel hero">`.
