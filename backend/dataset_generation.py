import os
import subprocess
import time

BASE_DIR = "data"
SAMPLES_PER_CATEGORY = 50
MODEL = "llama3.1:8b"

categories = {
    #"Emails": "Write a realistic internal professional email between colleagues.",
    "Meeting_Notes": "Write realistic internal meeting notes with agenda, discussion points, and action items.",
    "Tutorials_Guides": "Write a step-by-step internal technical tutorial or guide.",
    "Technical_Documentation": "Write realistic internal technical documentation for a software system.",
    "Reports": "Write a realistic internal project or status report.",
    "Policies_Rules": "Write a realistic internal company policy or guideline document.",
    "Other": "Write realistic unstructured internal notes or miscellaneous text."
}

def generate_text(prompt):
    full_prompt = f"""
{prompt}
The document should:
- Be 2–5 paragraphs
- Sound like internal company content
- Not mention AI or ChatGPT
- Be written in plain professional English
"""

    result = subprocess.run(
        ["ollama", "run", MODEL],
        input=full_prompt,
        text=True,
        capture_output=True
    )
    return result.stdout.strip()

os.makedirs(BASE_DIR, exist_ok=True)

for category, prompt in categories.items():
    cat_path = os.path.join(BASE_DIR, category)
    os.makedirs(cat_path, exist_ok=True)

    print(f"Generating samples for {category}...")

    for i in range(1, SAMPLES_PER_CATEGORY + 1):
        text = generate_text(prompt)
        file_path = os.path.join(cat_path, f"{category.lower()}_{i}.txt")

        with open(file_path, "w") as f:
            f.write(text)

        print(f"{category} sample {i}")
        time.sleep(0.5)  # prevents overheating

print("Ollama-powered dataset generation completed.")
