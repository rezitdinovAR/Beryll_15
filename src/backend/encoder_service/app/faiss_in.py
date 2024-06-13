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
            print(idx,emb)
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
    
    def search_all(self, query_embeddings, k=10):
        results = []
        for index, query in zip(self.indices, query_embeddings):
            D, I = index.search(np.array([query]), k)
            results.append(I.tolist())
        
        result = list(set(sum(results, [])))
        vectors = {int_your_specific_index:np.mean([np.linalg.norm(query_embeddings[i]-self.indices[i].reconstruct(int_your_specific_index)) for i in range(4)]) for int_your_specific_index in result}
        top = sorted(vectors, key=vectors.get)
        print(top)
        return top