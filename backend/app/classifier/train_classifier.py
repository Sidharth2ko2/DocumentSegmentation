import os
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
from torch.optim import AdamW
from transformers import AutoTokenizer
from .model import load_model
from tqdm import tqdm

class SimpleDocDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_len=512):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        encoding = self.tokenizer(
            str(self.texts[idx]),
            truncation=True,
            padding='max_length',
            max_length=self.max_len,
            return_tensors='pt'
        )
        return {
            'input_ids': encoding['input_ids'].squeeze(0),
            'attention_mask': encoding['attention_mask'].squeeze(0),
            'labels': torch.tensor(self.labels[idx], dtype=torch.long)
        }

# Setup Data
DATA_DIR = "data"
texts, labels, label_names = [], [], []

# Sorted folders for consistent label IDs
folders = sorted([f for f in os.listdir(DATA_DIR) if not f.startswith('.')])

for i, folder in enumerate(folders):
    label_names.append(folder)
    folder_path = os.path.join(DATA_DIR, folder)
    
    files = [f for f in os.listdir(folder_path) if not f.startswith('.')]
    for f in files:
        with open(os.path.join(folder_path, f), "r", encoding="utf-8") as file:
            texts.append(file.read())
            labels.append(i)

print(f"Loaded {len(texts)} documents across {len(label_names)} categories.")

# Device & Model
device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
model = load_model(len(label_names)).to(device)

dataset = SimpleDocDataset(texts, labels, tokenizer)
loader = DataLoader(dataset, batch_size=16, shuffle=True) # 16 is fine for 330 docs

# Optimizer
optimizer = AdamW(model.parameters(), lr=5e-5) # Slightly higher LR for small datasets

# Training Loop
model.train()
for epoch in range(5): # 5 epochs is better for small data
    loop = tqdm(loader, desc=f"Epoch {epoch+1}")
    for batch in loop:
        optimizer.zero_grad()
        
        input_ids = batch['input_ids'].to(device)
        mask = batch['attention_mask'].to(device)
        targets = batch['labels'].to(device)

        outputs = model(input_ids, attention_mask=mask, labels=targets)
        loss = outputs.loss
        loss.backward()
        optimizer.step()

        loop.set_postfix(loss=loss.item())

# Save for infer.py
save_path = "models/docclf"
os.makedirs(save_path, exist_ok=True)
model.save_pretrained(save_path)
tokenizer.save_pretrained(save_path)
print(f"Success! Model saved to {save_path}")