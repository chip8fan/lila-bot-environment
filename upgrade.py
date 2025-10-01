import os
token_file = open("tokens.txt")
tokens = [token.strip().split(" ")[0] for token in token_file]
token_file.close()
for token in tokens:
    os.system(f"curl -d '' http://localhost:8080/api/bot/account/upgrade -H \"Authorization: Bearer {token}\"")