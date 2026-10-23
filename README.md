# Jupiter Bay Getaways

Public marketing site for five Jupiter Bay vacation rentals.

## Calendar setup

The public repository contains **no VRBO iCal URLs**. The five feed URLs are stored as encrypted GitHub Actions secrets and used only by the daily sync workflow.

Required repository secrets:

- `VRBO_E302`
- `VRBO_E303`
- `VRBO_E305`
- `VRBO_F204`
- `VRBO_VILLA_B5`

The workflow runs daily and can also be started manually from GitHub Actions.

## Hosting

Enable GitHub Pages from the `main` branch and the repository root.
