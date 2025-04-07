import re
from collections import defaultdict

def process_chat_file(file_content):
    message_pattern = re.compile(r'^(\d{2}/\d{2}/\d{4} \d{2}:\d{2}) - ([^:]+): (.*)$')
    keywords = ["lula", "nine", "molusco", "bolsonaro", "presidiário", "cachaceiro"]
    
    counts = defaultdict(int)
    current_sender = None
    current_message = []
    
    for line in file_content.split('\n'):
        line = line.strip()
        match = message_pattern.match(line)
        
        if match:
            if current_sender is not None:
                full_message = ' '.join(current_message).lower()
                if any(keyword in full_message for keyword in keywords):
                    counts[current_sender] += 1
            
            current_sender = match.group(2)
            current_message = [match.group(3).lower()]
        else:
            if current_sender is not None:
                current_message.append(line.lower())
    
    if current_sender is not None:
        full_message = ' '.join(current_message).lower()
        if any(keyword in full_message for keyword in keywords):
            counts[current_sender] += 1
    
    return counts

def generate_results_html(counts):
    if not counts:
        return "<p>Nenhuma menção encontrada aos termos políticos!</p>"
    
    sorted_counts = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
    
    html = ['<table class="table table-striped mt-4">']
    html.append('<thead><tr><th>Rank</th><th>Participante</th><th>Menções</th></tr></thead>')
    html.append('<tbody>')
    
    for rank, (participant, count) in enumerate(sorted_counts[:20], 1):
        html.append(f'<tr><td>{rank}</td><td>{participant}</td><td>{count}</td></tr>')
    
    html.append('</tbody></table>')
    return '\n'.join(html)