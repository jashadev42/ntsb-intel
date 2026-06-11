import sqlite3
from pathlib import Path

def create_table(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS incidents (
            ntsb_num            TEXT PRIMARY KEY,
            event_date          TEXT,
            city                TEXT,
            state               TEXT,
            highest_injury      TEXT,
            latitude            REAL,
            longitude           REAL,
            report_type         TEXT,
            prelim_narrative    TEXT,
            factual_narrative   TEXT,
            analysis_narrative  TEXT,
            primary_cause       TEXT,
            has_narrative       INTEGER,
            raw_vehicles        TEXT
        )
    """)
    conn.commit()

def get_connection(db_path="data/incidents.db"):
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    return conn

def insert_record(conn, row):
    conn.execute("""
        INSERT OR REPLACE INTO incidents (
            ntsb_num, event_date, city, state, highest_injury,
            latitude, longitude, report_type, prelim_narrative,
            factual_narrative, analysis_narrative, primary_cause,
            has_narrative, raw_vehicles
        ) VALUES (
            :ntsb_num, :event_date, :city, :state, :highest_injury,
            :latitude, :longitude, :report_type, :prelim_narrative,
            :factual_narrative, :analysis_narrative, :primary_cause,
            :has_narrative, :raw_vehicles
        )
    """, row)
    conn.commit()