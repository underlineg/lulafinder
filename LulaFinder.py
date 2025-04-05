import re
from collections import defaultdict

message_pattern = re.compile(
    r'^(\d{2}/\d{2}/\d{4} \d{2}:\d{2}) - ([^:]+): (.*)$'
)

# All keywords in lowercase for case-insensitive matching
keywords = ["lula", "nine", "molusco", "lule" ,"presidiário", "cachaceiro"]

def process_chat_file(file_path):
    counts = defaultdict(int)
    current_sender = None
    current_message = []
    total_messages = 0

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            match = message_pattern.match(line)
            
            if match:
                if current_sender is not None:
                    full_message = ' '.join(current_message).lower()
                    if any(keyword in full_message for keyword in keywords):
                        counts[current_sender] += 1
                
                current_sender = match.group(2)
                current_message = [match.group(3).lower()]  # Convert to lowercase immediately
                total_messages += 1
            else:
                if current_sender is not None:
                    current_message.append(line.lower())  # Accumulate lowercase

        # Process last message
        if current_sender is not None:
            full_message = ' '.join(current_message)
            if any(keyword in full_message for keyword in keywords):
                counts[current_sender] += 1

    print(f"Debug: Found {sum(counts.values())} keyword matches in {total_messages} messages")
    return counts

def display_ranked_table(counts):
    if not counts:
        print("No matches found. Possible reasons:")
        print("- Keywords not present in chat")
        print("- All matches are in system messages")
        print("- File format still not matching")
        return
    
    sorted_counts = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
    
    print("\nRank | Participant | Messages Containing Keywords")
    print("-----|-------------|------------------------------")
    # Show top 20 results only
    for rank, (participant, count) in enumerate(sorted_counts[:20], 1):
        print(f"{rank:4} | {participant:11} | {count}")

if __name__ == "__main__":
    file_path = "chats.txt"  # UPDATE THIS PATH
    try:
        keyword_counts = process_chat_file(file_path)
        display_ranked_table(keyword_counts)
    except Exception as e:
        print(f"Error: {str(e)}")