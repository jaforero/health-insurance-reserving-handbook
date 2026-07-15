# Monthly triangle demo data

Entirely synthetic data for 60 origin months and development ages 0–24.

## Reproduction

```bash
python scripts/generate_demo_monthly_triangles.py --language en
```

## Files

- `monthly_paid_claims_long.csv`: observed long-format data.
- `monthly_paid_incremental_triangle.csv` and `monthly_paid_cumulative_triangle.csv`: traditional triangles.
- `monthly_age_to_age_factors.csv`: monthly factors and observation counts.
- `monthly_chain_ladder_results.csv`: ultimate, IBNR and comparison with simulated truth.
- `data_sufficiency_diagnostics.csv`: design-sufficiency controls.

The data do not represent any entity's experience or a prescribed method.
