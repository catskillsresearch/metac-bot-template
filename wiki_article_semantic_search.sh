!mkdir glimt/wikipedia
!cd glimt/wikipedia; wget https://dumps.wikimedia.org/enwiki/20250701/enwiki-20250701-all-titles-in-ns0.gz
!cd glimt/wikipedia; gunzip enwiki-20250701-all-titles-in-ns0.gz
!cd glimt/wikipedia; ls -l

big_wiki_titles_into_20_bundles.py
b.sh
    python encode_bundle.py "$bundle_file" "$output_file"
stack_all_bundles.py
build_faiss_index.py
query_index.py
