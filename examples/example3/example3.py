import sys
sys.path.insert(1, '../../elemento')
import elemento as el

notion = el.Notion()

f = open("../books/Modi0.txt","r+")
text = f.readlines()
notion.process_text(text)
print(notion.idees)
