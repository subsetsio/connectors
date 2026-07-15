-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "opr_desc_txt",
    "bus_svc_no_txt",
    "bus_dirctn_txt",
    "bus_route_seq_num",
    "rd_nam",
    "bus_stop_desc_txt",
    "op_hr_1_txt",
    "op_hr_2_txt",
    "orig_dest_txt",
    "fare_txt",
    "x_coord",
    "y_coord",
    "bus_stop_cd",
    "no_svc_ind"
FROM "sg-data-d-be2accb464cc5600de937eb9000a0255"
