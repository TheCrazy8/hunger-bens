import random

dicty = {
    "ben1": {
        "name": "Ben", "gender": "male"
    },
    "ben2": {
        "name": "Ben's Mom", "gender": "female"
    },
    "ben3" :{
        "name": "BenBot 3000", "gender": "object"
    }
}

listofbens = []
listofage = []
for x, obj in dicty.items():
    listofbens.append(dicty[x]["name"])
    listofage.append(dicty[x]["age"])

