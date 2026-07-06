const fs = require('fs');
const path = require('path');

const targetDir = __dirname + '/src';

const renames = [
    ['components/VaaniAgent', 'components/JanAIAgent'],
    ['components/JanAIAgent/VaaniWidget.jsx', 'components/JanAIAgent/JanAIWidget.jsx'],
    ['components/icons/VaaniIcons.jsx', 'components/icons/JanAIIcons.jsx'],
    ['../public/models/vaani.glb', '../public/models/janai.glb']
];

renames.forEach(([oldPath, newPath]) => {
    const fullOld = path.join(targetDir, oldPath);
    const fullNew = path.join(targetDir, newPath);
    if (fs.existsSync(fullOld)) {
        fs.renameSync(fullOld, fullNew);
    }
});

function walk(dir) {
    let results = [];
    const list = fs.readdirSync(dir);
    list.forEach(file => {
        file = path.join(dir, file);
        const stat = fs.statSync(file);
        if (stat && stat.isDirectory()) {
            results = results.concat(walk(file));
        } else {
            if (file.endsWith('.jsx') || file.endsWith('.js') || file.endsWith('.css') || file.endsWith('.html')) {
                results.push(file);
            }
        }
    });
    return results;
}

const files = walk(targetDir).concat([path.join(__dirname, 'index.html')]);

files.forEach(file => {
    try {
        const content = fs.readFileSync(file, 'utf8');
        let newContent = content;

        newContent = newContent.replaceAll('VaaniSeva', 'JanAI');
        newContent = newContent.replaceAll('vaaniseva', 'janai');
        newContent = newContent.replaceAll('VAANISEVA', 'JANAI');
        newContent = newContent.replaceAll('AI for Bharat Hackathon 2026', 'JanAI');
        newContent = newContent.replaceAll('AI for Bharat', 'JanAI');
        newContent = newContent.replaceAll('Vaani', 'JanAI');
        newContent = newContent.replaceAll('vaani', 'janai');
        newContent = newContent.replaceAll('978 830 9619', '831 298 8145');
        newContent = newContent.replaceAll('9788309619', '8312988145');

        if (file.includes('AvatarModel.jsx')) {
            newContent = newContent.replaceAll("modelUrl = '/models/janai.glb?v=2'", "modelUrl = '/models/janai.glb'");
            newContent = newContent.replaceAll("position = [0, 0, 0]", "position = [0, -1.5, 0]");
            newContent = newContent.replaceAll("position[1], position[2]", "position[1] - 1.5, position[2]");
            newContent = newContent.replaceAll("useGLTF.preload('/models/janai.glb?v=2')", "useGLTF.preload('/models/janai.glb')");
        }

        if (file.includes('JanAIWidget.jsx')) {
            newContent = newContent.replaceAll("/models/janai.glb?v=2", "/models/janai.glb");
        }

        if (file.includes('Home.jsx')) {
            newContent = newContent.replaceAll("30+", "50+");
            newContent = newContent.replaceAll("Government Schemes", "Verified Schemes");
            newContent = newContent.replaceAll("Always Available", "Action & Support");
            newContent = newContent.replaceAll("'4'", "'8'");
            newContent = newContent.replaceAll("500M+", "440M+");
            newContent = newContent.replaceAll(
                "Hundreds of millions of Indians have no smartphone, no internet, no access to digital services.",
                "India's AI Voice Layer for the Unconnected — a civic action layer, not just a chatbot. Check status, file complaints, and book visits in your own language."
            );
            newContent = newContent.replaceAll("Simple Process", "5 Specialized Agents");
            newContent = newContent.replaceAll(
                "Three steps. No app downloads. No internet required.",
                "Q&A and action execution (check status, file complaints, book visits). No app downloads."
            );
            newContent = newContent.replaceAll("Knowledge Base", "Knowledge & Action Base");
            newContent = newContent.replaceAll(
                "From crop prices to health coverage to legal rights — ask anything, in your language, right now.",
                "From crop prices to health coverage to filing labor complaints — our 5 specialized agents are ready to assist you."
            );
        }

        if (file.includes('index.html')) {
            newContent = newContent.replaceAll("500M+", "440M+");
            newContent = newContent.replaceAll("farming advice, health info & more — in Hindi, Marathi, Tamil & English", "execute actions, and get support in 8 languages");
            newContent = newContent.replaceAll("farming, health & more", "file complaints, book visits, & more");
            newContent = newContent.replaceAll("access government scheme information", "access government scheme information and execute civic actions");
        }

        if (newContent !== content) {
            fs.writeFileSync(file, newContent, 'utf8');
            console.log("Updated " + file);
        }
    } catch (e) {
        console.error(e);
    }
});
