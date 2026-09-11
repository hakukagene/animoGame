init python:

    def make_png_sequence(
        folder,
        prefix,
        start_frame,
        end_frame,
        fps=30,
        loop=False
    ):
        frames = []
        frame_time = 1.0 / fps

        for i in range(start_frame, end_frame + 1):

            path = "{}/{}{:05d}.png".format(
                folder,
                prefix,
                i
            )

            frames.extend([
                path,
                frame_time
            ])

        return Animation(
            *frames,
            loop=loop
        )

