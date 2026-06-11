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