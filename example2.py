import sys
import elemento.elemento as el
from colorama import Fore, Style

notion = el.Notion()

f = open("books/1_Heart_of_gold.txt","r+")
text = f.readlines()
notion.process_text(text, verbose=True)
print(notion.idees)

questions = []
for idee in notion.idees:
    questions.extend( el.generate_questions( idee ))

print( Fore.RED)
print("QUESTIONS:")
for question in questions:
    print("Question:", question["question"])
    print("Answer:", question["answer"])
    print("\n")
print( Style.RESET_ALL )
