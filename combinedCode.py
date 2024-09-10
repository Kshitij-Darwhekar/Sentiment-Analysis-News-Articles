import os
from dotenv import load_dotenv
from newsapi import NewsApiClient
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from tqdm import tqdm  # Import tqdm for the progress bar

# Load environment variables from .env file
load_dotenv()  
api_key_n = os.getenv('API_KEY')

# Init NewsApiClient
newsapi = NewsApiClient(api_key=api_key_n)

# Initialize the sentiment analysis pipeline
tokenizer = AutoTokenizer.from_pretrained("mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis")
model = AutoModelForSequenceClassification.from_pretrained("mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis")
nlp = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

# Fetch news data
top_headlines = newsapi.get_top_headlines(q='stock market', category='business', language='en', country='us')
all_articles = newsapi.get_everything(q='stock market', sources='bbc-news,the-verge', domains='bbc.co.uk,techcrunch.com', from_param='2024-08-10', to='2024-09-10', language='en', sort_by='relevancy', page=2)

# Extract descriptions for sentiment analysis
def extract_descriptions(articles):
    return [article['description'] for article in articles if article['description']]

top_headlines_descriptions = extract_descriptions(top_headlines['articles'])
all_articles_descriptions = extract_descriptions(all_articles['articles'])

# Use tqdm to add a progress bar for sentiment analysis
def analyze_sentiment(descriptions):
    results = []
    for description in tqdm(descriptions, desc="Processing Descriptions"):
        result = nlp(description)
        results.append(result[0])
    return results

# Analyze sentiment
top_headlines_sentiment = analyze_sentiment(top_headlines_descriptions)
all_articles_sentiment = analyze_sentiment(all_articles_descriptions)

# Function to write data to a file
def write_to_file(filename, content):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)

# Prepare content for top headlines with sentiment
top_headlines_content = "Top Headlines with Sentiment:\n"
if top_headlines['status'] == 'ok':
    for article, sentiment in zip(top_headlines['articles'], top_headlines_sentiment):
        top_headlines_content += f"Title: {article['title']}\n"
        top_headlines_content += f"Description: {article['description']}\n"
        top_headlines_content += f"Sentiment: {sentiment['label']}, Score: {sentiment['score'] * 100:.2f}%\n"
        top_headlines_content += f"URL: {article['url']}\n"
        top_headlines_content += "-" * 80 + "\n"
else:
    top_headlines_content = "Failed to fetch top headlines\n"

# Prepare content for all articles with sentiment
all_articles_content = "All Articles with Sentiment:\n"
if all_articles['status'] == 'ok':
    for article, sentiment in zip(all_articles['articles'], all_articles_sentiment):
        all_articles_content += f"Title: {article['title']}\n"
        all_articles_content += f"Description: {article['description']}\n"
        all_articles_content += f"Sentiment: {sentiment['label']}, Score: {sentiment['score'] * 100:.2f}%\n"
        all_articles_content += f"URL: {article['url']}\n"
        all_articles_content += "-" * 80 + "\n"
else:
    all_articles_content = "Failed to fetch all articles\n"

# Write content to files
write_to_file('top_headlines.txt', top_headlines_content)
write_to_file('all_articles.txt', all_articles_content)

print("Data with sentiment analysis has been exported to 'top_headlines.txt', 'all_articles.txt'.")
