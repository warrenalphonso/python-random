"""
Projection onto y-axis:
[[ 0, 0],
 [ 0, 1]]
"""
from manim import *


class Projection(Scene):
    def construct(self):
        grid = NumberPlane()
        self.add(grid)  # Make sure title is on top of grid

        self.play(
            grid.animate.apply_matrix([[0, 0], [0, 1]]),
            run_time=3,
        )
