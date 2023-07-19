import re

# Mapping of strings to characters
replacements = {
    "\u00c3\u00a0": "à",
    "\u00c3\u00a1": "á",
    "\u00c3\u00a2": "â",
    "\u00c3\u00a3": "ã",
    "\u00c3\u00a4": "ä",
    "\u00c3\u00a5": "å",
    "\u00c3\u00a6": "æ",
    "\u00c3\u00a7": "ç",
    "\u00c3\u00a8": "è",
    "\u00c3\u00a9": "é",
    "\u00c3\u00aa": "ê",
    "\u00c3\u00ab": "ë",
    "\u00c3\u00ad": "í",
    "\u00c3\u00ae": "î",
    "\u00c3\u00af": "ï",
    "\u00c3\u00b1": "ñ",
    "\u00c3\u00b3": "ó",
    "\u00c3\u00b4": "ô",
    "\u00c3\u00b5": "õ",
    "\u00c3\u00b6": "ö",
    "\u00c3\u00ba": "ú",
    "\u00c3\u00bb": "û",
    "\u00c3\u00bc": "ü",
    "\u00c3\u0080": "À",
    "\u00c3\u0081": "Á",
    "\u00c3\u0082": "Â",
    "\u00c3\u0083": "Ã",
    "\u00c3\u0084": "Ä",
    "\u00c3\u0085": "Å",
    "\u00c3\u0086": "Æ",
    "\u00c3\u00c7": "Ç",
    "\u00c3\u0088": "È",
    "\u00c3\u0089": "É",
    "\u00c3\u008a": "Ê",
    "\u00c3\u008b": "Ë",
    "\u00c3\u008d": "Í",
    "\u00c3\u008e": "Î",
    "\u00c3\u008f": "Ï",
    "\u00c3\u0091": "Ñ",
    "\u00c3\u0093": "Ó",
    "\u00c3\u0094": "Ô",
    "\u00c3\u0095": "Õ",
    "\u00c3\u0096": "Ö",
    "\u00c3\u009a": "Ú",
    "\u00c3\u009b": "Û",
    "\u00c3\u009c": "Ü",
    "\\": "",
    "\u00c3": "",
}

# Input and output file path
file_path = "json.txt"

# Read the file with unicode_escape encoding
with open(file_path, "r", encoding="unicode_escape") as file:
    content = file.read()

# Replace strings with characters
for string, char in replacements.items():
    content = content.replace(string, char)
    print("Cleaning characters...")
    
# Replace the strings starting with "@[" and removing everything between "@[" and the last ":"
content = re.sub(r"@(\[[^\]]*:)([^:\]]*)\]", r"@[\2]", content)

# Write updated content back to the same file
with open(file_path, "w", encoding="utf-8") as file:
    file.write(content)

print("File updated successfully!")