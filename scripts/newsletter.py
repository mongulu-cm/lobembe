
import re
from bs4 import BeautifulSoup
import requests

def extract_messages_with_links_whatsapp(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    link_pattern = re.compile(r'http|www')
    messages_with_links = [line for line in lines if link_pattern.search(line)]
    
    formatted_messages = []
    for message in messages_with_links:
        parts = message.split(" - ", 1)
        if len(parts) == 2:
            _, message_content = parts
            link_match = link_pattern.search(message_content)
            if link_match:
                start_idx = link_match.start()
                link = message_content[start_idx:].split()[0]
                message_without_name = message_content.split(": ", 1)[-1].split(link)[0].strip()
                formatted_messages.append(f"[{message_without_name}]({link})")

    formatted_messages_final = [message.replace(":", "").strip() for message in formatted_messages]
    output_file_path = file_path.replace(".txt", "_processed.txt")
    with open(output_file_path, "w", encoding="utf-8") as file:
        file.write("\n".join(formatted_messages_final))
    
    return output_file_path

def extract_info_from_links(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        links = file.readlines()

    results = []
    for link in links:
        link = link.strip()
        response = requests.get(link)
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title.string if soup.title else "No title"
        description_tag = soup.find("meta", attrs={"name": "description"})
        description = description_tag["content"] if description_tag else "No description"
        results.append(f"[{title}]({link}) - {description}")

    output_file_path = file_path.replace(".txt", "_info.txt")
    with open(output_file_path, "w", encoding="utf-8") as file:
        file.write("\n".join(results))
    
    return output_file_path

if __name__ == "__main__":
    choice = input("Choose the type of file (Enter 'whatsapp' for WhatsApp chat file or 'links' for links file): ").strip().lower()

    if choice == "whatsapp":
        file_path = input("Enter the path to the WhatsApp chat file: ")
        result_file = extract_messages_with_links_whatsapp(file_path)
        print(f"Processed messages saved to: {result_file}")
    elif choice == "links":
        file_path = input("Enter the path to the links file: ")
        result_file = extract_info_from_links(file_path)
        print(f"Link information saved to: {result_file}")
    else:
        print("Invalid choice!")

