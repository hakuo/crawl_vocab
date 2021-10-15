import json
import csv

from urllib.request import urlopen, urlretrieve

urls = [
    "https://www.essentialenglish.review/apps-data/4000-essential-english-words-1/data/data.json",
    "https://www.essentialenglish.review/apps-data/4000-essential-english-words-2/data/data.json",
    "https://www.essentialenglish.review/apps-data/4000-essential-english-words-3/data/data.json",
    "https://www.essentialenglish.review/apps-data/4000-essential-english-words-4/data/data.json",
    "https://www.essentialenglish.review/apps-data/4000-essential-english-words-5/data/data.json",
    "https://www.essentialenglish.review/apps-data/4000-essential-english-words-6/data/data.json"
]

url_template = "https://www.essentialenglish.review/apps-data/4000-essential-english-words-{book}/data/unit-{unit}/wordlist/{filename}"
filename_template= "data/4000W_{index}.{ext}"

word_index = 0
words = []

for idx in range(len(urls)):
    data = urlopen(urls[idx]).read().decode('utf-8-sig')
    data_js = json.loads(data)

    flashcard = data_js["flashcard"]

    for item in flashcard:
        if "wordlist" in item:
            unit = item["en"]
            wordlist = item["wordlist"]

            for word in wordlist:
                word_index = word_index + 1
                word["unit"] = unit.replace("Unit ", "")
                word["book"] = idx + 1
                word["index"] = word_index

                words.append(word)

                # download image
                urlretrieve (url_template.format(book=word["book"],
                                                        unit=word["unit"],
                                                        filename=word["image"]), 
                                                        filename_template.format(index=f'{word["index"]:04d}', ext="jpg"))

                # download audio
                urlretrieve (url_template.format(book=word["book"],
                                                        unit=word["unit"],
                                                        filename=word["sound"]), 
                                                        filename_template.format(index=f'{word["index"]:04d}', ext="mp3"))

with open('wordlist.csv', 'w', newline='') as output_file:
    fc = csv.DictWriter(output_file, 
                        fieldnames=words[0].keys())
    fc.writeheader()
    fc.writerows(words)
