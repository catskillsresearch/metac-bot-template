import sys
import numpy as np
import torch
from tqdm import tqdm
from sentence_transformers import SentenceTransformer

bundle_file = sys.argv[1]
output_file = sys.argv[2]

model = SentenceTransformer("all-MiniLM-L6-v2")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

with open(bundle_file, 'r', encoding='utf-8') as f:
    titles = [line.strip() for line in f.readlines()]

batch_size = 2000
embeddings = []

for i in tqdm(range(0, len(titles), batch_size), total=(len(titles) + batch_size - 1) // batch_size):
    batch = titles[i:i + batch_size]
    emb = model.encode(
        batch,
        convert_to_numpy=True,
        batch_size=batch_size,
        device=device,
        show_progress_bar=False
    )
    embeddings.append(emb)

all_embeddings = np.vstack(embeddings)
np.save(output_file, all_embeddings)
