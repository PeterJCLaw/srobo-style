#!/usr/bin/env python

from __future__ import print_function

import argparse
import os.path
import subprocess

# There are four parts to the spinner, so we only need to actually have
# explicit frames for a quarter-turn -- after that we can just loop and
# it will look like the rotation continues anyway.

QUARTER_ROTATION_DURATION_MS = 600
NUM_FRAMES = 10

IMAGEMAGIC_TICK_LEN_MS = 10
TICKS_PER_FRAME = QUARTER_ROTATION_DURATION_MS / (NUM_FRAMES * IMAGEMAGIC_TICK_LEN_MS)

FRACTION_PER_FRAME = 1.0 / NUM_FRAMES

BACKGROUND_COLOUR = '#3270ED'

WIDTH, HEIGHT = (52, 52)


def create_frame_svg(bld_dir, template, frame_id):
    WIDTH = 760
    assert 'svg width="760px" height="760px" viewBox="0 0 760 760"' in template

    fraction = 1 - frame_id * FRACTION_PER_FRAME
    inset = WIDTH * frame_id * FRACTION_PER_FRAME / 2

    content = template.replace(
        '<g id="Symbol" ',
        '<g id="Symbol" transform="translate({} 0) scale({} 1)" '.format(
            inset,
            fraction,
        ),
    )

    frame_name = 'spinner-frame-{}.svg'.format(frame_id)
    frame_path = os.path.join(bld_dir, frame_name)

    with open(frame_path, 'w') as f:
        f.write(content)

    return frame_path


def create_png_from_svg(svg_file):
    assert svg_file[-4:] == '.svg', "Expected an SVG file"

    png_file = '{}.png'.format(svg_file[:-4])

    subprocess.check_call([
        'inkscape',
        '--export-png={}'.format(png_file),
        '--export-width={}'.format(WIDTH),
        '--export-height={}'.format(HEIGHT),
        '--export-background={}'.format(BACKGROUND_COLOUR),
        svg_file,
    ])

    return png_file


def create_animation(frame_paths, target_file):
    assert frame_paths, "Expected some frames to convert"

    args = [
        'convert',
        '-delay', str(TICKS_PER_FRAME),
        '-loop', '0',
    ] + frame_paths + [target_file]

    subprocess.check_call(args)


def main():
    my_dir = os.path.dirname(__file__)
    bld_dir = os.path.join(my_dir, 'bld')
    template_file = os.path.join(my_dir, 'logo-white.svg')
    animation_file = os.path.join(my_dir, 'spinner.gif')

    if not os.path.exists(bld_dir):
        os.mkdir(bld_dir)

    with open(template_file, 'r') as f:
        template = f.read()

    frame_paths = []

    for frame_id in range(NUM_FRAMES):
        frame_svg_path = create_frame_svg(bld_dir, template, frame_id)
        frame_png_path = create_png_from_svg(frame_svg_path)
        frame_paths.append(frame_png_path)

    frame_paths += reversed(frame_paths)

    create_animation(frame_paths, animation_file)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Create an animated GIF spinner from an SVG template."
        "Uses Inkscape to convert from SVG to PNG and Imagemagic to "
        "create the GIF.",
    )
    parser.parse_args()
    main()
