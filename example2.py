import sys
import elemento.elemento as el
from colorama import Fore, Style

notion = el.Notion()

filename = sys.argv[1]
f = open("books/"+filename,"r+")
text = f.readlines()
notion.process_text(text, verbose=True)

questions = []
for idee in notion.idees:
    questions.extend( el.generate_questions( idee ))

print( Fore.YELLOW)
print("QUESTIONS:")
for question in questions:
    print("Question:", question["question"])
    print("Answer:", question["answer"])
    print("\n")
print( Style.RESET_ALL )
