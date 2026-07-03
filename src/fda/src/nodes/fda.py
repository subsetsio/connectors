"""FDA (openFDA) connector.

Mechanism: bulk_download. The manifest at https://api.fda.gov/download.json
enumerates, per category/endpoint, a list of gzip'd-JSON partition files that
together hold the full dataset. For each rank-accepted category/endpoint pair
we download every partition, extract a curated set of (string) columns from the
nested records, and write ONE parquet batch per partition
(`fda-<entity>-<idx>`). The transform glob-unions those batches and publishes a
Delta table per subset.

Design choice — stateless full re-pull (the default shape): the accepted
corpus is modest (~5GB across all subsets, largest single subset device-udi
~1.75GB), so every run re-fetches the whole manifest and overwrites each
partition batch. No watermark/cursor — the source has no usable incremental
filter for bulk pulls (see research download_handoff), and a full re-pull picks
up FDA's weekly/quarterly revisions for free. Memory stays bounded because each
partition is parsed and written independently, never all at once.

The two adverse-event firehoses (drug/event ~108GB, device/event ~17GB) were
ranked below the publish threshold (scale_deferred): they are record-level
report dumps, not the statistical unit this platform publishes, and infeasible
as full Delta re-pulls in a bounded run. A curator can opt them back in.
"""

from __future__ import annotations

import io
import json
import zipfile

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)

MANIFEST_URL = "https://api.fda.gov/download.json"

# Curated columns per entity: (output_column, path). `path` is a dotted lookup
# into a record; a list value along the path collapses to its first element
# (used to flatten openFDA's list-valued fields). Every column is stored as a
# string in raw — the source's JSON types drift across records, so we defer
# typing to downstream curation and keep the parquet schema a stable contract.
FIELDS: dict[str, list[tuple[str, str]]] = {
    "animalandveterinary-event": [
        ("unique_aer_id_number", "unique_aer_id_number"),
        ("report_id", "report_id"),
        ("original_receive_date", "original_receive_date"),
        ("onset_date", "onset_date"),
        ("type_of_information", "type_of_information"),
        ("primary_reporter", "primary_reporter"),
        ("foreign_or_domestic", "foreign_or_domestic"),
        ("number_of_animals_affected", "number_of_animals_affected"),
        ("number_of_animals_treated", "number_of_animals_treated"),
    ],
    "cosmetic-event": [
        ("report_number", "report_number"),
        ("report_type", "report_type"),
        ("report_version", "report_version"),
        ("legacy_report_id", "legacy_report_id"),
        ("event_date", "event_date"),
        ("initial_received_date", "initial_received_date"),
        ("latest_received_date", "latest_received_date"),
        ("meddra_version", "meddra_version"),
    ],
    "device-510k": [
        ("k_number", "k_number"),
        ("applicant", "applicant"),
        ("device_name", "device_name"),
        ("product_code", "product_code"),
        ("clearance_type", "clearance_type"),
        ("decision_code", "decision_code"),
        ("decision_description", "decision_description"),
        ("decision_date", "decision_date"),
        ("date_received", "date_received"),
        ("advisory_committee", "advisory_committee"),
        ("advisory_committee_description", "advisory_committee_description"),
        ("review_advisory_committee", "review_advisory_committee"),
        ("expedited_review_flag", "expedited_review_flag"),
        ("third_party_flag", "third_party_flag"),
        ("city", "city"),
        ("state", "state"),
        ("country_code", "country_code"),
        ("postal_code", "postal_code"),
    ],
    "device-classification": [
        ("product_code", "product_code"),
        ("device_name", "device_name"),
        ("device_class", "device_class"),
        ("regulation_number", "regulation_number"),
        ("medical_specialty", "medical_specialty"),
        ("medical_specialty_description", "medical_specialty_description"),
        ("review_panel", "review_panel"),
        ("review_code", "review_code"),
        ("submission_type_id", "submission_type_id"),
        ("gmp_exempt_flag", "gmp_exempt_flag"),
        ("implant_flag", "implant_flag"),
        ("life_sustain_support_flag", "life_sustain_support_flag"),
        ("third_party_flag", "third_party_flag"),
        ("summary_malfunction_reporting", "summary_malfunction_reporting"),
        ("unclassified_reason", "unclassified_reason"),
        ("definition", "definition"),
    ],
    "device-enforcement": [
        ("recall_number", "recall_number"),
        ("event_id", "event_id"),
        ("status", "status"),
        ("classification", "classification"),
        ("product_type", "product_type"),
        ("recalling_firm", "recalling_firm"),
        ("product_description", "product_description"),
        ("product_quantity", "product_quantity"),
        ("reason_for_recall", "reason_for_recall"),
        ("voluntary_mandated", "voluntary_mandated"),
        ("initial_firm_notification", "initial_firm_notification"),
        ("distribution_pattern", "distribution_pattern"),
        ("recall_initiation_date", "recall_initiation_date"),
        ("center_classification_date", "center_classification_date"),
        ("report_date", "report_date"),
        ("city", "city"),
        ("state", "state"),
        ("country", "country"),
        ("postal_code", "postal_code"),
    ],
    "device-pma": [
        ("pma_number", "pma_number"),
        ("supplement_number", "supplement_number"),
        ("supplement_type", "supplement_type"),
        ("supplement_reason", "supplement_reason"),
        ("applicant", "applicant"),
        ("trade_name", "trade_name"),
        ("generic_name", "generic_name"),
        ("product_code", "product_code"),
        ("advisory_committee", "advisory_committee"),
        ("advisory_committee_description", "advisory_committee_description"),
        ("decision_code", "decision_code"),
        ("decision_date", "decision_date"),
        ("date_received", "date_received"),
        ("fed_reg_notice_date", "fed_reg_notice_date"),
        ("expedited_review_flag", "expedited_review_flag"),
        ("docket_number", "docket_number"),
        ("city", "city"),
        ("state", "state"),
    ],
    "device-recall": [
        ("cfres_id", "cfres_id"),
        ("product_res_number", "product_res_number"),
        ("res_event_number", "res_event_number"),
        ("recall_status", "recall_status"),
        ("action", "action"),
        ("product_code", "product_code"),
        ("product_description", "product_description"),
        ("product_quantity", "product_quantity"),
        ("recalling_firm", "recalling_firm"),
        ("reason_for_recall", "reason_for_recall"),
        ("root_cause_description", "root_cause_description"),
        ("distribution_pattern", "distribution_pattern"),
        ("firm_fei_number", "firm_fei_number"),
        ("event_date_created", "event_date_created"),
        ("event_date_initiated", "event_date_initiated"),
        ("event_date_posted", "event_date_posted"),
        ("event_date_terminated", "event_date_terminated"),
        ("city", "city"),
        ("state", "state"),
        ("postal_code", "postal_code"),
    ],
    "device-registrationlisting": [
        ("registration_number", "registration.registration_number"),
        ("fei_number", "registration.fei_number"),
        ("name", "registration.name"),
        ("status_code", "registration.status_code"),
        ("initial_importer_flag", "registration.initial_importer_flag"),
        ("reg_expiry_date_year", "registration.reg_expiry_date_year"),
        ("address_line_1", "registration.address_line_1"),
        ("city", "registration.city"),
        ("state_code", "registration.state_code"),
        ("iso_country_code", "registration.iso_country_code"),
        ("zip_code", "registration.zip_code"),
        ("owner_operator_firm_name", "registration.owner_operator.firm_name"),
        ("k_number", "k_number"),
        ("pma_number", "pma_number"),
        ("establishment_type", "establishment_type"),
        ("proprietary_name", "proprietary_name"),
    ],
    "device-udi": [
        ("public_device_record_key", "public_device_record_key"),
        ("brand_name", "brand_name"),
        ("version_or_model_number", "version_or_model_number"),
        ("catalog_number", "catalog_number"),
        ("company_name", "company_name"),
        ("device_description", "device_description"),
        ("labeler_duns_number", "labeler_duns_number"),
        ("commercial_distribution_status", "commercial_distribution_status"),
        ("commercial_distribution_end_date", "commercial_distribution_end_date"),
        ("device_count_in_base_package", "device_count_in_base_package"),
        ("is_rx", "is_rx"),
        ("is_otc", "is_otc"),
        ("is_kit", "is_kit"),
        ("is_combination_product", "is_combination_product"),
        ("is_single_use", "is_single_use"),
        ("has_lot_or_batch_number", "has_lot_or_batch_number"),
        ("has_serial_number", "has_serial_number"),
        ("has_expiration_date", "has_expiration_date"),
        ("mri_safety", "mri_safety"),
        ("record_status", "record_status"),
        ("publish_date", "publish_date"),
        ("public_version_number", "public_version_number"),
        ("public_version_date", "public_version_date"),
    ],
    "drug-drugsfda": [
        ("application_number", "application_number"),
        ("sponsor_name", "sponsor_name"),
        ("brand_name", "openfda.brand_name"),
        ("generic_name", "openfda.generic_name"),
        ("manufacturer_name", "openfda.manufacturer_name"),
        ("product_type", "openfda.product_type"),
        ("route", "openfda.route"),
        ("substance_name", "openfda.substance_name"),
    ],
    "drug-enforcement": [
        ("recall_number", "recall_number"),
        ("event_id", "event_id"),
        ("status", "status"),
        ("classification", "classification"),
        ("product_type", "product_type"),
        ("recalling_firm", "recalling_firm"),
        ("product_description", "product_description"),
        ("product_quantity", "product_quantity"),
        ("reason_for_recall", "reason_for_recall"),
        ("voluntary_mandated", "voluntary_mandated"),
        ("initial_firm_notification", "initial_firm_notification"),
        ("distribution_pattern", "distribution_pattern"),
        ("recall_initiation_date", "recall_initiation_date"),
        ("center_classification_date", "center_classification_date"),
        ("report_date", "report_date"),
        ("termination_date", "termination_date"),
        ("city", "city"),
        ("state", "state"),
        ("country", "country"),
        ("postal_code", "postal_code"),
    ],
    "drug-label": [
        ("id", "id"),
        ("effective_time", "effective_time"),
        ("brand_name", "openfda.brand_name"),
        ("generic_name", "openfda.generic_name"),
        ("manufacturer_name", "openfda.manufacturer_name"),
        ("product_type", "openfda.product_type"),
        ("route", "openfda.route"),
        ("substance_name", "openfda.substance_name"),
        ("product_ndc", "openfda.product_ndc"),
        ("spl_set_id", "openfda.spl_set_id"),
    ],
    "drug-ndc": [
        ("product_ndc", "product_ndc"),
        ("product_id", "product_id"),
        ("spl_id", "spl_id"),
        ("brand_name", "brand_name"),
        ("brand_name_base", "brand_name_base"),
        ("generic_name", "generic_name"),
        ("labeler_name", "labeler_name"),
        ("product_type", "product_type"),
        ("dosage_form", "dosage_form"),
        ("marketing_category", "marketing_category"),
        ("application_number", "application_number"),
        ("marketing_start_date", "marketing_start_date"),
        ("listing_expiration_date", "listing_expiration_date"),
        ("finished", "finished"),
    ],
    "drug-shortages": [
        ("package_ndc", "package_ndc"),
        ("generic_name", "generic_name"),
        ("company_name", "company_name"),
        ("status", "status"),
        ("update_type", "update_type"),
        ("therapeutic_category", "therapeutic_category"),
        ("dosage_form", "dosage_form"),
        ("presentation", "presentation"),
        ("initial_posting_date", "initial_posting_date"),
        ("update_date", "update_date"),
        ("discontinued_date", "discontinued_date"),
        ("contact_info", "contact_info"),
        ("related_info", "related_info"),
    ],
    "food-enforcement": [
        ("recall_number", "recall_number"),
        ("event_id", "event_id"),
        ("status", "status"),
        ("classification", "classification"),
        ("product_type", "product_type"),
        ("recalling_firm", "recalling_firm"),
        ("product_description", "product_description"),
        ("product_quantity", "product_quantity"),
        ("reason_for_recall", "reason_for_recall"),
        ("voluntary_mandated", "voluntary_mandated"),
        ("initial_firm_notification", "initial_firm_notification"),
        ("distribution_pattern", "distribution_pattern"),
        ("recall_initiation_date", "recall_initiation_date"),
        ("center_classification_date", "center_classification_date"),
        ("report_date", "report_date"),
        ("termination_date", "termination_date"),
        ("city", "city"),
        ("state", "state"),
        ("country", "country"),
        ("postal_code", "postal_code"),
    ],
    "food-event": [
        ("report_number", "report_number"),
        ("date_created", "date_created"),
        ("date_started", "date_started"),
    ],
    "other-nsde": [
        ("package_ndc", "package_ndc"),
        ("package_ndc11", "package_ndc11"),
        ("proprietary_name", "proprietary_name"),
        ("dosage_form", "dosage_form"),
        ("marketing_category", "marketing_category"),
        ("application_number_or_citation", "application_number_or_citation"),
        ("product_type", "product_type"),
        ("billing_unit", "billing_unit"),
        ("marketing_start_date", "marketing_start_date"),
        ("marketing_end_date", "marketing_end_date"),
        ("inactivation_date", "inactivation_date"),
        ("reactivation_date", "reactivation_date"),
    ],
    "other-substance": [
        ("unii", "unii"),
        ("uuid", "uuid"),
        ("substance_class", "substance_class"),
        ("definition_type", "definition_type"),
        ("definition_level", "definition_level"),
        ("version", "version"),
    ],
    "tobacco-problem": [
        ("report_id", "report_id"),
        ("date_submitted", "date_submitted"),
        ("nonuser_affected", "nonuser_affected"),
        ("number_tobacco_products", "number_tobacco_products"),
        ("number_health_problems", "number_health_problems"),
        ("number_product_problems", "number_product_problems"),
    ],
}


@transient_retry()
def _get_bytes(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.content


@transient_retry()
def _get_json(url: str):
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def _extract(rec: dict, path: str):
    """Walk a dotted path through nested dicts; collapse a list to its first
    element. Return a string, or None for missing / non-scalar values."""
    cur = rec
    for part in path.split("."):
        if isinstance(cur, list):
            cur = cur[0] if cur else None
        if not isinstance(cur, dict):
            cur = None
            break
        cur = cur.get(part)
    if isinstance(cur, list):
        cur = cur[0] if cur else None
    if cur is None or isinstance(cur, (dict, list)):
        return None
    return str(cur)


def fetch_one(node_id: str) -> None:
    """Download every partition of one openFDA category/endpoint and write one
    parquet batch per partition. node_id is `fda-<entity>`; the entity (e.g.
    `drug-ndc`) splits into category (`drug`) and endpoint (`ndc`)."""
    entity = node_id[len("fda-"):]
    category, endpoint = entity.split("-", 1)
    fields = FIELDS[entity]
    schema = pa.schema([(col, pa.string()) for col, _ in fields])

    manifest = _get_json(MANIFEST_URL)
    partitions = manifest["results"][category][endpoint].get("partitions") or []
    if not partitions:
        raise AssertionError(f"{node_id}: manifest lists 0 partitions for {entity}")

    for idx, part in enumerate(partitions):
        url = part["file"]
        raw = _get_bytes(url)
        with zipfile.ZipFile(io.BytesIO(raw)) as zf:
            member = zf.namelist()[0]
            records = json.loads(zf.read(member)).get("results", []) or []

        columns = {col: [] for col, _ in fields}
        for rec in records:
            for col, path in fields:
                columns[col].append(_extract(rec, path))

        table = pa.table(
            {col: pa.array(columns[col], type=pa.string()) for col, _ in fields},
            schema=schema,
        )
        save_raw_parquet(table, f"{node_id}-{idx:04d}")


from constants import ENTITY_IDS

DOWNLOAD_SPECS = [
    NodeSpec(id=f"fda-{eid}", fn=fetch_one, kind="download")
    for eid in ENTITY_IDS
]

# Thin publish: each partition batch already carries a uniform string schema,
# so the transform just glob-unions the batches into the published table. Types
# are deferred to curation (openFDA date/flag encodings vary across endpoints).

# Per-entity grain (entity -> (key, temporal)). Keys use the endpoint's natural
# unique id (confirmed unique in profiling); temporal prefers a populated
# event/receipt/posting date over open-ended expiry/end dates. Reference tables
# with no observation period (classification, drugsfda, substance, tobacco) and
# tables with no confirmed unique id (device-pma, registrationlisting,
# drug-shortages) are left partly/fully undeclared. Every named column is an
# output column of that entity's SELECT *.
_GRAIN = {
    "animalandveterinary-event": (("unique_aer_id_number",), "original_receive_date"),
    "cosmetic-event": (("report_number",), "initial_received_date"),
    "device-510k": (("k_number",), "decision_date"),
    "device-classification": (("product_code",), None),
    "device-enforcement": (("recall_number",), "report_date"),
    "device-pma": (None, "decision_date"),
    "device-recall": (("product_res_number",), "event_date_posted"),
    "device-registrationlisting": (None, "reg_expiry_date_year"),
    "device-udi": (("public_device_record_key",), "publish_date"),
    "drug-drugsfda": (("application_number",), None),
    "drug-enforcement": (("recall_number",), "center_classification_date"),
    "drug-label": (("id",), "effective_time"),
    "drug-ndc": (("product_id",), "marketing_start_date"),
    "drug-shortages": (None, None),
    "food-enforcement": (("recall_number",), "report_date"),
    "food-event": (("report_number",), "date_created"),
    "other-nsde": (("package_ndc",), "marketing_start_date"),
    "other-substance": (("uuid",), None),
    "tobacco-problem": (("report_id",), None),
}

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        key=_GRAIN.get(s.id[len("fda-"):], (None, None))[0],
        temporal=_GRAIN.get(s.id[len("fda-"):], (None, None))[1],
        sql=f'SELECT * FROM "{s.id}"',
    )
    for s in DOWNLOAD_SPECS
]
