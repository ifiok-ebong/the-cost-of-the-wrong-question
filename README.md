# The Cost of the Wrong Question

Most analytics failures start before data is touched.

## Executive summary
- Decision: choose one primary intervention for the next quarter.
- Method: three competing structural drivers tested independently, then compared.
- Output: a dominance assessment and a recommendation in `analysis_recommendation.md`.

This repo is a decision-first case study showing how framing errors distort analysis and lead teams toward the wrong action.

## Reproduce (local)
**Python:** 3.11+ (tested on 3.12)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# Requires Kaggle credentials in ~/.kaggle/kaggle.json
python scripts/download_data.py
jupyter notebook notebooks/analysis_decision_analysis.ipynb
```

## Deliverables
- `README.md`
- `decision_statement.md`
- `business_context.md`
- `dataset_overview.md`
- `analysis_execution_blueprint.md`
- `notebooks/analysis_decision_analysis.ipynb`

## Reproducibility and data
This project uses a download script plus hashes.

- Run: `python scripts/download_data.py`
- Verify: `data/hashes.sha256`

Raw data is not committed by default.

## License
Project code and writing: MIT (unless otherwise noted).
Dataset licensing is documented in `data/README.md`.

## Quick links
- Decision brief: `decision_brief.md`
- Recommendation: `analysis_recommendation.md`
- Figures: `docs/README.md`
