#!/bin/bash -x

BUNDLE_DIR="glimt/wikipedia/bundles"

for bundle_file in "$BUNDLE_DIR"/bundle_*.txt; do
    output_file="${bundle_file%.txt}_embeddings.npy"
    python encode_bundle.py "$bundle_file" "$output_file"
done

