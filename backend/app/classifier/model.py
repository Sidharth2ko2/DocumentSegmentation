from transformers import AutoModelForSequenceClassification

MODEL_NAME = "distilbert-base-uncased"

def load_model(num_labels):
    return AutoModelForSequenceClassification.from_pretrained(
MODEL_NAME, num_labels=num_labels
)