from elemento import elemento as el

notion=el.Notion('elemento/patterns','elemento/time')

f = open("books/Ginger_the_girafe.txt","r+")
raw_lines = f.readlines()
text=[]
for l in raw_lines:
    if len(l)>0 and l[0]!='\n':
        L=l.split('.')
        text+=L

exclude=['\n']
text=[t for t in text if t not in exclude]

notion.process_text(text, verbose=True)

print(notion)

idees=notion.idees

idees.sort(key=lambda idee: idee.weight)

for idee in notion.idees:
    print(idee.get_words())