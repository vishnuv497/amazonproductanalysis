import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
from textblob import TextBlob

def get_amazon_product_data(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return None
    
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.find("span", attrs={"id": "productTitle"})
    rating = soup.find("span", attrs={"class": "a-icon-alt"})
    price = soup.find("span", attrs={"class": "a-price-whole"})
    reviews = soup.find_all("span", attrs={"class": "review-text-content"})
    
    title_text = title.get_text(strip=True) if title else "N/A"
    rating_text = rating.get_text(strip=True) if rating else "N/A"
    price_text = price.get_text(strip=True) if price else "N/A"
    
    review_texts = [review.get_text(strip=True) for review in reviews]
    
    return {
        "title": title_text,
        "rating": rating_text,
        "price": price_text,
        "reviews": review_texts
    }

def analyze_sentiment(reviews):
    sentiments = []
    for review in reviews:
        sentiment = TextBlob(review).sentiment.polarity
        sentiments.append(sentiment)
    return sentiments

def plot_sentiment_distribution(sentiments):
    plt.figure(figsize=(6, 4))
    plt.hist(sentiments, bins=20, edgecolor='black', alpha=0.7)
    plt.xlabel("Sentiment Polarity")
    plt.ylabel("Frequency")
    plt.title("Sentiment Analysis of Reviews")
    st.pyplot(plt)

def main():
    st.title("Amazon Product Analysis")
    product_url = st.text_input("Enter Amazon Product URL:")
    
    if st.button("Analyze"):
        with st.spinner("Fetching product data..."):
            product_data = get_amazon_product_data(product_url)
            
            if not product_data:
                st.error("Failed to retrieve product details. Check the URL and try again.")
                return
            
            st.subheader("Product Details")
            st.write(f"**Title:** {product_data['title']}")
            st.write(f"**Rating:** {product_data['rating']}")
            st.write(f"**Price:** {product_data['price']}")
            
            st.subheader("Sentiment Analysis of Reviews")
            sentiments = analyze_sentiment(product_data['reviews'])
            plot_sentiment_distribution(sentiments)
            
            sentiment_df = pd.DataFrame({"Review": product_data['reviews'], "Sentiment": sentiments})
            st.dataframe(sentiment_df)
            
if __name__ == "__main__":
    main()
