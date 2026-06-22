"""Static configuration for the Christmas Bird Count connector.

Enumeration of count circles. The CBC web app exposes circle data only through
the `HistoricalResultsByCount` report keyed by a numeric circle id (`cid`); the
id->circle map is not published as a clean list endpoint (the interactive grid
loads it through a fragile 3-level DevExpress callback cascade). Empirically the
valid circle ids occupy a single dense, contiguous band — every id below ~54,500
and above ~60,400 returns a 325-byte header-only template, while the band itself
is ~85% populated. So enumeration is a direct scan of the band: fetch each id,
keep the ones that return real data. New circles are assigned incrementing ids,
so the band's upper edge creeps up over time — CID_MAX carries headroom and the
crawl raises if real circles appear within CID_CEILING_MARGIN of it (signal to
extend the band) rather than silently truncating coverage.
"""

# Inclusive cid scan band. Observed live range ~[54,500, 60,400]; these carry
# margin below and ~1,600 ids of headroom above for circles added in future
# seasons.
CID_MIN = 54_000
CID_MAX = 62_000

# If a valid circle is found within this many ids of CID_MAX, the band is nearly
# exhausted and must be widened — raise instead of risking silent truncation.
CID_CEILING_MARGIN = 300

# Count-year window. Count year 1 = the 1900-01 season; the report returns every
# season within [SY, EY]. EY is set well beyond the current season (~126) so new
# seasons are always captured; out-of-range years simply return nothing.
SY = 1
EY = 140
