from manim import *


class CounterClockwise(Scene):
    def construct(self):
        grid = NumberPlane()
        self.add(grid)  # Make sure title is on top of grid
        # grid.prepare_for_nonlinear_transform()
        self.play(
            grid.animate.apply_matrix([[0, -1], [1, 0]]),
            run_time=3,
        )
