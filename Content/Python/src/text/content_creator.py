from transformers import pipeline
import sys
import os

from Content.Python.src.core import process_system


def format_output(out):
    str(out)

    return out["generated_text"]

generator = pipeline('text-generation', model ='EleutherAI/gpt-neo-2.7B')
# generator = pipeline('text-generation', model ='EleutherAI/gpt-neo-1.3B')
# generator = pipeline('text-generation', model ='EleutherAI/gpt-neo-125M')

context = sys.argv[1]
# A 3000 value will produce a buffer overflow so we need to prevent that.
text_length = int(sys.argv[2])
output = generator(context, max_length=text_length, do_sample=True, temperature=0.9)

filename = str(context)[:20].replace(" ", "_").replace(",", "").replace(".", "").replace("'", "").replace(":", "") + ".txt"

repo_dir = os.path.join(os.getcwd().split("\n")[0], "contentCreator")

if not os.path.exists(repo_dir):
    os.mkdir(repo_dir)
if process_system.plat() == "Windows":
    filename = repo_dir + "\\" + filename
else:
    filename = repo_dir + "/" + filename
with open(filename, 'w', encoding="utf-8") as f:
    f.write(format_output(output[0]))