import tkinter
from tkinter import *
from requests import get
from json import loads
from PIL import ImageTk, Image
from shutil import copyfileobj

window = tkinter.Tk()
window.title("Scryfall Search - ALPHA")
window.minsize(width=600, height=800)

title = tkinter.Label(text="Scryfall Search", font=("Arial", 24, "bold"))
title.pack(side=TOP, padx=10,pady=10) 

mtg_card_back = Image.open("back.jpg").resize((388,580))
mtg_card_back_img = ImageTk.PhotoImage(mtg_card_back)
card_placeholder = tkinter.Label(image=mtg_card_back_img)
card_placeholder.pack()



input = Entry(width=50) 
input.pack(side=TOP, padx=10,pady=10)


def flip_card():
    random_mtg_card = Image.open("reverse.jpg").resize((388,580))
    new_mtg_card = ImageTk.PhotoImage(random_mtg_card)
    card_placeholder.configure(image=new_mtg_card)
    card_placeholder.image = new_mtg_card

def search_clicked():
    new_search = input.get()
    print(new_search)
    card = loads(get(f"https://api.scryfall.com/cards/named?fuzzy={new_search}").text)
    mtg_title = card['name']
    try:
        img_url  = card['image_uris']['large']
    except:
        img_url  = card['card_faces'][0]['image_uris']['large']
        with open('image.jpg', 'wb') as out_file:
            copyfileobj(get(img_url , stream = True).raw, out_file)

        img_url2 = card['card_faces'][1]['image_uris']['large']
        with open('reverse.jpg', 'wb') as out_file:
            copyfileobj(get(img_url2, stream = True).raw, out_file)
        
        search = tkinter.Button(text="Flip", command=flip_card)
        search.pack(side=RIGHT)

    else:
        with open('image.jpg', 'wb') as out_file:
            copyfileobj(get(img_url, stream = True).raw, out_file)
        

    random_mtg_card = Image.open("image.jpg").resize((388,580))
    new_mtg_card = ImageTk.PhotoImage(random_mtg_card)
    card_placeholder.configure(image=new_mtg_card)
    card_placeholder.image = new_mtg_card
    print(mtg_title)


search = tkinter.Button(text="Summon Card", command=search_clicked)
search.pack(side=TOP)


window.mainloop()