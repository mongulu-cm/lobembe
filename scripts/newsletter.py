import re
from bs4 import BeautifulSoup
import requests
from typing import List, Dict

# Function to manually split messages
def split_messages_manually(content: str) -> List[Dict[str, str]]:
    messages = []
    lines = content.split('\n')
    current_message = None

    for line in lines:
        match = re.match(r'\[(\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2})\] ([^:]+): (.*)', line)
        if match:
            if current_message:
                messages.append(current_message)
            current_message = {
                'timestamp': match.group(1),
                'username': match.group(2),
                'message': match.group(3)
            }
        else:
            if current_message:
                current_message['message'] += '\n' + line

    if current_message:
        messages.append(current_message)

    return messages


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


def group_and_transform_messages_by_category_upper(messages: List[Dict[str, str]]) -> str:

    """

    Group messages by category and transform them into markdown format with ### Category.
    Messages without a category are placed under "### Others".
    Categories are transformed to uppercase for comparison.

    Parameters:
        - messages (List[Dict[str, str]]): A list of dictionaries, each containing a message with its details.
    Returns:
        str: A string containing the grouped and transformed messages in markdown format.
    """

    grouped_messages = {}
    link_pattern = r'(https?://[^\s]+)'
    category_pattern = r'\*(\w+)\*'

    for message in messages:
        categories = [c.upper() for c in re.findall(category_pattern, message['message'])]
        links = re.findall(link_pattern, message['message'])

        if links:
            for link in links:
                transformed_message = re.sub(link, '', message['message']).strip()
                transformed_message = f"[{transformed_message}]({link})"

                if not categories:
                    categories = ['OTHERS']

                for category in categories:
                    if category not in grouped_messages:
                        grouped_messages[category] = []
                    grouped_messages[category].append(transformed_message)

    # Convert to markdown format
    markdown_output = ""
    print(categories)
    for category, messages in grouped_messages.items():
        markdown_output += f"### {category.capitalize()}\n"
        for message in messages:
            markdown_output += f"- {message}\n"
        markdown_output += "\n"
    return markdown_output



def group_and_transform_messages_by_category(messages: List[Dict[str, str]]) -> str:

    """
    Group messages by category and transform them into markdown format with ### Category.
    Parameters:

        - messages (List[Dict[str, str]]): A list of dictionaries, each containing a message with its details.
    Returns:
        str: A string containing the grouped and transformed messages in markdown format.

    """

    grouped_messages = {}
    link_pattern = r'(https?://[^\s]+)'
    category_pattern = r'\*(\w+)\*'

    for message in messages:
        categories = re.findall(category_pattern, message['message'])
        links = re.findall(link_pattern, message['message'])
        if links:
            for link in links:
                transformed_message = re.sub(link, '', message['message']).strip()
                transformed_message = f"[{transformed_message}]({link})"
                for category in categories:
                    if category not in grouped_messages:
                        grouped_messages[category] = []
                    grouped_messages[category].append(transformed_message)

    # Convert to markdown format
    markdown_output = ""
    for category, messages in grouped_messages.items():
        markdown_output += f"### {category}\n"
        for message in messages:
            markdown_output += f"- {message}\n"
        markdown_output += "\n"
    return markdown_output

if __name__ == "__main__":
    choice = input("Choose the type of file (Enter 'whatsapp' for WhatsApp chat file or 'links' for links file): ").strip().lower()

    if choice == "whatsapp":
        file_path = input("Enter the path to the WhatsApp chat file: ")
        with open(file_path, 'r', encoding='utf-8') as f:
            file_content = f.read()
        # Split the messages
        split_messages = split_messages_manually(file_content)
        grouped_and_transformed_messages = group_and_transform_messages_by_category_upper(split_messages)
        print(grouped_and_transformed_messages)
    elif choice == "links":
        file_path = input("Enter the path to the links file: ")
        result_file = extract_info_from_links(file_path)
        print(f"Link information saved to: {result_file}")
    else:
        print("Invalid choice!")

