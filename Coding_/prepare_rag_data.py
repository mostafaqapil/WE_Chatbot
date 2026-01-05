import os
from pathlib import Path

INPUT_DIR = "data/clean_text"
OUTPUT_DIR = "data/chunks"
CHUNK_SIZE = 500       
MIN_TEXT_LENGTH = 200  
os.makedirs(OUTPUT_DIR, exist_ok=True)
# chunks
def chunk_text(text, chunk_size=500):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i+chunk_size]).strip()
        if chunk:  
            chunks.append(chunk)
    return chunks
    
all_chunks = []
file_count = 0
chunk_count = 0

for file in os.listdir(INPUT_DIR):
    if not file.endswith(".txt"):
        continue
    file_count += 1
    file_path = os.path.join(INPUT_DIR, file)
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read().strip()
    if len(text) < MIN_TEXT_LENGTH:
        print(f" Skipped (too short): {file}")
        continue
    chunks = chunk_text(text, CHUNK_SIZE)
    for idx, chunk in enumerate(chunks):
        clean_chunk = "\n".join([line.strip() for line in chunk.split("\n") if line.strip()])
        if not clean_chunk:
            continue

        all_chunks.append({
            "content": clean_chunk,
            "source": "https://te.eg",
            "page": file.replace(".txt", ""),
            "chunk_id": idx
        })
        chunk_count += 1

    print(f" Processed: {file} → {len(chunks)} chunks")

output_file = os.path.join(OUTPUT_DIR, "we_chunks_final.txt")
with open(output_file, "w", encoding="utf-8") as f:
    for c in all_chunks:
        f.write(f"[SOURCE]: {c['source']} | [PAGE]: {c['page']} | [CHUNK]: {c['chunk_id']}\n")
        f.write(c["content"] + "\n" + "="*80 + "\n")

print(f"\n Total files processed: {file_count}")
print(f" Total chunks created: {chunk_count}")
print(f" Chunks saved to: {output_file}")
