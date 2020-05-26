from summarize import summarize
import sys
import elemento.elemento as el

"""
python example5.py 0.3
"""

notion = el.Notion()

f = open("books/The_pirate_Modi.txt","r+")
text = f.readlines()

RATIO = float(sys.argv[1])
to_summarize=''.join([phrase for phrase in text])
sentence_count = int(len(text)*RATIO)
summarized = summarize( to_summarize, sentence_count=sentence_count)
notion.process_text(summarized.split('.'), verbose=True)

for idee in notion.idees:
    print(idee)
