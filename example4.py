import sys
import elemento.elemento as el

notion = el.Notion('elemento/patterns')

f = open("books/if.txt","r+")
text = f.readlines()
notion.process_text(text, verbose=True)

for idee in notion.idees:
    print(idee)
