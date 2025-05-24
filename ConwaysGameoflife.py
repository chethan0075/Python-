print("Chethan U, 1AY24AI025, SEC-M")
# Conwaysgameoflife.py

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def update(frame_num, img, grid, rows, cols):
    """
    Compute one step of Conway's Game of Life and update the image.
    """
    new_grid = grid.copy()
    for r in range(rows):
        for c in range(cols):
            # count alive neighbours (with wrap-around)
            total = (
                grid[(r-1)%rows, (c-1)%cols] + grid[(r-1)%rows, c] + grid[(r-1)%rows, (c+1)%cols] +
                grid[r, (c-1)%cols]                         + grid[r, (c+1)%cols] +
                grid[(r+1)%rows, (c-1)%cols] + grid[(r+1)%rows, c] + grid[(r+1)%rows, (c+1)%cols]
            )
            # Apply Conway's rules
            if grid[r, c] == 1:
                if total < 2 or total > 3:
                    new_grid[r, c] = 0
            else:
                if total == 3:
                    new_grid[r, c] = 1
    # update data
    img.set_data(new_grid)
    grid[:] = new_grid[:]
    return img,

def main():
    print("Conway's Game of Life")
    try:
        rows = int(input("Grid rows (e.g. 50): "))
        cols = int(input("Grid columns (e.g. 50): "))
    except ValueError:
        print("Invalid input, using default 50×50.")
        rows = cols = 50

    # Initialize grid: random live cells with given probability
    try:
        p = float(input("Initial live-cell probability (0.0–1.0, e.g. 0.2): "))
        if not (0.0 <= p <= 1.0):
            raise ValueError
    except ValueError:
        print("Invalid probability, using p = 0.2.")
        p = 0.2

    grid = np.random.choice([0, 1], size=(rows, cols), p=[1-p, p])

    # Set up the figure and animation
    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest', cmap='Greys')
    ax.set_title("Conway's Game of Life")
    ax.set_xticks([])
    ax.set_yticks([])

    try:
        interval = int(input("Update interval in ms (e.g. 200): "))
    except ValueError:
        print("Invalid interval, using 200ms.")
        interval = 200

    ani = animation.FuncAnimation(
        fig, update, fargs=(img, grid, rows, cols),
        frames=1000,
        interval=interval,
        save_count=50,
        blit=True
    )

    plt.show()

if __name__ == "__main__":
    main()
