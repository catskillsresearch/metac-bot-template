import faiss
import numpy as np

print("Load and normalize")
emb = np.load("glimt/wikipedia/wiki_title_embeddings_clean.npy", allow_pickle=True).astype("float32")
faiss.normalize_L2(emb)

print("Build FAISS IP index")
index = faiss.IndexFlatIP(emb.shape[1])
index.add(emb)

print("Save index")
faiss.write_index(index, "glimt/wikipedia/wiki_titles.index")

titles = [line.strip().replace('_',' ')
          for line in open("glimt/wikipedia/enwiki-20250701-all-titles-in-ns0", encoding="utf-8")]

with open('glimt/wikipedia/titles.txt', 'w') as f:
    f.write('\n'.join(titles))