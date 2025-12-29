import os

def find_string_in_files(search_str, root_dir):
    found_files = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.py') or file.endswith('.md') or file.endswith('.sh'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        if search_str in f.read():
                            found_files.append(file_path)
                except Exception:
                    pass
    return found_files

if __name__ == "__main__":
    search_term = "vllm_url"
    results = find_string_in_files(search_term, ".")
    print(f"Searching for '{search_term}'...")
    if results:
        for r in results:
            print(f"FOUND in: {r}")
    else:
        print("No matches found.")
