from ntsb_intel.ingest.parse import clean_narrative

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