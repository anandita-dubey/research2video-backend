from manim import *

class BarChartScene(Scene):
    def construct(self):
        axes = Axes(x_range=[0,5], y_range=[0,10])
        bars = VGroup(*[
            Rectangle(width=0.5, height=h, fill_color=BLUE, fill_opacity=0.75)
            for h in [3, 7, 5, 8]
        ])
        for i, bar in enumerate(bars):
            bar.next_to(axes.coords_to_point(i+1, 0), UP, buff=0)
        self.play(Create(axes), *[GrowFromEdge(bar, edge=DOWN) for bar in bars])
        self.wait(2)

class TextHighlightScene(Scene):
    def __init__(self, text="This is a test sentence", highlight_words=None, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.highlight_words = highlight_words or ["test", "sentence"]

    def construct(self):
        txt = Text(self.text, font_size=30)
        self.add(txt)
        for word in self.highlight_words:
            if word in self.text:
                idx = self.text.index(word)
                highlight = SurroundingRectangle(txt[idx:idx+len(word)], color=YELLOW)
                self.play(Create(highlight))
        self.wait(2)