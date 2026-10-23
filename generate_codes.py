import json
import secrets
import string

def generate_codes(num_codes=10, length=100):
    codes = []
    for _ in range(num_codes):
        # Generate a secure random 100-character alphanumeric string
        code = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(length))
        codes.append(code)
    
    with open("auth.json", "w") as f:
        json.dump({"valid_codes": codes, "active_users": {}}, f, indent=4)
        
    print(f"✅ Generated {num_codes} codes and saved to auth.json")
    print(f"Example Code: {codes[0]}")

if __name__ == "__main__":
    generate_codes()
