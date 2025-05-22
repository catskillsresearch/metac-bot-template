import faiss, pickle, os, fcntl
import numpy as np
from datetime import datetime, timedelta
from pprint import pprint
from sentence_transformers import SentenceTransformer

class LockedSaveMixin:
    def _atomic_save(self, path, data, mode='wb'):
        """Atomic save with file locking"""
        tmp_path = f"{path}.tmp"
        with open(tmp_path, mode) as f:
            if hasattr(f, 'fileno'):  # Unix file locking
                fcntl.flock(f, fcntl.LOCK_EX)
            pickle.dump(data, f)
        os.replace(tmp_path, path)

class RAGForecaster(LockedSaveMixin):

    def _initialize_index(self):
        try:
            index = faiss.read_index(self.index_path)
            print(f"Loaded existing index from {self.index_path}")
            return index
        except (RuntimeError, FileNotFoundError):
            print("Creating new FAISS index")
            return faiss.IndexFlatIP(768)
            
    def __init__(self, index_path="forecast_index.faiss", metadata_path="rag_metadata.pkl"):
        self.index_path = index_path
        self.metadata_path = metadata_path
        self.index = self._initialize_index()
        self.encoder = SentenceTransformer('all-mpnet-base-v2')
        self.metadata = self._load_metadata()
        self._load_with_lock()
        self._last_refresh = datetime.now()
        print(f"Index contains {self.index.ntotal} vectors at initialization")

    def _load_with_lock(self):
        """Load index with shared lock for concurrent readers"""
        # FAISS loading
        if os.path.exists(self.index_path):
            try:
                with open(self.index_path, 'rb') as f:
                    if hasattr(f, 'fileno'):
                        fcntl.flock(f, fcntl.LOCK_SH)
                    self.index = faiss.read_index(self.index_path)
            except (RuntimeError, FileNotFoundError):
                pass
                
        # Metadata loading
        self.metadata = self._load_metadata()

    def save_state(self):
        # Atomic FAISS write
        tmp_index_path = f"{self.index_path}.tmp"
        faiss.write_index(self.index, tmp_index_path)
        os.replace(tmp_index_path, self.index_path)
        
        # Atomic metadata write with locking
        self._atomic_save(self.metadata_path, self.metadata)
        print(f"Atomically saved RAG state")

    def _load_metadata(self):
        try:
            with open(self.metadata_path, 'rb') as f:
                if hasattr(f, 'fileno'):  # Shared lock for readers
                    fcntl.flock(f, fcntl.LOCK_SH)
                return pickle.load(f)
        except FileNotFoundError:
            return []



    def add_to_index(self, text, question_id):
        embedding = self.encoder.encode(text)
        self.index.add(np.array([embedding]))
        self.metadata.append({
            'id_of_question': question_id,
            'timestamp': datetime.now(),
            'usage_count': 0,
            'success_score': 1.0,
            'embedding': embedding,
            'raw_text': text  # NEW: Store original text
        })
        
    def retrieve_context(self, query, k=3):
        """Returns (contexts, indices) for feedback tracking"""
        query_embed = self.encoder.encode(query)
        
        if self.index.ntotal == 0:  # Empty index check
            return [], []
            
        D, I = self.index.search(np.array([query_embed]), k)
        results = []
        valid_indices = []
        
        for i in I[0]:
            try:
                if D[0][i] > 0.4 and i < len(self.metadata):
                    results.append((self.metadata[i], D[0][i]))
                    valid_indices.append(i)
            except:
                pass
        
        return results, valid_indices
   
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


    def _update_success_scores(self, used_indices: list, forecast_accuracy: float):
        """Update scores using weighted formula: 60% accuracy, 30% usage, 10% recency"""
        now = datetime.now()
        for idx in used_indices:
            if 0 <= idx < len(self.metadata):
                entry = self.metadata[idx]
                
                # Calculate components
                usage_freq = np.log1p(entry['usage_count'])  # Logarithmic scale
                recency = 1 - (now - entry['timestamp']).days/365  # Yearly decay
                
                # Weighted formula
                feedback = (0.6 * forecast_accuracy +
                          0.3 * usage_freq +
                          0.1 * recency)
                
                # Apply update with EMA
                entry['success_score'] = 0.85 * entry['success_score'] + 0.15 * feedback
                entry['usage_count'] += 1
    
    def decay_scores(self):
        """Daily score decay for recency component"""
        for m in self.metadata:
            m['success_score'] *= 0.98  # 2% daily decay

    def generate_index_report(self):
        """Reports FAISS index health"""
        return {
            "index_type": str(self.index),
            "total_vectors": self.index.ntotal,
            "dimensions": self.index.d,
            "metadata_alignment": f"{len(self.metadata)}/{self.index.ntotal}",
            "needs_reindexing": self.index.ntotal != len(self.metadata)
        }

    def generate_metadata_report(self):
        """Analyze knowledge retention patterns"""
        if not self.metadata:
            return {"status": "No metadata available"}
        
        now = datetime.now()
        valid_entries = [m for m in self.metadata if all(k in m for k in ['timestamp', 'success_score', 'usage_count', 'id_of_question'])]
        
        if not valid_entries:
            return {"status": "No valid metadata entries"}
        
        age_days = [(now - m['timestamp']).days for m in valid_entries]
        success_scores = [m['success_score'] for m in valid_entries]
        usage_counts = [m['usage_count'] for m in valid_entries]
        unique_questions = set([m['id_of_question'] for m in valid_entries])
        
        return {
            "total_entries": len(valid_entries),
            "unique_question_ids": unique_questions,
            "entry_age_stats": {
                "oldest_days": max(age_days),
                "newest_days": min(age_days),
                "average_days": np.mean(age_days)
            },
            "success_score_distribution": {
                "min": np.min(success_scores),
                "max": np.max(success_scores),
                "mean": np.mean(success_scores),
                "quartiles": list(np.quantile(success_scores, [0.25, 0.5, 0.75]))
            },
            "usage_analysis": {
                "total_uses": sum(usage_counts),
                "most_used_entry": max(usage_counts) if usage_counts else 0,
                "unused_entries": sum(1 for c in usage_counts if c == 0)
            }
        }


    def generate_combined_report(self):
        """Comprehensive report for both index and metadata"""
        index_report = self.generate_index_report()
        metadata_report = self.generate_metadata_report()
        
        return {
            "system_health": {
                "vectors_metadata_alignment": index_report['total_vectors'] == len(self.metadata),
                "last_updated": max(m['timestamp'] for m in self.metadata) if self.metadata else None
            },
            "index": index_report,
            "knowledge_base": metadata_report,
            "performance_metrics": {
                "high_value_entries": len([m for m in self.metadata if m['success_score'] > 0.8]),
                "stale_entries": len([m for m in self.metadata if (datetime.now() - m['timestamp']).days > 30])
            }
        }

    def dump_learning_texts(self, max_age_days=30):
        """Export readable learning texts with usage metrics"""
        cutoff = datetime.now() - timedelta(days=max_age_days)
        return [
            {
                'text': m['raw_text'],
                'id': m['id_of_question'],
                'last_used': m['timestamp'].strftime('%Y-%m-%d'),
                'score': m['success_score']
            }
            for m in self.metadata 
            if m['timestamp'] > cutoff and 'raw_text' in m
        ]

    def print_detailed_report(self):
        """Human-readable formatted report
        Sample output would look like:
        =============== RAG System Report ===============
        Index contains 1524 vectors (768D)
        Metadata has 1524 entries across 89 questions
        
        Top Performing Contexts:
        1. QX-229: Score 0.94 (12 uses)
        2. QF-112: Score 0.91 (8 uses) 
        3. QR-445: Score 0.89 (15 uses)
        
        System Health Check:
        ✅ Vector/Metadata alignment
        Last update: 2025-05-20 19:15:32.458212
        
        Retention Statistics:
        High value entries: 423
        Stale entries (>30d): 67
        """
        
        report = self.generate_combined_report()
        
        print(f"\n{' RAG System Report ':=^60}")
        print(f"Index contains {report['index']['total_vectors']} vectors ({report['index']['dimensions']}D)")
        try:
            n_active = len(report["knowledge_base"]["unique_question_ids"])
        except:
            n_active = 0
        print(f"Metadata has {len(self.metadata)} entries across {n_active} questions\n")
        
        print("Top Performing Contexts:")
        top_entries = sorted(self.metadata, key=lambda x: x['success_score'], reverse=True)[:3]
        for i, entry in enumerate(top_entries, 1):
            print(f"{i}. Q{entry['id_of_question']}: Score {entry['success_score']:.2f} ({entry['usage_count']} uses)")
        
        print("\nSystem Health Check:")
        status = "✅" if report['system_health']['vectors_metadata_alignment'] else "❌"
        print(f"{status} Vector/Metadata alignment")
        print(f"Last update: {report['system_health']['last_updated'] or 'Never'}")
        
        print("\nRetention Statistics:")
        print(f"High value entries: {report['performance_metrics']['high_value_entries']}")
        print(f"Stale entries (>30d): {report['performance_metrics']['stale_entries']}")

        # Raw data access
        print("\nIndex Structure:")
        pprint(self.generate_index_report())
        print("\nKnowledge Stats:")
        pprint(self.generate_metadata_report())
        print("\nRecent learning texts:")
        pprint(self.dump_learning_texts(max_age_days=7))
        
        # Save reports to file
        import json
        with open('rag_system_report.json', 'w') as f:
            json.dump(report, f, indent=4, default=str)

    def check_for_updates(self):
        """Returns True if files changed since last check"""
        current_index_mtime = os.path.getmtime(self.index_path) 
        current_metadata_mtime = os.path.getmtime(self.metadata_path)
        
        changed = (current_index_mtime > self._last_refresh.timestamp() or
                  current_metadata_mtime > self._last_refresh.timestamp())
        
        if changed:
            self._last_refresh = datetime.now()
            
        return changed

if __name__=="__main__":
    forecaster = RAGForecaster()
    forecaster.save_state() 
    forecaster.print_detailed_report()


