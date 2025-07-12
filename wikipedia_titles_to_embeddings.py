import numpy as np
import torch
from tqdm import tqdm
from sentence_transformers import SentenceTransformer

with open('glimt/wikipedia/enwiki-20250701-all-titles-in-ns0', 'r') as f:
    titles = [x[0:-1].replace('_', ' ') for x in f.readlines()[1:]]

# Load model (choose one optimized for short phrases)
model = SentenceTransformer("all-MiniLM-L6-v2")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

batch_size = 1000
embeddings = []

for i in tqdm(range(0, len(titles), batch_size), total=(len(titles) + batch_size - 1) // batch_size):
    batch = titles[i:i + batch_size]
    emb = model.encode(
        batch,
        convert_to_numpy=True,
        batch_size=batch_size,
        device=device,
        show_progress_bar=False  # tqdm already shows progress
    )
    embeddings.append(emb)

# Combine into single matrix
all_embeddings = np.vstack(embeddings)


# Save
all_embeddings = np.vstack(embeddings)
np.save("wiki_title_embeddings.npy", all_embeddings)
with open("wiki_titles.txt", "w", encoding="utf-8") as f:
    f.writelines(t + "\n" for t in titles)
