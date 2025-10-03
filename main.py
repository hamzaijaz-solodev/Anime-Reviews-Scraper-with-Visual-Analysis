from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import requests
import numpy as np
import sys


#Anime Search Engine
result_no = 0
result_list = []
ID_list = []
scores_List = []
counts_List = []

Anime_Name = str(input("\nAnime Search Engine:-\nEnter Anime Name: "))
search_url = f"https://myanimelist.net/anime.php?q={Anime_Name}"

#Searching Results on "https://myanimelist.net/anime.php?q="
search_html = requests.get(search_url).text
search_soup = BeautifulSoup(search_html, "lxml")
search_results = search_soup.find_all("a", class_ ="hoverinfo_trigger fw-b fl-l")

#Code Section to Print Anime search Titles and ID and their Links.
print("\nSearch Results:-")
print("(Type the Anime result \"number\" which you want the reviews from.)\n")

for result in search_results:

    #Getting Titles and Adding them in a List
    result_title = result.find("strong").text
    result_no += 1
    result_list.append(result_title)

    #Getting ID and Adding them in a List
    ID_text = result.get("id")
    Anime_ID = ID_text.replace("sinfo", "")
    ID_list.append(Anime_ID)

    #Printing Out Titles and ID.
    print(f"{result_no}. {result_title}")
    print(f"Anime ID: {Anime_ID}")
    print(f"Link: {result.get('href')}\n")


#Code to for asking User for a Result Number
selected_result_number = int(input("\nEnter Result Number: "))
selected_anime = selected_result_number - 1

#Taking out Selected Anime ID from the List
Anime_ID = ID_list[selected_anime]

#Showing the Anime you Selected
Anime_Name = str(result_list[selected_anime])
print(f"\nYou Selected: {Anime_Name}")
print(f"Anime ID: {Anime_ID}")
input("Press Enter to Continue...")

#URL variables below require (_) instead of whitespaces
Anime_Name = Anime_Name.replace(" ", "_")

#Link of Website
link = f"https://myanimelist.net/anime/{Anime_ID}/{Anime_Name}/reviews?sort=suggested&filter_check=&filter_hide=&preliminary=on&spoiler=on&p=1"

#starting variables
page = 1
section_no = 0

#code section to Display Total Reviews Number and Link of Website
website = requests.get(link).text
init = BeautifulSoup(website, "lxml")
total_review_sections_div = init.find("div", class_="filtered-results-box")

try:
    total_review_sections = int(total_review_sections_div.find("strong").text)

    if total_review_sections == 0:
        print("\n\nAnime can't be Rated. Total Reviews are Zero. Either Anime is recently aired or Anime is not very famous.")
        sys.exit()

except Exception:
    print("\n\nAnime Doesn't have any Reviews.")
    sys.exit()

print(f"\nTotal Reviews: {total_review_sections}")
print(f"Link: {link}\n")
input("Press Enter to See all the Reviews...")
print()

#Code Section for Scraping of all Individual Review
Scraping = True
while Scraping:
    #Scraping with Pagination (all pages)
    page_url = f"https://myanimelist.net/anime/{Anime_ID}/{Anime_Name}/reviews?sort=suggested&filter_check=&filter_hide=&preliminary=on&spoiler=on&p={page}"
    page += 1

    html_text = requests.get(page_url).text
    soup = BeautifulSoup(html_text, "lxml")

    #Getting Review Sections of each Individual.
    All_Sections = soup.find_all("div", class_ = "thumbbody mt8")

    #exits the program when all reviews are scraped
    for section in All_Sections:
        section_no += 1
        if section_no >= int(total_review_sections):
            Scraping = False

        #scraping all data related to a Review
        username = section.find("a", class_ = "ga-click", attrs={"data-ga-click-type" : "review-anime-reviewer"}).text

        review_div_tag = section.find("div", attrs={"data-id" : True})
        review_opinion = review_div_tag.find(string=True, recursive=False)

        # Score is out of 10
        review_score = section.find("span", class_="num").text
        scores_List.append(int(review_score))

        review_date = section.find("div", class_ = "update_at").text

        #Printing out all the Data on a Review
        print(f"Username: {username}")
        print(f"Opinion: {review_opinion}")
        print(f"Review Score: {review_score}/10")
        print(f"Review Date: {review_date}\n")


#Code Section for Analysis of Scores

#Custom weights to each Score
weight_table = {
    10: 3.0,
    9: 2.5,
    8: 1.5,
    7: 1.2,
    6: 1.0,
    5: 0.8,
    4: 0.5,
    3: 1.0,
    2: 1.5,
    1: 2.5,
    0: 3.0
}

# build weights for each review according to its score
counts_List = [scores_List.count(0), scores_List.count(1), scores_List.count(2), scores_List.count(3),
               scores_List.count(4), scores_List.count(5), scores_List.count(6), scores_List.count(7),
               scores_List.count(8), scores_List.count(9), scores_List.count(10)]

extra_weights_per_review = np.array([weight_table[score] for score in scores_List])

weighted_mean = np.sum(scores_List * extra_weights_per_review) / np.sum(extra_weights_per_review)



#Printing out Analyzed Data
input("Press Enter to get the Analysed Data...")
print(f"\nWeighted Mean Score: {weighted_mean}")
print(f"Number of \"10\" Score Reviews: {scores_List.count(10)}")
print(f"Number of \"9\" Score Reviews: {scores_List.count(9)}")
print(f"Number of \"8\" Score Reviews: {scores_List.count(8)}")
print(f"Number of \"7\" Score Reviews: {scores_List.count(7)}")
print(f"Number of \"6\" Score Reviews: {scores_List.count(6)}")
print(f"Number of \"5\" Score Reviews: {scores_List.count(5)}")
print(f"Number of \"4\" Score Reviews: {scores_List.count(4)}")
print(f"Number of \"3\" Score Reviews: {scores_List.count(3)}")
print(f"Number of \"2\" Score Reviews: {scores_List.count(2)}")
print(f"Number of \"1\" Score Reviews: {scores_List.count(1)}")
print(f"Number of \"0\" Score Reviews: {scores_List.count(0)}")



#Code Section for Visual Representation of Analysis in Matplotlib

verdict = ""

plt.figure(figsize=(8,6))

#x-axis labels: 1 to 10
scores = np.arange(1, 11)
counts = [np.sum(scores_List == s) for s in scores]

#Bar Chart for scores
plt.bar(scores, counts, color='skyblue', edgecolor='black')

#Title of Anime
plt.xticks(range(1,11))
plt.title(f"$\mathbf{{Anime Name:}}$ {Anime_Name}\n\nReview Score Distribution\n", fontsize=22)

#X-axis and Y-axis Labels.
plt.xlabel("Score", fontsize=14, fontweight="bold")
plt.ylabel("Number of Reviews", fontsize=14, fontweight="bold")

#Getting Verdict for the Anime.
if 8.5 <= weighted_mean <= 10 and total_review_sections > 100:
    verdict = "Highly Recommended! An absolute Must Watch."
elif 8 <= weighted_mean < 8.5 and total_review_sections > 100:
    verdict = "Awesome Reviews! Worth Watching."
elif 7 <= weighted_mean < 8 and total_review_sections > 100:
    verdict = "Average Reviews, May or May not be worth watching."
elif 5 <= weighted_mean < 7 and total_review_sections > 100:
    verdict = "Low reviews. Not Worth it!"
elif 3 <= weighted_mean < 5 and total_review_sections > 100:
    verdict = "Awful Reviews. Absolutely not Worth watching."
elif weighted_mean < 3 and total_review_sections > 100:
    verdict = "One of the Worst Anime ever. Don't Watch!"
elif total_review_sections <= 100:
    verdict = "\n\nAnime can't be Rated. Total Reviews are very low. Either Anime is recently aired or Anime is not very famous."
    print(verdict)
    sys.exit()

#Using LaTeX Style $\mathbf{}$ to bold specific text in a string.
plt.text(5, -0.8, f"\n\n\n$\mathbf{{Overall Score:}}$ {weighted_mean:.2f}\n$\mathbf{{Total Reviews:}}$ {total_review_sections}\n$\mathbf{{Verdict:}}$ {verdict}",
         ha='center', va='top', fontsize=18, transform=plt.gca().transData)

#showing the plt graph.
plt.tight_layout()
plt.show()
