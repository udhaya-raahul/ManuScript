import time
print("Checking libraries...")

start = time.time()
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    print(f"scikit-learn loaded in {time.time() - start:.2f}s")
except Exception as e:
    print(f"scikit-learn failed: {e}")

start = time.time()
try:
    import language_tool_python
    print("Initializing LanguageTool (may download server)...")
    tool = language_tool_python.LanguageTool('en-US')
    print(f"LanguageTool initialized in {time.time() - start:.2f}s")
except Exception as e:
    print(f"LanguageTool failed: {e}")

start = time.time()
try:
    from sentence_transformers import SentenceTransformer
    print("Loading SentenceTransformer model (may download)...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    print(f"SentenceTransformer loaded in {time.time() - start:.2f}s")
except Exception as e:
    print(f"SentenceTransformer failed: {e}")
