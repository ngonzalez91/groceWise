import os
import sqlite3
import numpy as np
from openai import OpenAI
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import DBSCAN

DB_PATH = "./bills.db"
SIMILARITY_THRESHOLD = 0.85
OPENAI_MODEL = "text-embedding-3-small"

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def normalize_new_items():
    ensure_normalization_table()
    items = fetch_items_to_normalize()
    if not items:
        print("[INFO] No new items to normalize.")
        return

    print(f"[INFO] Normalizing {len(items)} new items...")
    embeddings = get_embeddings(items)
    clusters = cluster_embeddings(items, embeddings)
    mapping = assign_canonical_names(clusters)
    save_mapping_to_db(mapping)

    print(f"[INFO] Canonical items added: {len(set(mapping.values()))}")
    print(f"[INFO] Item variants normalized: {len(mapping)}")

def ensure_normalization_table():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS item_normalization (
            variant_name TEXT PRIMARY KEY,
            canonical_name TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def fetch_items_to_normalize():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT DISTINCT name
        FROM receipts
        WHERE name NOT IN (
            SELECT variant_name FROM item_normalization
        )
    """)
    rows = c.fetchall()
    conn.close()
    return [row[0] for row in rows]

def get_embeddings(names):
    response = client.embeddings.create(
        model=OPENAI_MODEL,
        input=names
    )
    return [r.embedding for r in response.data]

def cluster_embeddings(names, embeddings, threshold=SIMILARITY_THRESHOLD):
    X = np.array(embeddings)
    cosine_sim = cosine_similarity(X)
    distance_matrix = np.clip(1 - cosine_sim, 0, 1)
    clustering = DBSCAN(eps=1-threshold, min_samples=1, metric='precomputed')
    labels = clustering.fit_predict(distance_matrix)

    clustered = {}
    for idx, label in enumerate(labels):
        clustered.setdefault(label, []).append(names[idx])
    return clustered

def assign_canonical_names(clusters):
    mapping = {}
    for group in clusters.values():
        canonical = sorted(group, key=len)[0]
        for variant in group:
            mapping[variant] = canonical
    return mapping

def save_mapping_to_db(mapping):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for variant, canonical in mapping.items():
        c.execute("""
            INSERT OR REPLACE INTO item_normalization (variant_name, canonical_name)
            VALUES (?, ?)
        """, (variant, canonical))
    conn.commit()
    conn.close()
