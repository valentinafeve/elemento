import sys
import elemento.elemento as el
from colorama import Fore, Style
import gensim.downloader as api

print("Loading models...")
model = api.load("glove-wiki-gigaword-300")
print("Models loaded")

notion = el.Notion(model=model)

filename = sys.argv[1]
f = open("books/"+filename, "r+")
text = f.readlines()
notion.process_text(text, verbose=True, solve_pronouns=True)

questions = []
for idee in notion.idees:
    questions.extend(el.generate_questions(idee))

print("QUESTIONS:")
for question in questions:
    print("Question:", question["question"])
    print("Answer:", question["answer"])
    print("\n")
print( Style.RESET_ALL )
