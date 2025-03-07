import itertools
import re

def is_valid_gmail(email):
    pattern = r'^[a-zA-Z0-9.]+@[gG][mM][aA][iI][lL]\.[cC][oO][mM]$'
    return re.match(pattern, email)

def generate_gmail_variants(email):
    if not is_valid_gmail(email):
        print("❌ Invalid Gmail address. Please enter a valid Gmail ID.")
        return []
    
    local, domain = email.split("@")
    
    # Remove dots since Gmail ignores them
    base_email = local.replace(".", "")
    
    # Generate exactly 5 dot variations
    dotted_variants = set()
    count = 0
    for i in range(1, len(base_email)):
        for combination in itertools.combinations(range(1, len(base_email)), i):
            if count >= 5:
                break
            modified = list(base_email)
            for pos in combination:
                modified.insert(pos, '.')
            dotted_variants.add("".join(modified) + "@" + domain)
            count += 1
    
    # Adding exactly 5 + tags (Hackers may exploit this for filtering bypass)
    plus_variants = set()
    common_aliases = ["info", "contact", "support", "service", "admin"]
    for alias in common_aliases:
        plus_variants.add(base_email + "+" + alias + "@" + domain)
        if len(plus_variants) >= 5:
            break
    
    # Combine exactly 5 dot and 5 plus variants
    all_variants = list(dotted_variants) + list(plus_variants)
    
    return all_variants

if __name__ == "__main__":
    email = input("Enter your Gmail address: ")
    variants = generate_gmail_variants(email)
    
    if variants:
        print("\n🔍 Possible Variants:")
        for variant in variants:
            print(variant)
