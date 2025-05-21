from RAGForecaster import RAGForecaster

def migrate_metadata(rag):
    """Convert existing error values to normalized success scores"""
    for m in rag.metadata:
        # Calculate normalized success score from stored error
        m['success_score'] = 1 - min(m.get('error', 1.0), 1.0)
        
    # Remove legacy error field if exists
    rag.metadata = [{k:v for k,v in item.items() if k != 'error'} 
                   for item in rag.metadata]
    
    print(f"Migrated {len(rag.metadata)} entries")

if __name__=="__main__":
    rag = RAGForecaster()
    migrate_metadata(rag)
    rag.save_state()
