import os
from tqdm import tqdm

input_file = 'wikipedia/enwiki-20250701-all-titles-in-ns0'
output_dir = 'wikipedia/bundles'
os.makedirs(output_dir, exist_ok=True)

with open(input_file, 'r', encoding='utf-8') as f:
    titles = [x.strip().replace('_', ' ') for x in f.readlines()[1:]]

num_bundles = 20
bundle_size = (len(titles) + num_bundles - 1) // num_bundles

for i in tqdm(range(num_bundles)):
    start = i * bundle_size
    end = min((i + 1) * bundle_size, len(titles))
    bundle_titles = titles[start:end]
    bundle_file = os.path.join(output_dir, f'bundle_{i}.txt')
    with open(bundle_file, 'w', encoding='utf-8') as bf:
        bf.writelines(t + '\n' for t in bundle_titles)
