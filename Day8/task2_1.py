import turtle

# Créer une fenêtre et une "tortue"
screen = turtle.Screen()
pen = turtle.Turtle()

# Dessiner un carré
for _ in range(4):
    pen.forward(100)
    pen.right(90)

screen.mainloop()
