import sys; sys.path.insert(0,"src")
import nodes.observatory_of_economic_complexity as M
print("BACI exporters:", len(M._members("trade_i_baci_a_22","Exporter Country Official","Trade Value")), "e.g.", M._members("trade_i_baci_a_22","Exporter Country Official","Trade Value")[:3])
print("BACI years:", M._members("trade_i_baci_a_22","Year","Trade Value"))
print("WDI countries:", len(M._members("indicators_i_wdi_a","Country Official","Measure")))
