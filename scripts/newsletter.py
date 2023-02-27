from zulip import Client
from decouple import config
import time

# Stream name
STREAM = "lobembe"

# Create Zulip client instance
client = Client(email="reminder-bot@mongulu.zulipchat.com", api_key=config('API_KEY'),site="https://mongulu.zulipchat.com")

request: dict = {
    "anchor": "newest",
    "num_before": 100,
    "num_after": 0,
    "narrow": [
        {"operator": "stream", "operand": STREAM},
        {"operator": "topic", "operand": "github", "negated": True},
        {"operator": "topic", "operand": "watchtower", "negated": True},
        {"operator": "topic", "operand": "stream events", "negated": True}
    ],
}

# Get all messages from all topics in the stream
result = client.get_messages(request)

# Extract messages from the result
messages = result["messages"]

# Dict to store messages grouped by topic
topics = {}

for message in messages:
    #print("Subject:", message["subject"], "Content:", message["content"])

    topic = message["subject"]
    content = message["content"]

    import html
    from html.parser import HTMLParser
    
    class MyHTMLParser(HTMLParser):
        def __init__(self):
            self.reset()
            self.strict = False
            self.convert_charrefs= True
            self.data = []

        def handle_data(self, data):
            self.data.append(data)
            

    parser = MyHTMLParser()
    parser.feed(html.unescape(content))
    text = parser.data[0]
    url = parser.data[0] if len(parser.data) == 1 else parser.data[1]

    if topic not in topics:
        topics[topic] = []
    topics[topic].append((text, url))

    #markdown_link = "[{}]({})".format(text,url)
    #print(markdown_link)

# Format the messages
output = ""
for topic, messages in topics.items():
    output += f"### {topic}\n"
    for text, url in messages:
        output += f"- [{text}]({url})\n"
    output +="\n"

print(output)
# Delete all messages
response = input("Do you want to delete all messages in topics (Make sure output is oki before) ? [y/n]: ")
if response.lower() == "y" or response.lower() == "yes":
    for message in result["messages"]:
        print(message)
        result = client.delete_message(message["id"])
        time.sleep(1)
    print("{} messages deleted".format(len(result["messages"]))
else:
    print("No messages deleted")




