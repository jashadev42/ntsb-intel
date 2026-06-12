import sqlite3

def get_top_categories(db_path="data/incidents.db", n=10):
    conn = sqlite3.connect(db_path)
    query = """
        SELECT      primary_cause
        FROM        incidents
        WHERE       has_narrative = 1
        AND         primary_cause NOT IN ('', 'Other')
        GROUP BY    primary_cause
        ORDER BY COUNT(*) DESC
        LIMIT ?
    """
    rows = conn.execute(query, (n,)).fetchall()
    conn.close()
    categories = [row[0] for row in rows]
    return categories

def load_training_data(db_path="data/incidents.db", categories=None):
    if categories is None:
        categories = get_top_categories(db_path)
    conn = sqlite3.connect(db_path)
    placeholders = ",".join("?" * len(categories))
    query = f"""
        SELECT  factual_narrative, analysis_narrative, primary_cause
        FROM    incidents
        WHERE   has_narrative = 1
        AND primary_cause IN ({placeholders})
    """
    rows = conn.execute(query, categories).fetchall()
    conn.close()

    texts = []
    labels = []
    for factual, analysis, cause in rows:
        text = factual if factual else analysis
        texts.append(text)
        labels.append(cause)

    return texts, labels