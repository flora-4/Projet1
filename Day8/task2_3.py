import turtle

def draw_polygon(sides):
    if sides < 3:
        print("Un polygone a au moins 3 côtés.")
        return

    angle = 360 / sides
    for _ in range(sides):
        pen.forward(100)
        pen.right(angle)

screen = turtle.Screen()
pen = turtle.Turtle()

draw_polygon(5)

screen.mainloop()

