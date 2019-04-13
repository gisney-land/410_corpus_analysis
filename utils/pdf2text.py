from tika import parser
import os.path
raw = parser.from_file('pdfs/very_difficult.pdf')
save_path = "texts"
complete_name = os.path.join(save_path, "very_difficult.txt")
f = open(complete_name, "w+")
f.write(raw['content'])
f.close()
print(raw['content'])