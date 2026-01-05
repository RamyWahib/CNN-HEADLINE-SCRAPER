import requests
import re
from bs4 import BeautifulSoup
from collections import Counter

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from scipy.io import savemat

data = {}
# Scraping the headlines from the CNN
URL = "https://www.cnn.com/"
HEADERS = {"User-Agent": "Mozilla/5.0"} # just in case CNN blocks bots

response = requests.get(URL, headers=HEADERS)
soup = BeautifulSoup(response.text, "html.parser")

headline_tags = soup.find_all("span", class_="container__headline-text")
headlines = [h.get_text(strip=True) for h in headline_tags]

print(f"Scraped {len(headlines)} headlines\n")

# Implementing specific keywords to be able to identify categories
categories = {
    "Politics": [
        "election", "biden", "trump", "congress", "senate",
        "white house", "supreme court", "government", "policy"
    ],
    "World": [
        "war", "ukraine", "russia", "gaza", "israel", "china",
        "palestine", "iran", "nato", "foreign"
    ],
    "Business": [
        "stocks", "market", "economy", "inflation",
        "jobs", "bank", "earnings", "crypto"
    ],
    "Technology": [
        "ai", "artificial intelligence", "google", "apple",
        "microsoft", "amazon", "tesla", "cyber"
    ],
    "Sports": [
        "nba", "nfl", "soccer", "olympics",
        "mlb", "nhl", "match", "tournament"
    ],
    "Health": [
        "outbreak", "medicine", "outbreak"
        ,"cases", "disease", "virus"
    ],
    "Entertainment": [
        "stranger things", "netflix", "youtube",
        "star", "actor", "finale", "musician"
    ],

}

# A function made
def rule_based_classify(headline, categories):
    text = headline.lower()
    scores = {}

    for category, keywords in categories.items():
        scores[category] = sum(1 for kw in keywords if kw in text)

    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "Other"

# Create labeled dataset
labeled_headlines = []
labels = []

for h in headlines:
    label = rule_based_classify(h, categories)
    if label != "Other":   # Remove weak/noisy samples
        labeled_headlines.append(h)
        labels.append(label)

print("Labeled " + str(len(labeled_headlines)) + " headlines for training\n")

# Using TF-IDF and creating a vector for it
vectorizer = TfidfVectorizer(
    stop_words="english",
    ngram_range=(1, 2),   # unigrams + bigrams
    min_df=2
)

X = vectorizer.fit_transform(labeled_headlines)
y = labels

# Train test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)

# Using Logisitc Regression to train it
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Evaluating the model
preds = model.predict(X_test)
accuracy = accuracy_score(y_test, preds)

print(f"Model accuracy: {accuracy:.2f}\n")
data["accuracy"] = accuracy * 100

# Classifying all the headlines
X_all = vectorizer.transform(headlines)
predicted_categories = model.predict(X_all)

# Analyzing the trends
trend_counts = Counter(predicted_categories)

print("Trending categories right now:\n")
for category, count in trend_counts.most_common():
    print(f"{category}: {count}")
    data[category] = count

data["headlines"] = []
print("\nSample classified headlines:\n")
for h, c in list(zip(headlines, predicted_categories))[:10]:
    print(f"[{c}] {h}")
    data["headlines"].append('"' + h + '"')

savemat("data.mat", data)