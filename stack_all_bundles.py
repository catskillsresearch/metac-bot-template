import numpy as np
import os
from tqdm import tqdm

bundle_dir = 'glimt/wikipedia/bundles'
num_bundles = 20

# First, determine the shape and dtype of your embeddings
# For example, let's assume each bundle has shape (N, D)
sample_emb = np.load(os.path.join(bundle_dir, 'bundle_0_embeddings.npy'))
bundle_shape = sample_emb.shape
dtype = sample_emb.dtype

# Calculate total rows
total_rows = 0
for i in range(num_bundles):
    emb_file = os.path.join(bundle_dir, f'bundle_{i}_embeddings.npy')
    emb = np.load(emb_file, mmap_mode='r')
    total_rows += emb.shape[0]

# Create a memory-mapped file for output
output_path = os.path.join('glimt/wikipedia', 'wiki_title_embeddings.npy')
all_embeddings = np.memmap(output_path, dtype=dtype, mode='w+', shape=(total_rows, bundle_shape[1]))

# Write each bundle into the correct slice of the memmap
start = 0
for i in tqdm(range(num_bundles)):
    emb_file = os.path.join(bundle_dir, f'bundle_{i}_embeddings.npy')
    emb = np.load(emb_file)
    end = start + emb.shape[0]
    all_embeddings[start:end] = emb
    start = end

# Flush changes to disk
all_embeddings.flush()

# Re-open the memmap file in read mode
all_embeddings = np.memmap(output_path, dtype=dtype, mode='r', shape=(total_rows, bundle_shape[1]))

# Save as a proper .npy file
np.save(os.path.join('glimt/wikipedia', 'wiki_title_embeddings_clean.npy'), np.array(all_embeddings))
