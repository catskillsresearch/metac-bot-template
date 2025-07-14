from sentence_transformers import SentenceTransformer
import numpy as np
import faiss

# Load index and titles
index = faiss.read_index("wikipedia/wiki_titles.index")
titles = [line.strip().replace('_',' ')
          for line in open("wikipedia/enwiki-20250701-all-titles-in-ns0", encoding="utf-8")]

# Load model and encode query
model = SentenceTransformer("all-MiniLM-L6-v2")
query = "origin of the coronavirus pandemic"
vec = model.encode([query], convert_to_numpy=True).astype("float32")
faiss.normalize_L2(vec)

# Search
D, I = index.search(vec, k=10)

# Show results
for i, score in zip(I[0], D[0]):
    print(f"{titles[i]} (score={score:.4f})")
