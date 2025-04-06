import re
from collections import defaultdict

def process_chat_file(file_content):
    message_pattern = re.compile(
        r'^(\d{2}/\d{2}/\d{4} \d{2}:\d{2}) - ([^:]+): (.*)$'
    )
    keywords = {"lula", "nine", "molusco", "bolsonaro", "presidiário", "cachaceiro", "socialismo", "comunismo"}
    
    counts = defaultdict(int)
    current_sender = None
    current_message = []
    
    for line in file_content.split('\n'):
        line = line.strip()
        if not line:
            continue
            
        match = message_pattern.match(line)
        if match:
            if current_sender is not None:
                full_message = ' '.join(current_message).lower()
                if any(kw in full_message for kw in keywords):
                    counts[current_sender] += 1
            
            current_sender = match.group(2)
            current_message = [match.group(3).lower()]
        elif current_sender:
            current_message.append(line.lower())
    
    # Process final message
    if current_sender:
        full_message = ' '.join(current_message).lower()
        if any(kw in full_message for kw in keywords):
            counts[current_sender] += 1
    
    return counts

def generate_results_html(counts):
    if not counts:
        return '<p class="text-danger">Nenhuma menção encontrada!</p>'
    
    sorted_counts = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
    
    # Minified HTML output
    html = [
        '<table class=table table-striped>',
        '<thead><tr><th>Rank</th><th>Participante</th><th>Menções</th></tr></thead>',
        '<tbody>'
    ]
    
    for rank, (participant, count) in enumerate(sorted_counts[:20], 1):
        html.append(
            f'<tr><td>{rank}</td>'
            f'<td>{participant[:30]}</td>'  # Truncate long names
            f'<td>{count}</td></tr>'
        )
    
    html.append('</tbody></table>')
    return ''.join(html)  # No newlines for minification