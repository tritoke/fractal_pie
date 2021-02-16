#!/usr/bin/env python
import numpy as np
from PIL import Image


def main():
    # width/height in pixels
    width = 1000  # 1920
    height = width  # 1080

    # centre of the image - the origin
    image_centre = (0, 0)
    # length along the real axis
    xlen_real = 4.0

    # the parameter for the julia set
    julia_centre = (-0.8, 0.156)

    # number of iterations to run
    iterations = 200

    # get bounding coordinates
    bl, tr = get_bounds(image_centre, xlen_real, width, height)

    # generate the x and y arrays from the bounding coordinates and image things
    xs, ys = get_arrays(bl, tr, width, height)

    its = julia(xs, ys, julia_centre, iterations)
    make_image(its)


def get_bounds(im_centre, xlen, width, height):
    """
    calculate the bottom left and top right coordinates
    """
    x, y = im_centre
    ylen = xlen * (width / height)
    hx = xlen / 2
    hy = ylen / 2
    # bottom left and then top right
    return (x - hx, y - hy), (x + hx, y + hy)


def get_arrays(bottom_left, top_right, width, height):
    """
    generate the x and y coordinate arrays
    """
    # extract the coordinates
    bl_x, bl_y = bottom_left
    tr_x, tr_y = top_right

    # generate one x row and one y column to duplicate
    x_row = np.arange(bl_x, tr_x, (tr_x - bl_x) / width)
    y_col = np.arange(bl_y, tr_y, (tr_y - bl_y) / height)

    xs = np.array([x_row.copy() for _ in range(height)])

    ys = np.array([y_col.copy() for _ in range(width)]).T

    return xs, ys


def julia(xs, ys, julia_centre, iterations):
    """
    This function does the main calculations to generate the fractal
    """
    jx, jy = julia_centre

    # mask of values as they escape
    escaped = xs ** 2 + ys ** 2 > 4.0
    xs[escaped] = 0
    ys[escaped] = 0

    # initialise the iterations taken to escape
    escape_counts = np.zeros(xs.shape, dtype="uint8")

    for i in range(iterations):
        # temp to hold the next xs
        tmps = xs ** 2 - ys ** 2 + jx
        ys = 2 * xs * ys + jy
        xs = tmps

        # calculate the new value of escaped
        new_escaped = xs ** 2 + ys ** 2 > 4.0

        # the newly escaped ones are those which were not escaped last time but now are
        newly_escaped = new_escaped & (~escaped)

        # update the iterations for those that escaped
        escape_counts[newly_escaped] = i + 1
        escaped |= new_escaped

        # set values to zero when escaped
        xs[escaped] = 0
        ys[escaped] = 0

    # those which haven't escaped are declared in the set by making them 0xFF
    escape_counts[~escaped] = 0xFF
    print(np.max(escape_counts))

    return escape_counts


# turn the x/y arrays into a black and white image
def make_image(its):
    # really basic greyscale algorithm
    Image.fromarray(0xFF - its).save("out.png")


# this is just some code to call the main function at the end
# it makes it so that you can write functions in any order
# and just worry about what to put in them :)
if __name__ == "__main__":
    main()
