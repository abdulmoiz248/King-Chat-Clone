import re
import json

def parsePersonalChat(filePath, yourName, muqeetName):
    with open(filePath, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    messageRegex = re.compile(r'^(\d{2}/\d{2}/\d{4}), (\d{2}:\d{2}) - ([^:]+): (.+)$')
    cleanedMessages = []

    for line in lines:
        if "Messages and calls are end-to-end encrypted." in line:
            continue
        match = messageRegex.match(line.strip())
        if match:
            date, time, sender, message = match.groups()
            if message.strip() != "<Media omitted>":
                cleanedMessages.append({
                    "sender": sender.strip(),
                    "message": message.strip()
                })

    dataPairs = []
    i = 0
    while i < len(cleanedMessages):
        if cleanedMessages[i]['sender'] == yourName:
            userMsgs = [cleanedMessages[i]['message']]
            i += 1
            while i < len(cleanedMessages) and cleanedMessages[i]['sender'] == yourName:
                userMsgs.append(cleanedMessages[i]['message'])
                i += 1
            if i < len(cleanedMessages) and cleanedMessages[i]['sender'] == muqeetName:
                dataPairs.append({
                    "input": '\n'.join(userMsgs),
                    "response": cleanedMessages[i]['message']
                })
        else:
            i += 1

    return dataPairs

def saveToJson(pairs, outPath='muqeet_personal_cleaned.json'):
    with open(outPath, 'w', encoding='utf-8') as f:
        json.dump(pairs, f, indent=2, ensure_ascii=False)

# === USAGE ===
yourName = "Abdul Moiz 🦅"
muqeetName = "King Muqeet"
filePath = "chats/personalChat.txt"

pairs = parsePersonalChat(filePath, yourName, muqeetName)
saveToJson(pairs)
print(f"✅ Extracted {len(pairs)} input-response pairs.")
