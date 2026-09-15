#!/usr/bin/env python3
"""GG Dashboard — Memory stats generator from ChromaDB SQLite backend.
Outputs gg-memory-stats.json consumed by the dashboard frontend."""

import json, os, sys

CHROMA_DB = "/home/airoot/.openclaw/memory/chromadb/chroma.sqlite3"

def main():
    if not os.path.exists(CHROMA_DB):
        print(json.dumps({"error": "ChromaDB not found at " + CHROMA_DB}))
        return 1

    try:
        import sqlite3
    except ImportError:
        print(json.dumps({"error": "sqlite3 not available"}))
        return 1

    conn = sqlite3.connect(CHROMA_DB)
    c = conn.cursor()

    # Total counts per collection
    c.execute("""
        SELECT cl.name, COUNT(e.id)
        FROM embeddings e
        JOIN segments s ON e.segment_id = s.id
        JOIN collections cl ON s.collection = cl.id
        GROUP BY cl.name
    """)
    total_by_collection = {r[0]: r[1] for r in c.fetchall()}

    # Daily growth
    c.execute("""
        SELECT DATE(created_at) as day, COUNT(*)
        FROM embeddings e
        JOIN segments s ON e.segment_id = s.id
        JOIN collections cl ON s.collection = cl.id
        WHERE cl.name = 'facts'
        GROUP BY day
        ORDER BY day
    """)
    cum = 0
    growth_data = []
    for day, cnt in c.fetchall():
        cum += cnt
        growth_data.append({"date": day, "added": cnt, "total": cum})

    # Top 100 by importance_score
    c.execute("""
        SELECT e.embedding_id,
               imp.float_value AS importance,
               doc.string_value AS document,
               created.string_value AS created_dt
        FROM embeddings e
        JOIN segments s ON e.segment_id = s.id
        JOIN collections cl ON s.collection = cl.id
        LEFT JOIN embedding_metadata imp ON e.id = imp.id AND imp.key = 'importance_score'
        LEFT JOIN embedding_metadata doc ON e.id = doc.id AND doc.key = 'chroma:document'
        LEFT JOIN embedding_metadata created ON e.id = created.id AND created.key = 'created_at'
        WHERE cl.name = 'facts' AND imp.float_value IS NOT NULL
        ORDER BY imp.float_value DESC
        LIMIT 100
    """)
    top100 = []
    for row in c.fetchall():
        doc = (row[2] or "").strip()[:120]
        if len(row[2] or "") > 120:
            doc += "..."
        top100.append({
            "id": row[0][:8],
            "importance": round(row[1] or 0, 1),
            "doc": doc,
            "created": (row[3] or "")[:10]
        })

    # Score distribution
    score_dist = {}
    for r in top100:
        s = r["importance"]
        if s >= 8: b = ">=8"
        elif s >= 7: b = "7-7.9"
        elif s >= 6: b = "6-6.9"
        elif s >= 5: b = "5-5.9"
        elif s >= 4: b = "4-4.9"
        elif s >= 3: b = "3-3.9"
        elif s >= 2: b = "2-2.9"
        elif s >= 1: b = "1-1.9"
        else: b = "<1"
        score_dist[b] = score_dist.get(b, 0) + 1

    output = {
        "total": {
            "facts": total_by_collection.get("facts", 0),
            "memories": total_by_collection.get("memories", 0),
            "all": sum(total_by_collection.values())
        },
        "growth": growth_data,
        "score_distribution": score_dist,
        "top100": top100,
        "generated": __import__("datetime").datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
    }

    print(json.dumps(output, ensure_ascii=False))
    conn.close()
    return 0

if __name__ == "__main__":
    sys.exit(main())
