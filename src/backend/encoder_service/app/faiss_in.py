import faiss
import numpy as np
import os

class Faiss():
    def __init__(self):
        self.indices = []
        try: 
            for idx in range(4):
                index = faiss.read_index(f'/code/app/faiss_index/index_{idx}.faiss')
                self.indices.append(index)
            self.counter = index.ntotal
        except Exception as e:
            print(f"Ошибка при загрузке индексов: {e}")
            self.indices = [faiss.IndexFlatL2(512) for _ in range(4)]
            self.counter = 0

    def normalize_vectors(self, vectors):
        vectors = np.atleast_2d(vectors)  # Преобразуем вектора в двумерный массив, если он еще не таков
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        return vectors / np.where(norms == 0, 1, norms)
        
    def save_index_to_file(self):
        for idx, index in enumerate(self.indices):
            file_path = f'/code/app/faiss_index/index_{idx}.faiss'
            print(f"Trying to save index to {file_path}")
            print("Current working directory:", os.getcwd())
            print("Directory contents:", os.listdir('/code/app/faiss_index/'))
            faiss.write_index(index, file_path)
        
    def write_indexx(self, embeddings,ind):
        for idx, emb in enumerate(embeddings):
            if idx not in ind:
                continue
            if isinstance(emb, np.ndarray):
                if emb.ndim == 1:
                    emb = emb.reshape(1, -1)
            else:
                emb = np.array(emb)
                if emb.ndim == 1:
                    emb = emb.reshape(1, -1)
            emb = np.atleast_2d(emb)
            #print("--------",emb.shape)
            self.indices[idx].add(emb)
        
        if self.counter % 10 == 0:
            self.save_index_to_file()
        self.counter += 1
    
    def search_all(self, query_embeddings, k=10):
        results = []
        Dd = []
        for index, query in zip(self.indices, query_embeddings):
            if index.ntotal==0:
                print("faiss пуст")
                return False
            D, I = index.search(np.array(query).reshape(1, -1), k)
            results.append(I.tolist()[0])
            Dd.append(D.tolist()[0])
        result = set([item for sublist in results for item in sublist])
        print(Dd,results)
        vector = []
        key = []
        number = []
        for resu in result:
            for i in range(4):
                if i==0:
                    vector.append(np.linalg.norm(query_embeddings[i]-self.indices[i].reconstruct(resu))/1.35)
                elif i==1:
                    vector.append(np.linalg.norm(query_embeddings[i]-self.indices[i].reconstruct(resu))*1.2)
                elif i==3:
                    vector.append(np.linalg.norm(query_embeddings[i]-self.indices[i].reconstruct(resu))*1.15)
                else:
                    vector.append(np.linalg.norm(query_embeddings[i]-self.indices[i].reconstruct(resu)))
                key.append(resu+1)
                number.append(i)

       # print(vector)
        ln = len(vector)
        for i in range(ln-1):
            for j in range(ln-1-i):
                if vector[j] > vector[j+1]:
                    vector[j], vector[j+1] = vector[j+1], vector[j]
                    key[j], key[j+1] = key[j+1], key[j]
                    number[j], number[j+1] = number[j+1], number[j]
        
        vectors = []
        keys = []
        numbers = []
        uniq = []
        for i in range(ln):
            if key[i] not in uniq:
                vectors.append(vector[i])
                keys.append(key[i])
                numbers.append(number[i])
                uniq.append(key[i])
        print(vectors,keys,numbers)
        return keys[:10]
    
    def search_four(self, query_embeddings, k=4):
        results = []
        for index, query in zip(self.indices, query_embeddings):
            if index.ntotal==0:
                print("faiss пуст")
                return False
            D, I = index.search(np.array(query).reshape(1, -1), k)
            results.append(I.tolist()[0])
            
        result = [0,0,0,0]
        for i in range(4):
            for z in range(4):
                if results[i][z] not in result:
                    result[i]=results[i][z]+1
                    continue
            
        return result