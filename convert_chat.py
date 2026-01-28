import re

INPUT_FILE = "chat.txt"
OUTPUT_FILE = "clean_chat.txt"

user_name = "Robin"
bot_name = "Saumyaaa"

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    lines = f.readlines()

clean = []

pattern = re.compile(r"\] (.*?): (.*)")

for line in lines:
    match = pattern.search(line)
    if not match:
        continue

    name, message = match.groups()

    # Skip media / empty messages
    if "<attached:" in message or not message.strip():
        continue

    if name == user_name:
        clean.append(f"User: {message.strip()}")
    elif name == bot_name:
        clean.append(f"Bot: {message.strip()}")

# Ensure User -> Bot pairing
paired = []
for i in range(len(clean) - 1):
    if clean[i].startswith("User:") and clean[i+1].startswith("Bot:"):
        paired.append(clean[i])
        paired.append(clean[i+1])
        paired.append("")

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(paired))

print("✅ clean_chat.txt generated successfully")
