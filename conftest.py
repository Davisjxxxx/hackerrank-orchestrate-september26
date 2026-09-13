"""Keep imported Lane B workspaces out of root finance test collection.

Lane B tests have their own ``pyproject.toml`` and are run from the canonical
lab directory. The retained red-team workspace is likewise an explicit
target. Ignoring both directories here prevents root pytest from collecting
two copies of ``price_intel`` while preserving root evaluation discovery.
"""

collect_ignore_glob = [
    "buy-or-wait-price-intelligence-lab/*",
    "buy-or-wait-price-intelligence-red-team/*",
]
