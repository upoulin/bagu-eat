import tkinter as tk
from PIL import ImageTk, Image
import apprentissage_ia
from collections import defaultdict
import cv2
import time
import os

# initialisation de la fenetre et des images
fenetre = tk.Tk() #Fenetre principale
fenetre.title('Bagu\'eat') #Titre de la fenetre
fenetre.geometry("375x667") #Taille de la fenetre au lancement du programme
fenetre.resizable(width = 0, height = 0) #Pas de redimensionnement de la fenetre
fenetre.configure(bg='#FFF6E4') #Couleur du background   
path = os.getcwd()
path_logo = 'F:/Lycee/Terminale/NSI/Intel/logo.png' #chemin vers le logo de l'application
fenetre.tk.call('wm', 'iconphoto', fenetre._w, tk.PhotoImage(file=path_logo)) #logo qui s'affiche dans la barre des taches
# importation de la photo de bienvenue
img_bienvenue = Image.open('logo.png')
img_resize = img_bienvenue.resize((250, 280))
img = ImageTk.PhotoImage(img_resize)

#////////////////////////////////////////////////////////////////////////

def retour(fonction):
   try:
      fonction
   except:
      pass

liste_ingredient = []


def ajouter_scan(valeur_entre):
   print(valeur_entre)
   image_match = apprentissage_ia.getMatch(valeur_entre)# matche de l'image avec une image de la banque
   ingredient = image_match.split("_")[0]
   return ingredient

def continuer_yes(ingre_ajouter, continuer, btn_yes_continuer, btn_no_continuer):
    # on retire l'ancienne étape
   ingre_ajouter.place_forget()
   continuer.place_forget()
   btn_yes_continuer.place_forget()
   btn_no_continuer.place_forget()

   retour(button1(img))

def retour_btn_no(plat_dispo, plat, retours):
   global liste_ingredient
   plat_dispo.place_forget()
   plat.place_forget()
   retours.place_forget()

   liste_ingredient = []

   retour(button1(img))

def continuer_no(ingre_ajouter, continuer, btn_yes_continuer, btn_no_continuer):
   global liste_ingredient
   # on retire l'ancienne étape
   ingre_ajouter.place_forget()
   continuer.place_forget()
   btn_yes_continuer.place_forget()
   btn_no_continuer.place_forget()

   # on montre les plat que on peut avoir
   plat_dispo = tk.Label(fenetre,  text="Plat pouvans être réaliser !", font=("Dotum",13), bg='#FFF6E4', fg="#294344")
   plat_dispo.place(relx = 0.5, rely = 0.1, anchor=tk.CENTER)

   # à revoir !
   x = apprentissage_ia.listerPlat(liste_ingredient)
   x = str(x)

   plat = tk.Label(fenetre, text = x, font=("Dotum",13), bg='#FFF6E4', fg="#294344")
   plat.place(relx = 0.5, rely = 0.3, anchor=tk.CENTER)

   retours = tk.Button(fenetre, text = "Retour", font = ("Dotum", 15), fg = "#294344", height = 2, width = 15, command= lambda: retour_btn_no(plat_dispo, plat, retours))
   retours.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

# les fonctions :
def bouton_yes_rep(response, ingredient_trouve, btn_yes, btn_no, valeur_nom_img):
   global liste_ingredient
   # on retire l'ancienne étape
   response.place_forget()
   ingredient_trouve.place_forget()
   btn_yes.place_forget()
   btn_no.place_forget()

   liste_ingredient.append(ajouter_scan(valeur_nom_img.get()))
   print(liste_ingredient)

   # message pour dire uqe l'ingrédient à était ajouter
   ingre_ajouter = tk.Label(fenetre,  text="Ingrédient ajouter à la liste !", font=("Dotum",13), bg='#FFF6E4', fg="#294344")
   ingre_ajouter.place(relx = 0.5, rely = 0.1, anchor=tk.CENTER)

   # message pour demander si on veut continuer à scanner des ingrédients
   continuer = tk.Label(fenetre,  text="Voulez-vous continuez à scanner vos ingrédients", font=("Dotum",13), bg='#FFF6E4', fg="#294344")
   continuer.place(relx = 0.5, rely = 0.3, anchor=tk.CENTER)

   # bouton  yes pour continuer
   btn_yes_continuer = tk.Button(fenetre, text = "YES", font = ("Dotum", 15), fg = "#294344", height = 2, width = 15, command = lambda: continuer_yes(ingre_ajouter, continuer, btn_yes_continuer, btn_no_continuer))
   btn_yes_continuer.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

   # bouton no pour continuer
   btn_no_continuer = tk.Button(fenetre, text = "NO", font = ("Dotum", 15), fg = "#294344", height = 2, width = 15, command = lambda: continuer_no(ingre_ajouter, continuer, btn_yes_continuer, btn_no_continuer))
   btn_no_continuer.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

def bouton_rep_no_valider(bon_ingre, valeur_bon_ingre, bouton_valider_bon_ingre):
   global liste_ingredient
   bon_ingre.place_forget()
   valeur_bon_ingre.place_forget()
   bouton_valider_bon_ingre.place_forget()

   liste_ingredient.append(valeur_bon_ingre.get())
   print(liste_ingredient)

   # message pour dire uqe l'ingrédient à était ajouter
   ingre_ajouter = tk.Label(fenetre,  text="Ingrédient ajouter à la liste !", font=("Dotum",13), bg='#FFF6E4', fg="#294344")
   ingre_ajouter.place(relx = 0.5, rely = 0.1, anchor=tk.CENTER)

   # message pour demander si on veut continuer à scanner des ingrédients
   continuer = tk.Label(fenetre,  text="Voulez-vous continuez à scanner vos ingrédients", font=("Dotum",13), bg='#FFF6E4', fg="#294344")
   continuer.place(relx = 0.5, rely = 0.3, anchor=tk.CENTER)

   # bouton  yes pour continuer
   btn_yes_continuer = tk.Button(fenetre, text = "YES", font = ("Dotum", 15), fg = "#294344", height = 2, width = 15, command = lambda: continuer_yes(ingre_ajouter, continuer, btn_yes_continuer, btn_no_continuer))
   btn_yes_continuer.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

   # bouton no pour continuer
   btn_no_continuer = tk.Button(fenetre, text = "NO", font = ("Dotum", 15), fg = "#294344", height = 2, width = 15)
   btn_no_continuer.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

def bouton_no_rep(response, ingredient_trouve, btn_yes, btn_no):
   # on retire l'ancienne étape
   response.place_forget()
   ingredient_trouve.place_forget()
   btn_yes.place_forget()
   btn_no.place_forget()
   
   # demande le bon ingredient
   bon_ingre = tk.Label(fenetre,  text="Quel est le bon ingrédient ?", font=("Dotum",13), bg='#FFF6E4', fg="#294344")
   bon_ingre.place(relx = 0.5, rely = 0.1, anchor=tk.CENTER)

   # entré pour le mettre
   nom_bon_ingre = tk.StringVar()
   valeur_bon_ingre = tk.Entry(fenetre, width=50, textvariable=nom_bon_ingre)
   valeur_bon_ingre.place(relx = 0.5, rely = 0.35, anchor=tk.CENTER)

   # bouton pour valider
   bouton_valider_bon_ingre = tk.Button(fenetre, text = "Valider", font = ("Dotum", 15), fg = "#294344", height = 2, width = 15, command= lambda: bouton_rep_no_valider(bon_ingre, valeur_bon_ingre, bouton_valider_bon_ingre))
   bouton_valider_bon_ingre.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

def reponse_scan(demande_nom, valeur_nom_img, bouton_ajoute_scan):
   demande_nom.place_forget()
   valeur_nom_img.place_forget()
   bouton_ajoute_scan.place_forget()

   # demande utilisateur
   response = tk.Label(fenetre, text="est ce que c'est le bon aliment ?", font=("Dotum",13), bg='#FFF6E4', fg="#294344")
   response.place(relx = 0.5, rely = 0.1, anchor=tk.CENTER)

   # l'ingrédient trouvé
   ingredient_trouve = tk.Label(fenetre, text=ajouter_scan(valeur_nom_img.get()), font=("Dotum",15), bg='#FFF6E4', fg="#294344")
   ingredient_trouve.place(relx = 0.5, rely = 0.3, anchor=tk.CENTER)

   # bouton yes
   btn_yes = tk.Button(fenetre, text = "YES", font = ("Dotum", 15), fg = "#294344", height = 2, width = 15, command = lambda: bouton_yes_rep(response, ingredient_trouve, btn_yes, btn_no, valeur_nom_img))
   btn_yes.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

   # bouton no
   btn_no = tk.Button(fenetre, text = "NO", font = ("Dotum", 15), fg = "#294344", height = 2, width = 15, command = lambda: bouton_no_rep(response, ingredient_trouve, btn_yes, btn_no))
   btn_no.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

def reponse_scan_photo(img_name):
   # demande utilisateur
   response = tk.Label(fenetre, text="est ce que c'est le bon aliment ?", font=("Dotum",13), bg='#FFF6E4', fg="#294344")
   response.place(relx = 0.5, rely = 0.1, anchor=tk.CENTER)

   # l'ingrédient trouvé
   ingredient_trouve = tk.Label(fenetre, text=ajouter_scan(img_name), font=("Dotum",15), bg='#FFF6E4', fg="#294344")
   ingredient_trouve.place(relx = 0.5, rely = 0.3, anchor=tk.CENTER)

   # bouton yes
   btn_yes = tk.Button(fenetre, text = "YES", font = ("Dotum", 15), fg = "#294344", height = 2, width = 15, command = lambda: bouton_yes_rep(response, ingredient_trouve, btn_yes, btn_no, img_name))
   btn_yes.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

   # bouton no
   btn_no = tk.Button(fenetre, text = "NO", font = ("Dotum", 15), fg = "#294344", height = 2, width = 15, command = lambda: bouton_no_rep(response, ingredient_trouve, btn_yes, btn_no))
   btn_no.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

def button_scan_data(button_scan, button_scan_photo, data):
   # on retrire les ancien élément
   data.place_forget()
   button_scan.place_forget()
   button_scan_photo.place_forget()
   # on demande ce que on veut
   demande_nom = tk.Label(fenetre, text="Quel est le chemin vers votre image ?", font=("Dotum",13), bg='#FFF6E4', fg="#294344")
   demande_nom.place(relx = 0.5, rely = 0.1, anchor=tk.CENTER)
   # et on écrit
   nom_img = tk.StringVar()
   valeur_nom_img = tk.Entry(fenetre, width=50, textvariable=nom_img)
   valeur_nom_img.place(relx = 0.5, rely = 0.35, anchor=tk.CENTER)

   # bouton pour ajouter l'ingrédient
   bouton_ajoute_scan = tk.Button(fenetre, text = "Ajouter", font = ("Dotum", 15), fg = "#294344", height = 2, width = 15, command = lambda: reponse_scan(demande_nom, valeur_nom_img, bouton_ajoute_scan))
   bouton_ajoute_scan.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

def bouton_yes_photo_rep(rep, ingredient_trouve, btn_yes, btn_no, img_scan):
   global liste_ingredient
   
   rep.place_forget()
   ingredient_trouve.place_forget()
   btn_yes.place_forget()
   btn_no.place_forget()

   liste_ingredient.append(img_scan)

   # message pour dire uqe l'ingrédient à était ajouter
   ingre_ajouter = tk.Label(fenetre,  text="Ingrédient ajouter à la liste !", font=("Dotum",13), bg='#FFF6E4', fg="#294344")
   ingre_ajouter.place(relx = 0.5, rely = 0.1, anchor=tk.CENTER)

   # message pour demander si on veut continuer à scanner des ingrédients
   continuer = tk.Label(fenetre,  text="Voulez-vous continuez à scanner vos ingrédients", font=("Dotum",13), bg='#FFF6E4', fg="#294344")
   continuer.place(relx = 0.5, rely = 0.3, anchor=tk.CENTER)

   # bouton  yes pour continuer
   btn_yes_continuer = tk.Button(fenetre, text = "YES", font = ("Dotum", 15), fg = "#294344", height = 2, width = 15, command = lambda: continuer_yes(ingre_ajouter, continuer, btn_yes_continuer, btn_no_continuer))
   btn_yes_continuer.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

   # bouton no pour continuer
   btn_no_continuer = tk.Button(fenetre, text = "NO", font = ("Dotum", 15), fg = "#294344", height = 2, width = 15, command = lambda: continuer_no(ingre_ajouter, continuer, btn_yes_continuer, btn_no_continuer))
   btn_no_continuer.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

img_counter = 0

def photo_scan():
   global img_counter
   cv2.namedWindow("window")
   cam = cv2.VideoCapture(0)
   boucle = True
   while boucle == True:   
      ret, frame = cam.read()
      if not ret:
         print("fermeture du programme")
         boucle = False
      cv2.imshow("window", frame)
      k = cv2.waitKey(1)
      if k%256 == 27:
         # ESC pressed
         print("touche Echap pressée, fermeture...")
         boucle = True
      elif k%256 == 32:
         # SPACE pressed
         img_name = "opencv_frame_{}.png".format(img_counter)
         cv2.imwrite(os.path.join(path, img_name), frame)
         print("{} written!".format(img_name))
         img_counter += 1
         cam.release()
         cv2.destroyAllWindows()
         time.sleep(1)
         boucle = False
         return img_name

def valeur_img_scan():
   img_scan = photo_scan()
   x = ajouter_scan(img_scan)
   return x

def button_photo_scan(data, button_scan, button_scan_photo):
   data.place_forget()
   button_scan.place_forget()
   button_scan_photo.place_forget()

   img_scan = valeur_img_scan()

   rep = tk.Label(fenetre, text = "est ce que c'est le bon aliment ?",font=("Dotum", 13), bg='#FFF6E4', fg="#294344")
   rep.place(relx=0.5, rely=0.1, anchor = tk.CENTER)

   # l'ingrédient trouvé
   ingredient_trouve = tk.Label(fenetre, text=img_scan, font=("Dotum",15), bg='#FFF6E4', fg="#294344")
   ingredient_trouve.place(relx = 0.5, rely = 0.3, anchor=tk.CENTER)

   # bouton yes
   btn_yes = tk.Button(fenetre, text = "YES", font = ("Dotum", 15), fg = "#294344", height = 2, width = 15, command= lambda: bouton_yes_photo_rep(rep, ingredient_trouve, btn_yes, btn_no, img_scan))
   btn_yes.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

   # bouton no
   btn_no = tk.Button(fenetre, text = "NO", font = ("Dotum", 15), fg = "#294344", height = 2, width = 15)
   btn_no.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

# button pour les scan
def scanbutton():

   #Cette fonction est l'action renvoyée par le bouton scan, il faudrait intégrer le scan réel
   data = tk.Label(fenetre, text = 'Comment voulez-vous scanner vos aliments ?',font=("Dotum", 13), bg='#FFF6E4', fg="#294344")
   data.place(relx=0.5, rely=0.1, anchor = tk.CENTER) #Ecriture de base

   # bouton pour le scan sans la photo
   button_scan = tk.Button(fenetre, text = "Par bibliothèque", font = ("Dotum", 15), fg = "#294344", height = 2, width = 15, command = lambda: button_scan_data(button_scan, button_scan_photo, data))
   button_scan.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

   # bouton pour le scan avec la photo
   button_scan_photo = tk.Button(fenetre, text = "Par photo", font = ("Dotum", 15), fg = "#294344", height = 2, width = 15, command= lambda: button_photo_scan(data, button_scan, button_scan_photo))
   button_scan_photo.place(relx=0.5, rely=0.6, anchor=tk.CENTER)


# supprimer les images de bienvenue et lancer les bouton de scan
def button1_data(btn, Bienvenu, panel_bienvenue):
   scanbutton()
   btn.place_forget()
   Bienvenu.place_forget()
   panel_bienvenue.place_forget()

# bouton de bienvenue pour le scan
def button1(img):
   # photo de bienvenue
   # importation

   panel_bienvenue = tk.Label(fenetre, image = img, bg="#FFF6E4")
   panel_bienvenue.place(relx = 0.5, rely = 0.40, anchor = tk.CENTER)

   Bienvenu = tk.Label(fenetre, text='Bienvenu sur Bagu\'eat', font=("Dotum",20),bg='#FFF6E4',fg="#294344") #Création message bienvenu
   Bienvenu.place(relx = 0.5, rely = 0.1, anchor=tk.CENTER) #Affichage du message de bienven

   #Integration du bouton pour scanner
   btn_bienvenue = tk.Button(fenetre, text="Scan",font=("Dotum",15), fg='#294344', height = 2, width = 15, command = lambda: button1_data(btn_bienvenue, Bienvenu, panel_bienvenue))
   btn_bienvenue.place(relx=0.5, rely=0.75, anchor=tk.CENTER)

button1(img)

#///////////////////////////////////////////////////////////////////////////////
                
#Lancement de la fenetre
fenetre.mainloop()
