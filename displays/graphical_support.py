import sys
import tkinter

from graphical_helpers import format_color

# The root window for graphics output.
root_window = None

# The canvas which holds graphics.
canvas = None

# Size of canvas object.
canvas_xs = None
canvas_ys = None

# Current position on canvas.
canvas_x = None
canvas_y = None

# Background color of canvas.
bg_color = None


def begin_graphics(width=640, height=480, color=format_color(0, 0, 0), title=None):
    global root_window, canvas, canvas_xs, canvas_ys, canvas_x, canvas_y, bg_color

    if root_window is not None:
        root_window.destroy()

    canvas_xs, canvas_ys = width - 1, height - 1
    canvas_x, canvas_y = 0, canvas_ys
    bg_color = color

    root_window = tkinter.Tk()
    root_window.protocol('WM_DELETE_WINDOW', destroy_window)
    root_window.title(title or 'Pac-Man Graphical Display')
    root_window.resizable(0, 0)

    try:
        canvas = tkinter.Canvas(root_window, width=width, height=height)
        canvas.pack()
        draw_background()
        canvas.update()
    except RuntimeError:
        root_window = None
        raise


def clear_screen():
    global canvas_x, canvas_y
    canvas.delete('all')
    draw_background()
    canvas_x, canvas_y = 0, canvas_ys


def draw_background():
    corners = [(0, 0), (0, canvas_ys), (canvas_xs, canvas_ys), (canvas_xs, 0)]
    polygon(corners, bg_color, fill_color=bg_color, filled=True, smoothed=False)


def polygon(coordinates, outline_color, fill_color=None, filled=1, smoothed=1, behind=0, width=1):
    c = []
    for coordinate in coordinates:
        c.append(coordinate[0])
        c.append(coordinate[1])

    if fill_color is None:
        fill_color = outline_color

    if filled == 0:
        fill_color = ""

    poly = canvas.create_polygon(c, outline=outline_color, fill=fill_color, smooth=smoothed, width=width)

    if behind > 0:
        canvas.tag_lower(poly, behind)

    return poly


def circle(pos, r, outline_color, fill_color, endpoints=None, style='pieslice', width=2):
    x, y = pos
    x0, x1 = x - r - 1, x + r
    y0, y1 = y - r - 1, y + r

    if endpoints is None:
        e = [0, 359]
    else:
        e = list(endpoints)

    while e[0] > e[1]:
        e[1] = e[1] + 360

    return canvas.create_arc(x0, y0, x1, y1, outline=outline_color, fill=fill_color,
                             extent=e[1] - e[0], start=e[0], style=style, width=width)


def square(pos, r, color, filled=1, behind=0):
    x, y = pos
    coordinates = [(x - r, y - r), (x + r, y - r), (x + r, y + r), (x - r, y + r)]
    return polygon(coordinates, color, color, filled, 0, behind=behind)


def line(here, there, color=format_color(0, 0, 0), width=2):
    x0, y0 = here[0], here[1]
    x1, y1 = there[0], there[1]
    return canvas.create_line(x0, y0, x1, y1, fill=color, width=width)


def text(pos, color, contents, font='Helvetica', size=12, style='normal', anchor="nw"):
    global canvas_x, canvas_y
    x, y = pos
    font = (font, str(size), style)
    return canvas.create_text(x, y, fill=color, text=contents, font=font, anchor=anchor)


def destroy_window():
    sys.exit(0)


def move_to(the_object, x, y=None, d_o_e=None, d_w=tkinter._tkinter.DONT_WAIT):
    if d_o_e is None:
        d_o_e = root_window.dooneevent

    if y is None:
        try:
            x, y = x
        except RuntimeError:
            raise Exception('incomprehensible coordinates')

    horizontal = True
    new_coordinates = []

    current_x, current_y = canvas.coords(the_object)[0:2]

    for coord in canvas.coords(the_object):
        if horizontal:
            inc = x - current_x
        else:
            inc = y - current_y

        horizontal = not horizontal

        new_coordinates.append(coord + inc)

    canvas.coords(the_object, *new_coordinates)
    d_o_e(d_w)


def show():
    root_window.mainloop()


def write_postscript(filename):
    ps_file = open(filename, 'w')
    ps_file.write(canvas.postscript(pageanchor='sw', y='0.c', x='0.c'))
    ps_file.close()


if __name__ == '__main__':
    if sys.version_info < (3, 0):
        print("Graphical Support example requires Python 3.x.")
        sys.exit(1)

    ghost_shape = [
        (0, 0.3),
        (0.25, 0.75),
        (0.5, 0.3),
        (0.75, 0.75),
        (0.75, -0.5),
        (0.5, -0.75),
        (-0.5, -0.75),
        (-0.75, -0.5),
        (-0.75, 0.75),
        (-0.5, 0.3),
        (-0.25, 0.75)
    ]

    begin_graphics()
    clear_screen()
    ghost_shape = [(x * 30 + 20, y * 30 + 20) for x, y in ghost_shape]
    g = polygon(ghost_shape, format_color(.9, 0, 0))
    move_to(g, (50, 50))
    circle((150, 150), 20, format_color(0.7, 0.3, 0.0), format_color(1.0, 0.6, 0.0), endpoints=[15, - 15])
    square((100, 150), 0.5 * 30, color=format_color(0.0 / 255.0, 51.0 / 255.0, 255.0 / 255.0), filled=1, behind=0)
    square((150, 200), 0.5 * 30, color=format_color(0.0 / 255.0, 51.0 / 255.0, 255.0 / 255.0), filled=1, behind=0)
    text((300, 300), format_color(.4, 0.13, 0.91), "SCORE: 0", "Times", 24, "bold")
    line((150, 50), (200, 200), format_color(.1, .75, .7), width=5)
    write_postscript("display.ps")
    show()
