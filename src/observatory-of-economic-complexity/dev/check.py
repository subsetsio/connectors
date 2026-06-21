import sys
sys.path.insert(0, "src")
from nodes.observatory_of_economic_complexity import _parse_csv, _data_csv, _request_params, _transform_sql, _spec_id, _members
from constants import CUBES

# ECI small whole
cfg = CUBES["complexity_eci_a_hs92_hs4"]
ms = {__import__("nodes.observatory_of_economic_complexity", fromlist=["_snake"])._snake(m) for m in cfg["measures"]}
txt = _data_csv(_request_params("complexity_eci_a_hs92_hs4", cfg["drilldowns"], cfg["measures"], {}))
t = _parse_csv(txt, ms)
print("ECI table:", t.num_rows, "rows; schema:")
print(t.schema)
print("sample:", t.slice(0,2).to_pylist())

# 13f whole (single, 19MB) just header/schema check on small slice via cut
# Check members for BACI Year
print("BACI Year members:", _members("trade_i_baci_a_22", "Year"))

# transform sql examples
print(_transform_sql(_spec_id("complexity_eci_a_hs92_hs4"), cfg["measures"]))
print(_transform_sql(_spec_id("gini_inequality_combined"), CUBES["gini_inequality_combined"]["measures"]))
print(_transform_sql(_spec_id("13f_managers"), CUBES["13f_managers"]["measures"]))
