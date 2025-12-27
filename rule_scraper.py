import requests
from bs4 import BeautifulSoup
from storage import categories

url = "https://www.cnn.com/"

def classify_headline(headline, categories):
    headline = headline.lower()
    scores = {}

    for category, keywords in categories.items():
        score = 0
        for word in keywords:
            if word in headline:
                score += 1
        scores[category] = score

        # find category with highest score
    best_category = max(scores, key=scores.get)

    # if no keywords matched
    if scores[best_category] == 0:
        return "Other"

    return best_category

politics = 0
world = 0
business = 0
tech = 0
health = 0
climate = 0
law = 0
entertainment = 0
sports = 0
other = 0

# 1️⃣ Fetch the page
response = requests.get(url)
html = response.text
soup = BeautifulSoup(html, "html.parser")

headlines = soup.find_all(
    "span",
    class_="container__headline-text"
)

for h in headlines:
    category = classify_headline(h.get_text(), categories)

    if category == "World":
        world += 1
    elif category == "Business":
        business += 1
    elif category == "Technology":
        tech += 1
    elif category == "Sports":
        sports += 1
    elif category == "Politics":
        politics += 1
    elif category == "Health":
        health += 1
    elif category == "Climate":
        climate += 1
    elif category == "Law":
        law += 1
    elif category == "Entertainment":
        entertainment += 1
    else:
        other += 1

print("There are " + str(politics) + " politics headlines")
print("There are " + str(business) + " business headlines")
print("There are " + str(tech) + " tech headlines")
print("There are " + str(sports) + " sports headlines")
print("There are " + str(world) + " world headlines")
print("There are " + str(health) + " health headlines")
print("There are " + str(climate) + " climate headlines")
print("There are " + str(law) + " law headlines")
print("There are " + str(entertainment) + " entertainment headlines")
print("There are " + str(other) + " other headlines")

