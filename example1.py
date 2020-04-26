import sys
import elemento.elemento as el

notion = el.Notion()

f = open("books/The_pirate_Modi.txt","r+")
text = f.readlines()
notion.process_text(text)
print(notion.idees)
