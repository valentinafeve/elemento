import sys
import elemento.elemento as el
from colorama import Fore, Style

notion = el.Notion()

filename = sys.argv[1]
f = open("books/"+filename,"r+")
text = f.readlines()
notion.process_text(text, verbose=True)

print( Fore.CYAN )
for idee in notion.idees:
    print(idee)
print( Style.RESET_ALL )
