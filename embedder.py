
from sentence_transformers import SentenceTransformer

class EmbedderService:
    def __init__(self):
        self.model = SentenceTransformer('all-mpnet-base-v2')

    def generate_vector(self, text: str) -> list[float]:
        new_vec_list = self.model.encode(text).tolist()
        return new_vec_list