import json, glob
from pathlib import Path
from sentence_transformers import SentenceTransformer
import faiss

FILES = sorted(glob.glob("data/profiles/*.md"))
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

texts, ids = [], []
for path in FILES:
    t = Path(path).read_text()
    texts.append(t); ids.append(path)

if not texts:
    Path("vector").mkdir(parents=True, exist_ok=True)
    Path("vector/meta.json").write_text(json.dumps({"files": []}, indent=2))
    print("No profiles yet.")
else:
    emb = model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
    index = faiss.IndexFlatIP(emb.shape[1])
    index.add(emb)
    Path("vector").mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, "vector/index.faiss")
    Path("vector/meta.json").write_text(json.dumps({"files": ids}, indent=2))
    print(f"Indexed {len(ids)} profiles.")
