import os
import glob
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

class RAGEngine:
    def __init__(self, model_name='all-MiniLM-L6-v2', knowledge_dir='knowledge_base'):
        self.model = SentenceTransformer(model_name)
        self.knowledge_dir = knowledge_dir
        self.index = None
        self.chunks = []
        self.index_path = os.path.join(knowledge_dir, "vector_index.faiss")
        self.chunks_path = os.path.join(knowledge_dir, "chunks.txt")
        
        # Load or create index
        if os.path.exists(self.index_path) and os.path.exists(self.chunks_path):
            self.load_index()
        else:
            self.rebuild_index()

    def rebuild_index(self):
        print("Rebuilding Knowledge Base Index...")
        files = glob.glob(os.path.join(self.knowledge_dir, "*.txt")) + \
                glob.glob(os.path.join(self.knowledge_dir, "*.md"))
        
        all_text = ""
        for file in files:
            with open(file, 'r') as f:
                all_text += f.read() + "\n\n"
        
        if not all_text.strip():
            print("Knowledge base is empty.")
            return

        # Simple chunking by paragraph/newline
        self.chunks = [c.strip() for c in all_text.split("\n\n") if len(c.strip()) > 20]
        
        if not self.chunks:
            return

        embeddings = self.model.encode(self.chunks)
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(np.array(embeddings).astype('float32'))
        
        # Save for later
        faiss.write_index(self.index, self.index_path)
        with open(self.chunks_path, 'w') as f:
            f.write("\n---CHUNK_SPLIT---\n".join(self.chunks))

    def load_index(self):
        self.index = faiss.read_index(self.index_path)
        with open(self.chunks_path, 'r') as f:
            self.chunks = f.read().split("\n---CHUNK_SPLIT---\n")

    def query(self, text, top_k=3):
        if self.index is None or not self.chunks:
            return ""
        
        query_embedding = self.model.encode([text])
        distances, indices = self.index.search(np.array(query_embedding).astype('float32'), top_k)
        
        results = []
        for i in indices[0]:
            if i != -1 and i < len(self.chunks):
                results.append(self.chunks[i])
        
        return "\n\n".join(results)
