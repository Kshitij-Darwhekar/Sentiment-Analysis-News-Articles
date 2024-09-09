from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import pipeline
from tqdm import tqdm  # Import tqdm for the progress bar

# Load the model and tokenizer
model = AutoModelForSequenceClassification.from_pretrained("yiyanghkust/finbert-tone")
tokenizer = AutoTokenizer.from_pretrained("yiyanghkust/finbert-tone")

# Initialize the sentiment analysis pipeline
nlp = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

# List of sentences for sentiment analysis
sentences = [
    "Nifty 50 Snaps 3-day losing run:why did the Indian Stock market rise today?",  
    "US stocks edge higher after last week's rout", 
    "Expert View: This roaring bull market has hues of irrational exurberance",
    "GMR Airports to increase stake in Delhi airport by 10%",
    "Call Waiting : How Vodafone Idea can claw its way back.",
    "Why ikea's parent is betting big on malls when quick commerce rules the day."
]

# Use tqdm to add a progress bar
results = []
for sentence in tqdm(sentences, desc="Processing Sentences"):
    result = nlp(sentence)
    results.append(result[0])

# Print the formatted results
for sentence, result in zip(sentences, results):
    label = result['label']
    score = result['score'] * 100  # Convert score to percentage
    print(f"Sentence: \"{sentence}\"")
    print(f"Label: {label}, Score: {score:.2f}%\n")
