
from manim import *

class DynamicTextScene(Scene):
    def construct(self):
        text = Text(r"""Introduction to the research topic and its significance in language learning.""", font_size=36, line_spacing=1.2)
        self.play(Write(text))
        self.wait(2)
