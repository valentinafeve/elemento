import sys
import elemento.elemento as el

notion = el.Notion()

f = open("books/Modi0.txt","r+")
text = f.readlines()
notion.process_text(text)

for idee in notion.idees:
    print(idee.dictionary)
    print(idee.time)
