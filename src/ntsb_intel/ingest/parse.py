import html

def clean_narrative(text):
    if text is None:
        return ""
    unescaped = html.unescape(text)
    return " ".join(unescaped.split())

def parse_record(record):
    return {
        "ntsb_num": record.get("cm_ntsbNum"),
        "event_date": record.get("cm_eventDate"),
        "city": record.get("cm_city"),
        "state": record.get("cm_state"),
        "highest_injury": record.get("cm_highestInjury"),
        "latitude": record.get("cm_Latitude"),
        "longitude": record.get("cm_Longitude"),
        "report_type": record.get("cm_mostRecentReportType"),
        "prelim_narrative": clean_narrative(record.get("prelimNarrative")),
        "factual_narrative": clean_narrative(record.get("factualNarrative")),
        "analysis_narrative": clean_narrative(record.get("analysisNarrative")),
    }

def extract_primary_cause(record):
    events = []
    for vehicle in record.get("cm_vehicles", []):
        events.extend(vehicle.get("cm_events", []))

    if not events:
        return None
    
    for event in events:
        if event.get("cm_isDefiningEvent"):
            return event.get("cicttEventSOEGroup")
        
def has_narrative(record):
    factual = clean_narrative(record.get("factualNarrative"))
    analysis = clean_narrative(record.get("analysisNarrative"))
    if factual or analysis:
        return 1
    return 0