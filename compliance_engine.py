import chromadb
from chromadb.utils import embedding_functions
import os

# Initialize ChromaDB
client = chromadb.PersistentClient(path="./compliance_db")

# Use a simple default embedding function (sentence-transformers)
# Note: In a real environment, you'd use a more robust one or an API
ef = embedding_functions.DefaultEmbeddingFunction()

collection = client.get_or_create_collection(name="ride_hailing_regs", embedding_function=ef)

def populate_compliance_data():
    """Populate ChromaDB with ride-hailing regulations and security info"""
    regs = [
        {
            "id": "reg1",
            "text": "All ride-hailing vehicles entering the Red Zone (G-5, F-5) must have a valid ICT Administration E-Tag.",
            "metadata": {"category": "security", "zones": ["red", "G-5", "F-5"]}
        },
        {
            "id": "reg2",
            "text": "Vehicles registered outside Islamabad/Rawalpindi may be subject to additional security checks at city entry points (I-8, Faizabad).",
            "metadata": {"category": "security", "zones": ["I-8", "Faizabad"]}
        },
        {
            "id": "reg3",
            "text": "Bike-sharing services are strictly prohibited from carrying more than one passenger.",
            "metadata": {"category": "safety", "vehicle": "bike"}
        },
        {
            "id": "reg4",
            "text": "Night-time travel (after 10 PM) in diplomatic areas requires valid ID and destination proof.",
            "metadata": {"category": "security", "zones": ["diplomatic", "F-5"]}
        },
        {
            "id": "reg5",
            "text": "Standard AC car fares are regulated by the local administration to prevent overcharging during peak summer months.",
            "metadata": {"category": "regulation", "vehicle": "car"}
        }
    ]
    
    for reg in regs:
        collection.upsert(
            documents=[reg["text"]],
            metadatas=[reg["metadata"]],
            ids=[reg["id"]]
        )

def get_compliance_notes(query_text, zones=None):
    """Query ChromaDB for relevant regulations based on route or zones"""
    results = collection.query(
        query_texts=[query_text],
        n_results=2
    )
    
    notes = []
    if results["documents"]:
        for doc_list in results["documents"]:
            notes.extend(doc_list)
            
    return list(set(notes)) # Unique notes

if __name__ == "__main__":
    populate_compliance_data()
    print("Compliance database populated.")
