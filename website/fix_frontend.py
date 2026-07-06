import os
import re

target_dir = r"d:\Downloads\JanAI\JanAI\website\src"

# Rename files first so paths are correct
renames = [
    (r"components\VaaniAgent", r"components\JanAIAgent"),
    (r"components\JanAIAgent\VaaniWidget.jsx", r"components\JanAIAgent\JanAIWidget.jsx"),
    (r"components\icons\VaaniIcons.jsx", r"components\icons\JanAIIcons.jsx"),
    (r"..\public\models\vaani.glb", r"..\public\models\janai.glb")
]

for old, new in renames:
    old_path = os.path.join(target_dir, old)
    new_path = os.path.join(target_dir, new)
    if os.path.exists(old_path):
        os.rename(old_path, new_path)

def replace_in_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return
    
    new_content = content
    
    # 1. Global replacements
    new_content = new_content.replace('VaaniSeva', 'JanAI')
    new_content = new_content.replace('vaaniseva', 'janai')
    new_content = new_content.replace('VAANISEVA', 'JANAI')
    new_content = new_content.replace('AI for Bharat Hackathon 2026', 'JanAI')
    new_content = new_content.replace('AI for Bharat', 'JanAI')
    new_content = new_content.replace('Vaani', 'JanAI')
    new_content = new_content.replace('vaani', 'janai')
    new_content = new_content.replace('978 830 9619', '831 298 8145')
    new_content = new_content.replace('9788309619', '8312988145')
    
    # 2. AvatarModel fixes
    if "AvatarModel.jsx" in path:
        new_content = new_content.replace("modelUrl = '/models/janai.glb?v=2'", "modelUrl = '/models/janai.glb'")
        new_content = new_content.replace("position = [0, 0, 0]", "position = [0, -1.5, 0]")
        new_content = new_content.replace("position[1], position[2]", "position[1] - 1.5, position[2]")
        new_content = new_content.replace("useGLTF.preload('/models/janai.glb?v=2')", "useGLTF.preload('/models/janai.glb')")
    
    # 3. Widget fixes
    if "JanAIWidget.jsx" in path:
        new_content = new_content.replace("/models/janai.glb?v=2", "/models/janai.glb")
        
    # 4. Home.jsx fixes
    if "Home.jsx" in path:
        new_content = new_content.replace("30+", "50+")
        new_content = new_content.replace("Government Schemes", "Verified Schemes")
        new_content = new_content.replace("24/7", "24/7") # keep
        new_content = new_content.replace("Always Available", "Action & Support")
        new_content = new_content.replace("4", "8")
        new_content = new_content.replace("500M+", "440M+")
        new_content = new_content.replace(
            "Hundreds of millions of Indians have no smartphone, no internet, no access to digital services.",
            "India's AI Voice Layer for the Unconnected — a civic action layer, not just a chatbot. Check status, file complaints, and book visits in your own language."
        )
        new_content = new_content.replace("Simple Process", "5 Specialized Agents")
        new_content = new_content.replace(
            "Three steps. No app downloads. No internet required.",
            "Q&A and action execution (check status, file complaints, book visits). No app downloads."
        )
        new_content = new_content.replace("Knowledge Base", "Knowledge & Action Base")
        new_content = new_content.replace(
            "From crop prices to health coverage to legal rights — ask anything, in your language, right now.",
            "From crop prices to health coverage to filing labor complaints — our 5 specialized agents are ready to assist you."
        )
        # Correctly replace the avatar model import which might be wrong case now
        
    if new_content != content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {path}")

for root, dirs, files in os.walk(target_dir):
    for file in files:
        if file.endswith(('.jsx', '.js', '.css', '.html')):
            replace_in_file(os.path.join(root, file))

