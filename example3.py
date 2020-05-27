from summarize import summarize
import sys
import elemento.elemento as el
from colorama import Fore, Style

notion = el.Notion()

filename = sys.argv[1]
f = open("books/"+filename,"r+")
text = f.readlines()

RATIO = float(sys.argv[2])
to_summarize=''.join([phrase for phrase in text])
sentence_count = int(len(text)*RATIO)
summarized = summarize( to_summarize, sentence_count=sentence_count)
notion.process_text(summarized.split('.'), verbose=True)

print( Fore.CYAN)
for idee in notion.idees:
    print(idee)
print( Style.RESET_ALL )
