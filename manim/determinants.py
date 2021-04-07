"""

"""
from manim import *


class Two(Scene):
    def construct(self):
        grid = NumberPlane()
        self.add(grid)
        self.play(
            grid.animate.apply_matrix([[1, 0], [1, 2]]),
            run_time=3
        )
