import re
import dns.resolver
from email import policy
from email.parser import BytesParser
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)

# AI-Based Email Classifier (Trained on Dummy Data)
def train_email_classifier():
    training_data = [
        "SPF_PASS DKIM_PASS DMARC_PASS",  # Legit
        "SPF_FAIL DKIM_PASS DMARC_FAIL",  # Suspicious
        "SPF_PASS DKIM_FAIL DMARC_PASS",  # Suspicious
        "SPF_FAIL DKIM_FAIL DMARC_FAIL",  # Highly suspicious
    ]
    
    labels = ["Legit", "Suspicious", "Suspicious", "Highly Suspicious"]
    
    vectorizer = CountVectorizer()
    X_train = vectorizer.fit_transform(training_data)
    
    model = MultinomialNB()
    model.fit(X_train, labels)
    
    return model, vectorizer

# DNS Record Checking Functions
def get_txt_records(domain):
    try:
        txt_records = dns.resolver.resolve(domain, 'TXT')
        return [record.to_text().strip('"') for record in txt_records]
    except dns.resolver.NoAnswer:
        return []
    except dns.resolver.NXDOMAIN:
        return ["Domain does not exist"]
    except Exception as e:
        return [f"Error: {e}"]

def check_spf(domain):
    records = get_txt_records(domain)
    spf_records = [rec for rec in records if rec.startswith("v=spf1")]
    return "SPF_PASS" if spf_records else "SPF_FAIL"

def check_dmarc(domain):
    records = get_txt_records("_dmarc." + domain)
    dmarc_records = [rec for rec in records if rec.startswith("v=DMARC1")]
    return "DMARC_PASS" if dmarc_records else "DMARC_FAIL"

def check_dkim(domain, selector="default"):
    records = get_txt_records(f"{selector}._domainkey.{domain}")
    dkim_records = [rec for rec in records if "DKIM" in rec or "v=DKIM1" in rec]
    return "DKIM_PASS" if dkim_records else "DKIM_FAIL"

# AI-Based Email Security Analyzer
def analyze_email_security(email_address):
    if not is_valid_email(email_address):
        print("❌ Invalid email format. Please enter a valid email address.")
        return
    
    domain = email_address.split("@")[1]
    
    spf_result = check_spf(domain)
    dkim_result = check_dkim(domain)
    dmarc_result = check_dmarc(domain)

    security_features = f"{spf_result} {dkim_result} {dmarc_result}"

    # Train AI Model
    model, vectorizer = train_email_classifier()
    
    # Predict Email Security
    X_test = vectorizer.transform([security_features])
    prediction = model.predict(X_test)[0]
    
    print(f"\n🔍 Email Security Analysis for: {email_address}\n")
    print(f"✅ SPF Check: {spf_result}")
    print(f"✅ DKIM Check: {dkim_result}")
    print(f"✅ DMARC Check: {dmarc_result}")
    print(f"\n🔴 AI Prediction: **{prediction}**")

if __name__ == "__main__":
    email = input("Enter an email address to analyze: ")
    analyze_email_security(email)
