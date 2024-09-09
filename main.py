from transformers import BertTokenizer, BertForSequenceClassification
from transformers import pipeline
from tqdm import tqdm  # Import tqdm for the progress bar

# Load the model and tokenizer
model = BertForSequenceClassification.from_pretrained("ahmedrachid/FinancialBERT-Sentiment-Analysis", num_labels=3)
tokenizer = BertTokenizer.from_pretrained("ahmedrachid/FinancialBERT-Sentiment-Analysis")

# Initialize the sentiment analysis pipeline
nlp = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

# List of sentences for sentiment analysis
sentences = [
    "Operating profit rose to EUR 13.1 mn from EUR 8.7 mn in the corresponding period in 2007 representing 7.7 % of net sales.",  
    "Bids or offers include at least 1,000 shares and the value of the shares must correspond to at least EUR 4,000.", 
    "Raute reported a loss per share of EUR 0.86 for the first half of 2009 , against EPS of EUR 0.74 in the corresponding period of 2008.",
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
