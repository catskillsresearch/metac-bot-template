import faiss, pickle
import numpy as np
from datetime import datetime, timedelta
from EnhancedResearchPro import EnhancedResearchPro

class RAGForecaster:
    def __init__(self, index_path="forecast_index.faiss", metadata_path="rag_metadata.pkl"):
        self.index_path = index_path
        self.metadata_path = metadata_path

        from sentence_transformers import SentenceTransformer
        self.encoder = SentenceTransformer('all-mpnet-base-v2')
        self.index = self._initialize_index()
        self.metadata = self._load_metadata()
        
    def _initialize_index(self):
        try:
            index = faiss.read_index(self.index_path)
            print(f"Loaded existing index from {self.index_path}")
            return index
        except (RuntimeError, FileNotFoundError):
            print("Creating new FAISS index")
            return faiss.IndexFlatIP(768)
            
    def _load_metadata(self):
        try:
            with open(self.metadata_path, 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            return []
            
    def save_state(self):
        faiss.write_index(self.index, self.index_path)
        with open(self.metadata_path, 'wb') as f:
            pickle.dump(self.metadata, f)
        print(f"Saved RAG state to {self.index_path} and {self.metadata_path}")
        
    def add_to_index(self, text, question_id):
        embedding = self.encoder.encode(text)
        self.index.add(np.array([embedding]))
        self.metadata.append({
            'id': question_id,
            'timestamp': datetime.now(),
            'usage_count': 0,
            'success_score': 1.0,
            'embedding': embedding  # Stored for potential reclustering
        })
        
    def retrieve_context(self, query, k=3):
        query_embed = self.encoder.encode(query)
        D, I = self.index.search(np.array([query_embed]), k)
        results = []
        for i in I[0]:
            try:
                if D[0][i] > 0.4 and i < len(self.metadata):
                    results.append(self.metadata[i], D[0][i])
            except:
                break
        print("Context:", results)
        return results
        
    def prune_old_entries(self, max_age_days=30):
        cutoff = datetime.now() - timedelta(days=max_age_days)
        new_metadata = []
        keep_indices = []
        
        for i, m in enumerate(self.metadata):
            if m['timestamp'] > cutoff and m['success_score'] > 0.2:
                new_metadata.append(m)
                keep_indices.append(i)
                
        # Rebuild index with kept entries
        if keep_indices:
            new_embeddings = np.array([self.metadata[i]['embedding'] for i in keep_indices])
            self.index.reset()
            self.index.add(new_embeddings)
            
        self.metadata = new_metadata
        print(f"Pruned {len(keep_indices)}/{len(self.metadata)} entries remaining")