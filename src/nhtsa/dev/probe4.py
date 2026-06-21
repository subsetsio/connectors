import importlib.util
spec=importlib.util.spec_from_file_location("nhtsa","src/nodes/nhtsa.py")
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
m.configure_http(headers=m._SR_HEADERS)
# tiny traversal: one make, collect vids, fetch one detail
ids=m._vehicle_ids_for_make(2020, "Acura")
print("vids for 2020 Acura:", ids[:5], "count", len(ids))
rec=m._sr_results(f"{m._SR_BASE}/VehicleId/{ids[0]}")
print("detail keys:", sorted(rec[0].keys())[:6], "... OverallRating=", rec[0].get("OverallRating"))
print("rate limiter ok, browser UA applied")
