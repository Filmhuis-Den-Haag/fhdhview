# ADR-002 Upcoming Price Changes

Date: 2026-11-22

## Context

Once in a while the prices need to change. The info screen should show the upcoming new prices in the sidebar, so that customers are informed beforehand.

## Decision

The configuration is refactored so that a `PriceRow` allows for an optional `price_new`.

If the `prijzen` section has entries with `price_new` and the `prices` config has a `price_start` date the frontend will show the new prices in a separate column.

If the `price_start` date has passed the frontend will automatically use the `price_new` for each row.

## MVP Definition

See a column with upcoming price changes. Adopt the new prices when the expected date has passed.

## Future Improvements

* add similar behavior for `kortingsprijzen` section (not needed right now)
