from sentence_transformers import SentenceTransformer
import numpy as np
import faiss, datetime
from get_wiki_page import get_wiki_page

print("loading massive wiki index", datetime.datetime.now())
index = faiss.read_index("glimt/wikipedia/wiki_titles.index")

print("loading wiki article titles", datetime.datetime.now())
with open('glimt/wikipedia/titles.txt', 'r') as f:
    titles = [x.strip() for x in f.readlines()]

print("loading sentence transformer model", datetime.datetime.now())
model = SentenceTransformer("all-MiniLM-L6-v2")

print("done", datetime.datetime.now())

def wiki_semantic_search(title_plus_criteria, k=10):
    vec = model.encode([title_plus_criteria], convert_to_numpy=True).astype("float32")
    faiss.normalize_L2(vec)
    
    D, I = index.search(vec, k=k)
    
    return [(score, titles[i], get_wiki_page(titles[i])) 
            for i, score in zip(I[0], D[0])]