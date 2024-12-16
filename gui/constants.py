import json

URL = "http://192.168.19.181/"

with open("waste_desc.json", "r", encoding="utf-8") as file:
    WASTE_DESC = json.load(file)

WASTE_DESC = {
  "paper": {
    "name": "Papier",
    "description": "Odpad został najprawdopodobniej wykonany z papieru. Po zgnieceniu możesz go wrzucić do "
                   "niebieskiego kosza na papier.\n Pamiętaj, że brudny, zatłuszczony papier nie nadaje się do "
                   "segregacji, więc przed wyrzuceniem upewnij się, że jest on czysty.",
    "icon_big": "icons/bin_blue.png",
    "icon_small": "icons/bin_blue_smallp.png"
  },
  "cardboard": {
    "name": "Karton",
    "description": "Odpad został najprawdopodobniej wykonany z kartonu. Po zgnieceniu możesz go wrzucić do "
                   "niebieskiego kosza na karton.\n Pamiętaj, że brudny, zatłuszczony karton nie nadaje się do "
                   "segregacji, więc przed wyrzuceniem upewnij się, że jest on czysty.",
    "icon_big": "icons/bin_blue.png",
    "icon_small": "icons/bin_blue_smallk.png"
  },
  "metal": {
    "name": "Metal",
    "description": "Odpad został najprawdopodobniej wykonany z metalu. Po zgnieceniu możesz go wrzucić do żółtego "
                   "kosza na metal.\n Pamiętaj żeby do tego pojemnika nie wyrzucać zużytych baterii, "
                   "sprzętów elektrycznych i elektronicznych oraz opakowań po farbach i olejach.",
    "icon_big": "icons/bin_yellow.png",
    "icon_small": "icons/bin_yellow_smallm.png"
  },
  "plastic": {
    "name": "Plastik",
    "description": "Odpad został najprawdopodobniej wykonany z tworzywa sztucznego. Po zgnieceniu możesz go wrzucić "
                   "do żółtego kosza na tworzywa sztuczne.\n Pamiętaj żeby do tego pojemnika nie wrzucać opakowań po "
                   "farbach i olejach oraz zabrudzonych opakowań styropianowych.",
    "icon_big": "icons/bin_yellow.png",
    "icon_small": "icons/bin_yellow_smallp.png"
  },
  "glass": {
    "name": "Szkło",
    "description": "Odpad został najprawdopodobniej wykonany ze szkła. Możesz go wrzucić do zielonego kosza na "
                   "szkło.\n Pamiętaj żeby do tego pojemnika nie wyrzucać szkła stołowego, ceramiki, szkła okiennego, "
                   "luster, szyb, żarówek, porcelany oraz potłuczonych naczyń.",
    "icon_big": "icons/bin_green.png",
    "icon_small": "icons/bin_green_small.png"
  },
  "food_organics": {
    "name": "Organiczne",
    "description": "Odpad najprawdopodobniej można wyrzucić do brązowego pojemnika na odpady organiczne.\n Pamiętaj, "
                   "żeby nie wyrzucać tam resztek mięsnych, kości, tłuszczy zwierzęcych, oleju, ziemi i odchodów "
                   "zwierzęcych.",
    "icon_big": "icons/bin_brown.png",
    "icon_small": "icons/bin_brown_small.png"
  },
  "trash": {
    "name": "Zmieszane",
    "description": "Tego odpadu najprawdopodobniej nie da się rozdzielić na odpady segregowalne i powinien trafić do "
                   "szarego kosza na odpady zmieszane.\n Pamiętaj, aby nie wrzucać do niego sprzętu elektronicznego i "
                   "elektrycznego, AGD, baterii i akumulatorów, odpadów budowlanych, odpadów zielonych, leków oraz "
                   "chemikalii.",
    "icon_big": "icons/bin_grey.png",
    "icon_small": "icons/bin_grey_small.png"
  },
  "textile": {
    "name": "Tekstylia",
    "description": "Odpad najprawdopodobniej można wyrzucić do pojemnika na tekstylie - PCK lub Caritas.\n Pamiętaj, "
                   "żeby nie wyrzucać tam zawilgoconych tekstyliów, zanieczyszczonych chemikaliami lub innymi "
                   "substancjami. Jeżeli jest to odzież w dobrym stanie, rozważ oddanie ich do organizacji "
                   "zbierających używane ubrania.",
    "icon_big": "icons/bin_pink.png",
    "icon_small": "icons/bin_pink_small.png"
  },
  "vegetation": {
    "name": "Zielone",
    "description": "Odpad najprawdopodobniej można wyrzucić do brązowego pojemnika na odpady zielone.\n Pamiętaj, "
                   "żeby nie wyrzucać tam kamieni, popiołu, ziemi i odchodów zwierzęcych.",
    "icon_big": "icons/bin_brown.png",
    "icon_small": "icons/bin_brown.png"
  }
}