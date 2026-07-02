# this is where the chunks actually become vectors and get saved to somewhere
# we can search later
# Main ideas are, sentense transformers where txt are turned into numbers
# chromaDb stores these numbera and knows hoe to seach them

import chromadb# this is our vector database
from chromadb.utils import embedding_functions

# PersistentClient -  means that chroma writes everything on the disk, in the folder
# even if you stop the server, later on your uploaded documents are still there.
client = chromadb.PersistentClient(path = './data/chroma_db')

# creating an embedding function-something Chroma can call automatically any
# time we add or search to turn text into vector
embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name = "all-MiniLM-L6-v2")

# collection in chromadb is like a table in database
# get_or_create_collection - if a collection named documents in our case already exists, reuse it else create a new one.
collection = client.get_or_create_collection(name='documents')

# add_chunk for saving chunks in the vectordb
def add_chunks(doc_id: str, chunks: list[str]):

    # create a unique ID for every chunk
    # chromaDB requires every stored item to have a unique id
    ids = [f"{doc_id} {i}"for i in range(len(chunks))]
    # create a metadata dictionary for each chunk
    # "source" - which file the chunk came from
    # chunk_index - position of this chunk within the file
    metadatas = [{"source": doc_id, "chunk_index": i}for i in range(len(chunks))]

    # actually inserts data into ChromaDB
    # documents = chunks - the raw text (gets embedded automatically using embedding_fn)
    collection.add(documents = chunks, metadatas = metadatas, ids=ids)

    # return the count of chunks that were added
    return len(chunks)

# lets now write a function that will search
# search_chunks() - finding the closest chunk to a question
# query - is the question text, top_k - how many of the closest chunks to return
def search_chunks(query: str, top_k: int = 4):
    return collection.query(query_texts = [query], n_results = top_k)

