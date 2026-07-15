# Demo data: simulated health paid claims triangles

This folder contains reproducible synthetic data generated with:

```bash
python scripts/generate_demo_triangles.py --language en
```

Files:

- `demo_health_paid_claims_long.csv`: observed synthetic claim payments by origin year and development age.
- `paid_incremental_triangle.csv`: paid incremental triangle.
- `paid_cumulative_triangle.csv`: paid cumulative triangle.
- `age_to_age_factors.csv`: selected volume-weighted development factors.
- `chain_ladder_results.csv`: latest paid, selected CDF, ultimate and IBNR by origin year.
- `run_summary.txt`: concise run summary.

The data are synthetic and must not be interpreted as real portfolio experience.
