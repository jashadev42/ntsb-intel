import json
from ntsb_intel.ingest.db import get_connection, create_table, insert_record
from ntsb_intel.ingest.parse import parse_record

def main():
    conn = get_connection()
    create_table(conn)

    with open("data/aviation_raw.json") as f:
        records = json.load(f)

        inserted = 0
        for record in records:
            row = parse_record(record)
            insert_record(conn, row)
            inserted += 1

        conn.close()
        print(f'{inserted} rows inserted.')

if __name__ == "__main__":
    main()