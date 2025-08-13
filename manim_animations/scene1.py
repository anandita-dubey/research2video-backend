from manim import *

class SimpleScene(Scene):
    def construct(self):
        title = Text("Mobile Devices in Language Learning")
        self.play(Write(title))
        self.wait(1)

        graph = Line(start=LEFT*3 + DOWN, end=RIGHT*3 + UP*2)
        self.play(Create(graph))
        self.wait(1)

        circle = Circle(radius=1, color=BLUE)
        self.play(GrowFromCenter(circle))
        self.wait(1)

        self.play(FadeOut(title), FadeOut(graph), FadeOut(circle))