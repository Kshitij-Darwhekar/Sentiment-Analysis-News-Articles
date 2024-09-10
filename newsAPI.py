from dotenv import load_dotenv
import os
from newsapi import NewsApiClient

load_dotenv()  # Load environment variables from .env file
api_key_n = os.getenv('API_KEY')

# Init
newsapi = NewsApiClient(api_key=api_key_n)

# /v2/top-headlines
top_headlines = newsapi.get_top_headlines(q='stock market',
                                          category='business',
                                          language='en',
                                          country='us')

# /v2/everything
all_articles = newsapi.get_everything(q='stock market',
                                      sources='bbc-news,the-verge',
                                      domains='bbc.co.uk,techcrunch.com',
                                      from_param='2024-08-10',
                                      to='2024-09-10',
                                      language='en',
                                      sort_by='relevancy',
                                      page=2)

# /v2/top-headlines/sources
# sources = newsapi.get_sources()

# Function to write data to a file
def write_to_file(filename, content):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)

# Prepare content for top headlines
top_headlines_content = "Top Headlines:\n"
if top_headlines['status'] == 'ok':
    for article in top_headlines['articles']:
        top_headlines_content += f"Title: {article['title']}\n"
        top_headlines_content += f"Description: {article['description']}\n"
        top_headlines_content += f"URL: {article['url']}\n"
        top_headlines_content += "-" * 80 + "\n"
else:
    top_headlines_content = "Failed to fetch top headlines\n"

# Prepare content for all articles
all_articles_content = "All Articles:\n"
if all_articles['status'] == 'ok':
    for article in all_articles['articles']:
        all_articles_content += f"Title: {article['title']}\n"
        all_articles_content += f"Description: {article['description']}\n"
        all_articles_content += f"URL: {article['url']}\n"
        all_articles_content += "-" * 80 + "\n"
else:
    all_articles_content = "Failed to fetch all articles\n"

# Prepare content for sources
# sources_content = "Sources:\n"
# if sources['status'] == 'ok':
#     for source in sources['sources']:
#         sources_content += f"Source Name: {source['name']}\n"
#         sources_content += f"Description: {source['description']}\n"
#         sources_content += f"URL: {source['url']}\n"
#         sources_content += "-" * 80 + "\n"
# else:
#     sources_content = "Failed to fetch sources\n"

# Write content to files
write_to_file('top_headlines.txt', top_headlines_content)
write_to_file('all_articles.txt', all_articles_content)
# write_to_file('sources.txt', sources_content)

print("Data has been exported to 'top_headlines.txt', 'all_articles.txt'.")