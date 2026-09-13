# FX

`FXProvider.get_rate(base, quote, date)` is the provider-neutral boundary.
`StoredFXProvider` uses a dated, directed database row and safely handles an
inverse pair. A production fetch adapter can populate `exchange_rates` from a
reputable ECB-compatible source, after which settled historical transactions
reuse the stored dated rate rather than repeatedly calling the network.
