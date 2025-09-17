import random

def decision(setting):
        if setting >= 12:
                print("you loose!")
decision(14)

def Next_brick():
        list=[1,2,3,4,5,6]
        print(random.choice(list))
Next_brick()
