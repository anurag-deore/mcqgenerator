from flask import Flask, render_template, request
import generator
import os

app = Flask("__app__")

@app.route('/')
def index():
    return render_template("index_copy.html")

@app.route('/about')
def about():
    return render_template('about_copy.html')

@app.route('/getMCQ', methods = ["POST", "GET"])
def getMCQ():
    if request.method == "POST":
        inptype = request.form['inptype']
        if inptype == 'file':
            file = request.files['myFile']
            file_content = file.read()
            file_content = file_content.decode("utf-8")   
        elif inptype == 'text':
            file_content = request.form['inputtext']  
        full_text, summarized_text, mcq_dict = generator.mcq_generate(file_content)
        # full_text = file_content
        # summarized_text = "The Nile River fed Egyptian civilization for hundreds of years. The river is called the upper Nile in the south and the lower Nile in the north. This soil was fertile, which means it was good for growing crops. Red Land, Black Land The ancient Egyptians lived in narrow bands of land on each side of the Nile. The red land was the barren desert beyond the fertile region. Isolation The harsh desert acted as a barrier to keep out enemies. When the birds arrived, the annual flood waters would soon follow. They were the first to grind wheat into flour and to mix the flour with yeast and water to make dough rise into bread. Egyptians often painted walls white to reflect the blazing heat. Veins (long streaks) of copper, iron, and bronze were hidden inside desert mountains in the hot Sinai Peninsula, east of Egypt. One ancient painting even shows a man ready to hit a catfish with a wooden hammer. A boomerang is a curved stick that returns to the person who threw it.) Eventually, Egyptians equipped their reed boats with sails and oars. Going south, they raised a sail and let the winds that blew in that direction push them. The Nile provided so well for Egyptians that sometimes they had surpluses, or more goods than they needed. Ancient Egypt had no money, so people exchanged goods that they grew or made. This prosperity made life easier and provided greater opportunities for many Egyptians. For example, some ancient Egyptians learned to be scribes, people whose job was to write and keep records. Some skilled artisans erected stone or brick houses and temples. These traders took Egyptian products such as scrolls, linen, gold, and jewelry. They brought back exotic woods, animal skins, and live beasts. Egyptians created a government that divided the empire into 42 provinces. Many officials worked to keep the provinces running smoothly. Before entering a temple, a priest bathed and put on special linen garments and white sandals. In Egypt, people became slaves if they owed a debt, committed a crime, or were captured in war. Unlike other ancient African cultures, in Egyptian society men and women had fairly equal rights. For example, they could both own and manage their own property. The main job of most women was to care for their children and home, but some did other jobs too. Boys and some girls from wealthy families went to schools run by scribes or priests. As in many ancient societies, much of the knowledge of Egypt came about as priests studied the world to find ways to please the gods. Doctors believed that the heart controlled thought and the brain circulated blood, which is the opposite of what is known now. Early Egyptians created a hieroglyphic system with about 700 characters. Egyptians cut the stems into strips, pressed them, and dried them into sheets that could be rolled into scrolls. Legend says a king named Narmer united Upper and Lower Egypt. Some historians think Narmer actually represents several kings who gradually joined the two lands. When a king died, one of his children usually took his place as ruler. The order in which members of a royal family inherit a throne is called the succession. Historians divide ancient Egyptian dynasties into the Old Kingdom, the Middle Kingdom, and the New Kingdom. The Old Kingdom started about 2575 B.C., when the Egyptian empire was gaining strength. The word pharaoh meant “great house,” and it was originally used to describe the king’s palace. Egyptians believed that if the pharaoh and his subjects honored the gods, their lives would be happy. The first rulers of Egypt were often buried in an underground tomb topped by mud brick."
        # mcq_dict = {1: {'question': '________ cut the stems into strips, pressed them, and dried them into sheets that could be rolled into scrolls.', 'options': ['Angolan', 'Bantu', 'Egyptians', 'Algerian'], 'answer': 'Egyptians'}, 2: {'question': 'The ________ provided so well for Egyptians that sometimes they had surpluses, or more goods than they needed.', 'options': ['Entebbe', 'Buganda', 'Nile', 'Gulu'], 'answer': 'Nile'}, 3: {'question': 'As in many ancient societies, much of the knowledge of ________ came about as priests studied the world to find ways to please the gods.', 'options': ['Egypt', 'Saudi Arabia', 'Iraq','Kuwait'], 'answer': 'Egypt'}, 4: {'question': 'The river is called the ________ Nile in the south and the lower Nile in the north.', 'options': ['Upper', 'counter', 'quarter', 'saddle'], 'answer': 'Upper'}, 5: {'question': 'Legend says a king named Narmer united Upper and ________.', 'options': ['Lower egypt', 'Eastern Desert', 'Aswan High Dam', 'Aswan'], 'answer': 'Lower egypt'}, 6: {'question': '________ says a king named Narmer united Upper and Lower Egypt.', 'options': ['adventure story', 'love story', 'fable', 'Legend'], 'answer': 'Legend'}}
    return render_template("getMCQ_copy.html", MCQ = mcq_dict, full_text = full_text, summarized_text = summarized_text)

if __name__ == "__main__":
    app.run(debug = True)