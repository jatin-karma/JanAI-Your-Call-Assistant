import os
import re

target_dir = r"d:\Downloads\JanAI\JanAI"

def replace_in_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return
    
    new_content = content
    # Replace exact case first
    new_content = new_content.replace('JanAI', 'JanAI')
    new_content = new_content.replace('janai', 'janai')
    new_content = new_content.replace('JANAI', 'JANAI')
    
    # Also renaming files if needed, but the prompt just said "every mention of"
    
    if new_content != content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {path}")

for root, dirs, files in os.walk(target_dir):
    if '.git' in root or 'node_modules' in root:
        continue
    for file in files:
        if file.endswith(('.py', '.js', '.html', '.css', '.md', '.json', '.txt', '.example')):
            replace_in_file(os.path.join(root, file))
