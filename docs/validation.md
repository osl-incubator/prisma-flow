# Validation

`prisma-flow` validates the initial PRISMA count relationships:

```text
records_screened = identified_total - removed_total
reports_sought = records_screened - records_excluded
reports_assessed = reports_sought - reports_not_retrieved
```

All counts must be non-negative integers.

The relationship between reports assessed, reports excluded, and studies
included is a warning by default because one study can have multiple reports.
Use strict validation if you want that reconciliation to be an error.
