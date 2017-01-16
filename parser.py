import re


def moveinline(x, y):
    print("> moveinline(" + x + ", " + str(y) + ")")

def movetopoint(x):
    print("> movetopoint(" + x + ")")

def detonate():
    print("> detonate()")

def movebombinline(x, y):
    print("> moveinline(" + x + ", " + str(y) + ")")

def movebombtopoint(x):
    print("> movebomb(" + x + ")")

def defuse(x):
    print("> defuse(" + x + ")")

actionlist = {"zmień":"move", "przejdź":"move", "dojdź":"move", "idź":"move", "jedź":"move", "pojedź":"move",
            "przejedź":"move", "dojedź":"move", "dotrzyj":"move", "podjedź":"move", "podejdź":"move",
            "detonuj":"detonate", "zniszcz":"detonate", "niszcz":"detonate", "zdetonuj":"detonate", "przetnij":"defuse",
            "rozbrój":"defuse", "rozbrajaj":"defuse", "przesuń":"movebomb", "przenieś":"movebomb", "zanieś":"movebomb",
            "podnieś":"movebomb"}

numbers = {"jedną":1, "1":1, "dwie":2, "2":2, "trzy":3, "3":3, "cztery":4, "4":4, "pięć":5, "5":5, "sześć":6, "6":6, "siedem":7, "7":7, "osiem":8,
           "8":8, "dziewięć":9, "9":9}

directions = {"góry":"up", "górę":"up", "północ":"up", "górny":"up", "góra":"up", "górnym":"up", "północnym":"up", "północny":"up", "północy":"up", "prawo":"right",
              "wschód":"right", "wschodni":"right", "wschodnim":"right", "lewo":"left", "zachód":"left", "zachodnim":"left", "zachodni":"left", "dół":"down", "dołu":"down", "południe":"down",
              "południową":"down", "południowy":"down", "dolny":"down", "dolnym":"down", "południowym":"down"}

randomstring = "przejedź na pozycję D5, zmień lokalizację na E2 i przesuń się o 9 kratek w lewo, dotrzyj na pole C5, podnieś bombę, zanieś ją na pole E6, zdetonuj bombę, przesuń się do góry o 5 kratek, idź w lewo 3 razy, przesuń bombę na F7, idź na A4, rozbrajaj, podejdź na B5, detonuj, jedź na pole G9, rozbrajaj ładnuek, przetnij, idź 5 kratek na zachód, dojedź na B7, dojdź na H8, idź w górę 5 kratek, podejdź do miny na A2, detonuj bombę"

splitted = randomstring.lower().replace('.', ',').replace(" i ", ",").split(",")

pattern = re.compile("[a-zA-Z]\d")



for i in range(len(splitted)): #pojedyncze komendy
    commandsinglewords = splitted[i].split()
    order = ["", "", ""]
    print(splitted[i])
    for word in commandsinglewords:
        for action, key in actionlist.items():
            if word == action:
                order[0] = key
        for direction, key in directions.items():
            if word == direction:
                order[1] = key
        for number, key in numbers.items():
            if word == number:
                order[2] = key
        if re.match(pattern, word):
            order[2] = word
    if order[0]=="move":
        if order[1]=="":
            movetopoint(order[2])
        else:
            moveinline(order[1], order[2])
    elif order[0]=="detonate":
        detonate()
    elif order[0]=="movebomb":
        if order[1]=="":
            movebombtopoint(order[2])
        else:
            movebombinline(order[1], order[2])
    elif order[0]=="defuse":
        defuse(order[2])


'''
for i in range(len(splitted)): #pojedyncze komendy
    commandsinglewords = splitted[i].split()
    order = ["", "", ""]
    print(splitted[i])
    for j in range(len(commandsinglewords)):
        for k in range(18):
            if commandsinglewords[j] == movelist[k] and not splitted[i].__contains__("bomb"):
                order[0] = "move"
            elif commandsinglewords[j] == defusionlist[k]:
                order[0] = "defuse"
            elif commandsinglewords[j] == detonatelist[k]:
                order[0] = "detonate"
            elif commandsinglewords[j] == movebomblist[k]:
                order[0] = "movebomb"
            elif commandsinglewords[j] == directions[k]:
                order[1] = commandsinglewords[j]
            elif commandsinglewords[j] == numbers[k]:
                order[2] = commandsinglewords[j]
        if re.match(pattern, commandsinglewords[j]):
            order[2] = commandsinglewords[j]
    if order[0]=="move":
        if order[1]=="":
            movetopoint(order[2])
        else:
            moveinline(order[1], order[2])
    elif order[0]=="detonate":
        detonate(order[2])
    elif order[0]=="movebomb":
        movebomb(order[2])
    elif order[0]=="defuse":
        defuse(order[2])
'''