# Model API (Exact Colab Inference)

This API serves drift-capacity predictions using the **exact trained model artifacts** from Colab.

## 1) Place model files

Put your Colab-trained files in these folders:

- `api/models/column/pretrained_model.pkl` (or `api/models/column/model.txt`)
- `api/models/wall/pretrained_model.pkl` (or `api/models/wall/model.txt`)

Notes:
- Use the exact files exported from Colab to match Colab outputs.
- If both `.pkl` and `.txt` exist, `.pkl` is loaded first.

If you only have the notebook session model object (`bst`) in Colab:

```python
import pickle

with open("pretrained_model.pkl", "wb") as f:
    pickle.dump(bst, f)

bst.save_model("model.txt")
```

## 2) Install and run locally

```powershell
cd api
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --host 127.0.0.1 --port 8000
```

Health check:

```text
GET http://127.0.0.1:8000/health
```

## 3) Frontend integration

The website model pages call:

- `POST /predict/column`
- `POST /predict/wall`

Default API base URL in frontend: `http://127.0.0.1:8000`.

To use a deployed API URL, set it in `site/assets/js/model-api-config.js`:

```javascript
window.MODEL_API_BASE = "https://your-api-domain.example";
```

## 4) Optional environment overrides

You can override model search paths:

- `COLUMN_MODEL_PATHS` (semicolon-separated)
- `WALL_MODEL_PATHS` (semicolon-separated)

Example:

```powershell
$env:COLUMN_MODEL_PATHS = "C:\models\column\pretrained_model.pkl"
$env:WALL_MODEL_PATHS = "C:\models\wall\pretrained_model.pkl"
uvicorn main:app --host 127.0.0.1 --port 8000
```
