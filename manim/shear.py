"""
Shear transformation:
[[ 1, 0],
 [ 1, 1]]
"""
from manim import *


class Shear(Scene):
    def construct(self):
        grid = NumberPlane()
        self.add(grid)  # Make sure title is on top of grid
        # grid.prepare_for_nonlinear_transform()
        self.play(
            grid.animate.apply_matrix([[1, 1], [0, 1]]),
            run_time=3,
        )
