import re
import json

def parseGroupChat(filePath, muqeetName):
    with open(filePath, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # WhatsApp message format in group chat
    messagePattern = re.compile(r'^(\d{2}/\d{2}/\d{4}), \d{2}:\d{2} - ([^:]+): (.+)$')
    
    messages = []
    for line in lines:
        match = messagePattern.match(line.strip())
        if match:
            date, sender, message = match.groups()
            if "<Media omitted>" in message or "This message was deleted" in message:
                continue
            messages.append({"sender": sender.strip(), "message": message.strip()})

    pairs = []
    contextMessages = []  # Initialize context for all non-Muqeet messages
    response = []  # Collect Muqeet's responses

    for i in range(len(messages)):
        if messages[i]['sender'] == muqeetName:
            # Add context until Muqeet's message comes
            if contextMessages:
                context = "\n".join(contextMessages)
                pairs.append({"context": context, "response": "\n".join(response)})
                contextMessages = []  # Reset context after adding it to pairs
                response = []  # Reset response after adding it to pairs

            # Collect Muqeet's messages for response
            response.append(messages[i]['message'])

            # Add multiple responses from Muqeet until someone else speaks
            j = i + 1
            while j < len(messages) and messages[j]['sender'] == muqeetName:
                if "null" in messages[j]['message'] or not messages[j]['message'].strip():
                    j += 1
                    continue
                response.append(messages[j]['message'])
                j += 1
            
        else:
            # Collect messages from others in the context window until Muqeet replies
            if response:
                contextMessages.append(f"{messages[i]['sender']}: {messages[i]['message']}")

    # If there are leftover responses after the last message
    if response:
        context = "\n".join(contextMessages)
        pairs.append({"context": context, "response": "\n".join(response)})

    # Write the parsed pairs to a JSON file
    with open('muqeet_responses.json', 'w', encoding='utf-8') as json_file:
        json.dump(pairs, json_file, ensure_ascii=False, indent=4)

    return pairs

filePath = "chats/groupChat_2.txt"
muqeetName = "King Muqeet"

muqeetPairs = parseGroupChat(filePath, muqeetName)

# Optionally, return the first few pairs as a sanity check
outputSample = muqeetPairs[:5]  # show first 5 results
len(muqeetPairs), outputSample
