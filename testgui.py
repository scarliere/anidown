import tkinter as tk
import json

with open("1.json", "r") as read_file:
	epidump = json.load(read_file)
read_file.close()
print(epidump)
m = tk.Tk()
m.geometry("400x400")
m.title('Anidown')
text_box = tk.Text()
for var in epidump.items():
	text_box.insert("1.0", var[0]+"\n")
w = tk.Label(m,text = "Ohaiyo")
w.pack()
def changelabel():
	w.config(text='SEKAI GOOD MORNING WORLD')
def addanime():
	name = entry.get()
	print("New entry: ",name)
	text_box.insert("1.0",name+"\n")
	text_box.pack()
	epidump[name]=["[SubsPlease]",0]
	with open("latest_episodetest.json", "w") as outfile:
		json.dump(epidump, outfile,indent=4)
	outfile.close()
button = tk.Button(m, text='Sekai?', width=25, command=changelabel).pack()
entry = tk.Entry()
entry.pack()
button2 = tk.Button(m, text='Add', width=25, command=addanime).pack()
text_box.pack()
m.mainloop()