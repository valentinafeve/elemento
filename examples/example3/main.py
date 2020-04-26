import sys
sys.path.insert(1, '../../elemento')
import elemento as el

notion = el.Notion()

f = open("../books/The_pirate_Modi.txt","r+")
text = f.readlines()
notion.process_text(text)
print(notion.idees)
