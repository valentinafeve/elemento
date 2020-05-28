import elemento.elemento as el
import sys

notion = el.Notion()
notion.process_text([sys.argv[1]], verbose=True)

questions = []
for idee in notion.idees:
    questions.extend( el.generate_questions( idee ))

print(questions)
