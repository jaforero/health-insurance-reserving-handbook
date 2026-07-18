# Monthly demo data r2

Synthetic data with a **72 x 36** estimation basis and a traditional **36 x 36** view. Full runoff is simulated through age 48; the 35->48 tail is a known generator assumption.

- `monthly_paid_cumulative_triangle.csv`: full estimation basis.
- `traditional_36x36_view.csv`: latest 36 origins, traditional 36 x 36 presentation.
- `monthly_age_to_age_factors.csv`: factors and observations per link.
- `unpaid_claim_liability_projection_results.csv`: projected cost, tail and estimated unpaid claim liability.
- `monthly_bornhuetter_ferguson_prior.csv`: synthetic BF/Benktander prior.

**Scope:** an aggregate paid-only triangle cannot split pure IBNR, RBNS and IBNER. This is an educational result, not a booked reserve.
