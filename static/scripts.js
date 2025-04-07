const KEYWORDS = new Set([
    'lula', 'nine', 'molusco', 'bolsonaro',
    'presidiário', 'cachaceiro', 'socialismo', 'comunismo',
]);


const updateProgress = (percent) => {
    const progressBar = document.querySelector('.progress-bar');
    progressBar.style.width = `${percent}%`;
    progressBar.setAttribute('aria-valuenow', percent);
    progressBar.textContent = `${Math.round(percent)}%`;
};

const analyzeChat = (content) => {
    const counts = new Map();
    let currentSender = null;
    let currentMessage = [];
    const lines = content.split('\n');
    const messagePattern = /^(\d{2}\/\d{2}\/\d{4} \d{2}:\d{2}) - ([^:]+): (.*)$/;

    lines.forEach((line, index) => {
        const match = messagePattern.exec(line.trim());
        if (match) {
            processMessage(counts, currentSender, currentMessage);
            currentSender = match[2];
            currentMessage = [match[3].toLowerCase()];
        } else if (currentSender) {
            currentMessage.push(line.toLowerCase());
        }

        if (index % 100 === 0) {
            updateProgress((index / lines.length) * 100);
        }
    });

    processMessage(counts, currentSender, currentMessage);
    return formatResults(counts);
};

const processMessage = (counts, sender, message) => {
    if (sender && message.length > 0) {
        const fullMessage = message.join(' ').toLowerCase();
        for (const keyword of KEYWORDS) {
            if (fullMessage.includes(keyword)) {
                counts.set(sender, (counts.get(sender) || 0) + 1);
                break;
            }
        }
    }
};

const formatResults = (counts) => {
    return Array.from(counts.entries())
        .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
        .slice(0, 20); // Top 30 results
};

const showResults = (results) => {
    const tableRows = results.map(([participant, count], index) => `
        <tr>
            <td>${index + 1}</td>
            <td class="participant">${participant}</td>
            <td>${count}</td>
        </tr>
    `).join('');

    const html = `
        <div class="card">
            <div class="card-header bg-primary text-white">
                Resultados - ${results.length} participantes
            </div>
            <div class="card-body">
                <table class="table table-hover">
                    <thead>
                        <tr>
                            <th>Rank</th>
                            <th>Participante</th>
                            <th>Menções</th>
                        </tr>
                    </thead>
                    <tbody>${tableRows}</tbody>
                </table>
            </div>
        </div>
    `;
    document.getElementById('results-container').innerHTML = html;
};

document.getElementById('upload').addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (!file) return;

    document.getElementById('progress').style.display = 'block';
    updateProgress(0);

    const reader = new FileReader();
    reader.onprogress = (e) => {
        if (e.lengthComputable) {
            updateProgress((e.loaded / e.total) * 100);
        }
    };
    reader.onload = () => {
        try {
            const results = analyzeChat(reader.result);
            showResults(results);
        } catch (error) {
            alert(`Erro na análise: ${error.message}`);
        } finally {
            document.getElementById('progress').style.display = 'none';
        }
    };
    reader.onerror = () => {
        alert('Erro na leitura do arquivo!');
        document.getElementById('progress').style.display = 'none';
    };
    reader.readAsText(file, 'UTF-8');
});