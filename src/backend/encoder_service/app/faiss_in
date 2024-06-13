import faiss
import numpy as np
import os

class Faiss():
    def __init__(self):
        self.indices = []
        try: 
            for idx in range(4):
                index = faiss.read_index(f'/app/faiss_index/index_{idx}.faiss')
                self.indices.append(index)
            self.counter = index.ntotal
        except Exception as e:
            print(f"Ошибка при загрузке индексов: {e}")
            self.indices = [faiss.IndexFlatL2(512) for _ in range(4)]
            self.counter = 0

    def save_index_to_file(self):
        for idx, index in enumerate(self.indices):
            file_path = f'/code/app/faiss_index/index_{idx}.faiss'
            print(f"Trying to save index to {file_path}")
            print("Current working directory:", os.getcwd())
            print("Directory contents:", os.listdir('/code/app/faiss_index/'))
            faiss.write_index(index, file_path)
        
    def write_indexx(self, embeddings):
        for idx, emb in enumerate(embeddings):
            print(idx)
            if isinstance(emb, np.ndarray):
                if emb.ndim == 1:
                    emb = emb.reshape(1, -1)
            else:
                emb = np.array(emb)
                if emb.ndim == 1:
                    emb = emb.reshape(1, -1)
        self.indices[idx].add(emb)
        
        if self.counter % 10 == 0:
            self.save_index_to_file()
        self.counter += 1
    
    def search_all(indices, query_embeddings, k=10):
        results = []
        results_D = []
        for index, query in zip(indices, query_embeddings):
            D, I = index.search(np.array([query]), k)
            results.append(I.tolist())
        
        result = list(set(sum(results, [])))
        
        return results, results_D