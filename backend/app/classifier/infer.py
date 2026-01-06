import os, torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

model = None
tokenizer = None
labels = []

try:
    model = AutoModelForSequenceClassification.from_pretrained('models/docclf')
    tokenizer = AutoTokenizer.from_pretrained('distilbert-base-uncased')
    labels = sorted([f for f in os.listdir('data') if not f.startswith('.')])
except:
    pass

def classify(text: str):
    if not model:
        return 'Other', 0.0
    inputs = tokenizer(text, return_tensors='pt', truncation=True)
    logits = model(**inputs).logits
    probs = torch.softmax(logits, dim=1)
    idx = torch.argmax(probs).item()
    return labels[idx], float(probs[0][idx])