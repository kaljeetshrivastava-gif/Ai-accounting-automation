import pytesseract
from PIL import Image
import re
import spacy
from collections import defaultdict
import os #

import os
import subprocess
import sys

# English model ko force download karne ke liye
try:
    import en_core_web_sm
    nlp = en_core_web_sm.load()
except ImportError:
    subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
    import en_core_web_sm
    nlp = en_core_web_sm.load()


# Categories for balance sheet
ASSET_KEYWORDS = ['cash', 'bank', 'inventory', 'property', 'asset', 'receivable']
LIABILITY_KEYWORDS = ['payable', 'loan', 'mortgage', 'liability', 'debt']
EQUITY_KEYWORDS = ['capital', 'equity', 'earnings']

def ocr_image_to_text(image_path):
    # Image se text nikalne ke liye
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text

def extract_entries(text):
    # Amounts aur descriptions nikalne ke liye regex
    pattern = re.compile(r'([A-Za-z\s]+)\s+([\d,]+\.\d{2}|\d+)')
    entries = pattern.findall(text)
    cleaned_entries = [(desc.strip().lower(), float(amount.replace(',', ''))) for desc, amount in entries]
    return cleaned_entries

def categorize_entry(description):
    desc = description.lower()
    if any(keyword in desc for keyword in ASSET_KEYWORDS):
        return 'Assets'
    elif any(keyword in desc for keyword in LIABILITY_KEYWORDS):
        return 'Liabilities'
    elif any(keyword in desc for keyword in EQUITY_KEYWORDS):
        return 'Equity'
    else:
        return 'Uncategorized'

def generate_balance_sheet(entries):
    balance_sheet = defaultdict(float)
    for desc, amount in entries:
        category = categorize_entry(desc)
        balance_sheet[category] += amount
    return balance_sheet

if __name__ == "__main__":
    print("AI Accounting Tool - Developed by Kaljeet")
    # Ye sample logic hai, real image path yahan aayega
    sample_text = "Cash 5000\nLoan 2000\nCapital 3000"
    entries = extract_entries(sample_text)
    bs = generate_balance_sheet(entries)
    
    print("\n--- Balance Sheet Summary ---")
    for cat, amt in bs.items():
        print(f"{cat}: ${amt:,.2f}")
      
