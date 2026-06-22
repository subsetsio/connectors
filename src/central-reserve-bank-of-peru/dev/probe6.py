import sys
sys.path.insert(0, "src/nodes")
import central_reserve_bank_of_peru as m

# parser unit checks
assert m._period_to_iso("10.Feb.26", "Diaria") == "2026-02-10", m._period_to_iso("10.Feb.26","Diaria")
assert m._period_to_iso("Ene.2024", "Mensual") == "2024-01-01"
assert m._period_to_iso("Dic.1992", "Mensual") == "1992-12-01"
assert m._period_to_iso("T1.00", "Trimestral") == "2000-01-01"
assert m._period_to_iso("T4.94", "Trimestral") == "1994-10-01", m._period_to_iso("T4.94","Trimestral")
assert m._period_to_iso("2024", "Anual") == "2024-01-01"
assert m._period_to_iso("garbage", "Mensual") is None
assert m._parse_value("n.d.") is None and m._parse_value("3.14") == 3.14 and m._parse_value("") is None
print("parser OK")

# live single-series fetch (no save_raw)
obs = m._fetch_series_observations("PN00001MM", "Mensual", "Ene-1992")
print("monthly obs", len(obs), obs[0], obs[-1])
obs = m._fetch_series_observations("PD04637PD", "Diaria", "Feb-2014")
print("daily obs", len(obs), obs[0], obs[-1])
obs = m._fetch_series_observations("PN02526AQ", "Trimestral", "1979-1")
print("quarterly obs", len(obs), obs[0], obs[-1])
obs = m._fetch_series_observations("PM05317AA", "Anual", "1921")
print("annual obs", len(obs), obs[0] if obs else None, obs[-1] if obs else None)
