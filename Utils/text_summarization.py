from summarize import summarize
import sys

if (len(sys.argv) < 3 or len(sys.argv) > 4):
    print("Correct usage: ")
    print("python main.py sentence ratio")
    print("Example:")
    print("python main.py \"Bob is cute and quirky. Together they go on wonderful\" 0.2")
ratio = float(sys.argv[2])
to_summarize=sys.argv[1]
sentence_count = int(len(to_summarize.split('.'))*ratio)
summarized = summarize(to_summarize, sentence_count=sentence_count)

print(summarized)

