import turtle

LARGEUR, HAUTEUR = 640, 400

if __name__ == "__main__":
    turtle.setup(LARGEUR, HAUTEUR)
    turtle.speed("fast") #Met la vitesse de traçage à rapide
    ecart = 1
    for i in range(30):
        turtle.left(30)
        #turtle.up(); turtle.forward(ecart); turtle.down()
        turtle.forward(ecart)
        ecart += 3
    turtle.exitonclick()

