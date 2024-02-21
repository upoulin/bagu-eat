import cv2
import os
from collections import defaultdict
import time
import sqlite3 as sql3

orb=None
flann=None
ingredients=[]

#Fill 'ingredients' array with all pictures file names
def loadFiles():
    global ingredients
    ingredients = os.listdir("download")

#Initializes ORB and Flann
def initOrbandFlann():
    global orb,flann
    orb = cv2.ORB_create(700)   #ORB Init
    index_det = dict(algorithm = 6,table_number=10,key_size=20,multi_probe_level=0)
    search = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_det,search) #Flann Init

#Get descriptors for each images
def getDescriptors():
    global flann,ingredients
    for filename in ingredients:
        img2 =cv2.imread("download/"+filename,0)
        kp2, des2 = orb.detectAndCompute(img2, None)
        flann.add([des2])#Add each image descriptor to flann
    flann.train()

#Get a match for a image
#img -> filename of the ingredient
def getMatch(img):
    global kp1, des1,flann
    img1 = cv2.imread(img)
    kp1, des1 = orb.detectAndCompute(img1, None)
    matches= flann.match(des1)
    matches_dict = defaultdict(lambda : 0)
    for f in matches:
        matches_dict[f.imgIdx]+=1
    temp = sorted(matches_dict.items(),key=lambda x:x[1],reverse=True)
    index = next(iter(temp))
    file = ingredients[list(index)[0]]
    return file
    
# agrandissement banque d'image
liste = []
number = []

for root, dirs, files in os.walk("."):
   for name in files:
      liste.append(name)

del liste[0:23]

path = os.getcwd()



# base de donnée plat

basePlat = sql3.connect('basePlat.db')

listePlatIA = []

def name_ingTOid_ing (listeIngredient) :
    #Ne pas enlever la ',' devant 'nomIng' dans le .format()
    return [basePlat.cursor().execute('SELECT id_ing FROM Ingredient WHERE nom_ing = ?',(nomIng,)).fetchall()[0][0] for nomIng in listeIngredient]

#print(name_ingTOid_ing(['apple','tomato sauce','onion']))

def listerPlat (listeIngredient):
    '''
    Arguments :
        listeIngredient = list -> Liste des noms des ingrédients reconnus par l'IA

    Return :
        dictPlat = dict -> Dictionnaire de la forme : {nom du plat : pourcentage}
    '''
    listeIngredient = name_ingTOid_ing (listeIngredient)
    curs = basePlat.cursor()

    #On liste les plats ayant les ingrédients reconnus:
    listPlat = list({curs.execute('SELECT nomPlat FROM Plat WHERE listIng LIKE "%{}%"'.format(id)).fetchall()[0][0] for id in listeIngredient})

    dictPlat = {plat : curs.execute('SELECT listIng FROM Plat WHERE nomPlat = ?',(plat,)).fetchall()[0][0][:-1].split(sep= ';') for plat in listPlat}
    #Calcule du pourcentage des plats :
    for plat in dictPlat.keys() :
        listIngPlat = dictPlat[plat]
        cpt = 0
        for id in listeIngredient:
            if str(id) in listIngPlat :
                cpt += 1
        pourcentage = cpt/len(listIngPlat) * 100
        dictPlat[plat] = pourcentage


    return dictPlat

#print(listerPlat(['tomato sauce','apple','onion'])) 

# compteur de la caméra

img_counter = 0

#/////////////////////////////////////////////////////////

# main
# chargement de la banque d'image
def initialisation():
    """
    fonction initialisation qui initilialise la banque d'image
    """
    print("Initialating ORB")
    initOrbandFlann()
    print("Loading files")
    loadFiles()
    print("Getting images descriptors")
    getDescriptors()
    print("Training FLANN")
    print("Current number of ingredients: "+str(len(flann.getTrainDescriptors())))# nombre d'image présent dans la banque

initialisation()

def scan():

    boucle = True
    while boucle == True:  
            
        image = input("Quelle est votre image ?\n")
        print("Getting match")
        image_match = getMatch(image)# matche de l'image avec une image de la banque
        print(image_match.split("_")[0])
        response = input("is this the right ingredient ?\n")
        if response == "no":
            ingredient = input("what is the right ingredient ?\n")
            for i in liste:
                y = len(ingredient)
                if i[0:y] == ingredient:
                    if i[y] == "_":
                        number.append(int(i[y+1:y+7]))
                        max_number = max(number)
                        max_number += 1
                        max_number = str(max_number)
                        z = len(max_number)
                        z = -z
                        number_of_zero = "000000"
                        final = (ingredient + "_"  + number_of_zero[0:z] + max_number + image[-4:])
                        
            print("image added to database !")
            print(final.split("_")[0])
            listePlatIA.append(final.split("_")[0])
            os.rename(path + image, path + final)
            time.sleep(1)
            os.replace(path + "\\" + final,  path + "\\Download\\" + final)

        else:
            name = image_match.split("_")[0]
            y = len(name)
            for i in liste:
                if i[0:y] == name:
                    if i[y] == "_":
                        number.append(int(i[y+1:y+7]))
                        max_number = max(number)
                        max_number += 1
                        max_number = str(max_number)
                        z = len(max_number)
                        z = -z
                        number_of_zero = "000000"
                        final2 = (name + "_" + number_of_zero[0:z] + max_number + image[-4:])
            
            print("image added to database !")
            print(final2.split("_")[0])
            listePlatIA.append(final2.split("_")[0])
            os.rename(path + image, path + final2)
            time.sleep(1)
            os.replace(path + final2,  path + "\\Download\\" + final2)
            
        sortir = input("Do you want to continue?\n")
        if sortir == "no":
            #print("With the ingredients you have you could make these dishes\n")
            #print(listerPlat(listePlatIA))
            boucle = False


def scan_photo():

    global img_counter
    cv2.namedWindow("window")
    cam = cv2.VideoCapture(0)
    boucle = True
    while boucle == True:   
        ret, frame = cam.read() 

        if not ret:
            print("closing the program")
            boucle = False
        cv2.imshow("window", frame)
        k = cv2.waitKey(1)

        if k%256 == 27:
            # ESC pressed
            print("Esc key pressed, closing...")
            boucle = False
            
        elif k%256 == 32:
            # SPACE pressed
            img_name = "opencv_frame_{}.png".format(img_counter)
            cv2.imwrite(os.path.join(path, img_name), frame)
            # print("{} written!".format(img_name))
            img_counter += 1
            time.sleep(1)
            image = img_name

            
            print("Getting match")
            image_match = getMatch(image)# matche de l'image avec une image de la banque
            print(image_match.split("_")[0])
            response = input("is this the right ingredient ?\n")
            if response == "no":
                ingredient = input("what is the right ingredient ?\n")
                for i in liste:
                    y = len(ingredient)
                    if i[0:y] == ingredient:
                        if i[y] == "_":
                            number.append(int(i[y+1:y+7]))
                            max_number = max(number)
                            max_number += 1
                            max_number = str(max_number)
                            z = len(max_number)
                            z = -z
                            number_of_zero = "000000"
                            final = (ingredient + "_"  + number_of_zero[0:z] + max_number + image[-4:])
                            
                print("image added to database !")
                print(final.split("_")[0])
                listePlatIA.append(final.split("_")[0])
                os.rename(image, final)
                time.sleep(1)
                os.replace(path + "\\" + final,  path + "\\Download\\" + final)

            else:
                name = image_match.split("_")[0]
                y = len(name)
                for i in liste:
                    if i[0:y] == name:
                        if i[y] == "_":
                            number.append(int(i[y+1:y+7]))
                            max_number = max(number)
                            max_number += 1
                            max_number = str(max_number)
                            z = len(max_number)
                            z = -z
                            number_of_zero = "000000"
                            final2 = (name + "_" + number_of_zero[0:z] + max_number + image[-4:])
                
                print("image added to database !")
                print(final2.split("_")[0])
                listePlatIA.append(final2.split("_")[0])
                os.rename(image, final2)
                time.sleep(1)
                os.replace(path + "\\" + final2,  path + "\\Download\\" + final2)
                
            sortir = input("Do you want to continue?\n")
            if sortir == "no":
                boucle = False
                
    cam.release()
    cv2.destroyAllWindows()

def final_rep():
    print("With the ingredients you have you could make these dishes\n")
    print(listerPlat(listePlatIA)) 
