from ntsb_intel.ingest.parse import clean_narrative
from ntsb_intel.ingest.parse import parse_record
from ntsb_intel.ingest.parse import extract_primary_cause
from ntsb_intel.ingest.parse import has_narrative

def test_clean_narative_removes_html_entities():
    raw = "damage&#x0D;&#x0D;The pilot"
    result = clean_narrative(raw)
    assert result == "damage The pilot"

def test_null_returns_empty_string():
    assert clean_narrative(None) == ""

def test_already_clean_text_unchanged():
    assert clean_narrative("The pilot landed safely") == "The pilot landed safely"

def test_collapses_whitespace():
    assert clean_narrative("The  pilot   landed") == "The pilot landed"

def test_parse_record_extracts_flat_fields():
    record = {
        "cm_ntsbNum": "TEST123",
        "cm_city": "Duncan",
        "cm_state": "OK",
        "cm_Latitude": 34.47,
        "prelimNarrative": "The pilot landed&#x0D;\nsafely",
    }
    result = parse_record(record)
    assert result["ntsb_num"] == "TEST123"

def test_primary_cause_uses_defining_event():
    record = {
        "cm_vehicles": [
            {
                "cm_events": [
                    {"cicttEventSOEGroup": "Loss of Control", "cm_isDefiningEvent": False, "cm_sequenceNum": 1},
                    {"cicttEventSOEGroup": "Engine Failure", "cm_isDefiningEvent": True, "cm_sequenceNum": 2},
                ]
            }
        ]
    }
    assert extract_primary_cause(record) == "Engine Failure"

def test_has_narrative():
    records = {
            "analysisNarrative": "Test",
            "factualNarrative": None,
    }
    
    assert has_narrative(records) == 1