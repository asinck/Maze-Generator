#!/usr/bin/env python
#Adam Sinck

#this is a list of import commands. If the user doesn't have Tkinter
#or other libraries installed, it will fail gracefully instead of
#crashing.
imports = [
    "from Tkinter import *",
    "import Tkinter as tk"
]
#failedPackages will keep a record of the names of the packages that
#failed to import, so that the program can go through the entire list
#of packages that it wants to import. This will allow the program to
#give the user a complete list of packages that they need to install,
#instead of only telling the user one at a time.
failedPackages = ''
for i in imports:
    try:
        exec(i)
    except ImportError as error:
        failedPackages += str(error) + '\n'
#if there were any errors in the imports, tell the user what packages
#didn't import, and exit.
if len(failedPackages) > 0:
    print "Some packages could not be imported:"
    print failedPackages
    exit()


easel_width = 500
easel_height = 500
easel_background = "#000"
easel_foreground = "#FFF"
window_border = 2
cell_size = 3

def configure(event):
    global easel_width, easel_height
    easel_width, easel_height = event.width, event.height
    print "Adjusted to new width and height %dx%d" %(easel_width, easel_height)

#this is for blanking it
def resetEasel():
    global easel, easel_width, easel_height, window_border, \
        easel_background
    if (easel != None):
        easel.pack_forget()
    easel = Canvas(mainFrame, width = easel_width-window_border, \
                   height = easel_height-window_border, \
                   bg = easel_background)
    easel.pack(fill=BOTH, expand=YES)
    easel.bind("<Configure>", configure)


#this generates a maze
def generate_maze(var=None):
    resetEasel()
    import random, time
    global cell_width

    """
    the plan here:

    start at 5, 5, the center of the first cell (pixelwise)

    check the center of each adjacent cell, located cell_width away

    if it's white, it's visited; ignore

    if it's black, make a path and add it to the list of cells to visit

    go until there are no to-visit cells

    """

    def get_neighbors((x, y), visited):
        neighbors = []
        if (x > 5 and (x-10, y) not in visited):
            # cells.append( ((x, y), (x-10, y)) )
            # visited.append( (x-10, y) )
            neighbors.append( ((x, y), (x-10, y)) )

        if (y > 5 and (x, y-10) not in visited):
            # cells.append( ((x, y), (x, y-10)) )
            # visited.append( (x, y-10) )
            neighbors.append( ((x, y), (x, y-10)) )

        if (x < easel_width and (x+10, y) not in visited):
            # cells.append( ((x, y), (x+10, y)) )
            # visited.append( (x+10, y))
            neighbors.append( ((x, y), (x+10, y)) )

        if (y < easel_height and (x, y+10) not in visited):
            # cells.append( ((x, y), (x, y+10)) )
            # visited.append( (x, y+10) )
            neighbors.append( ((x, y), (x, y+10)) )
        return neighbors
        
    
    coordinates = (1, 1) #pixels

    visited = []
    cells = [((0, 0), coordinates)]
    cell = None

    chance = 3
    while len(cells) > 0:
        # #mix a depth first traversal and a random traversal. This
        # #gives a mix between long hallways and all branches
        if (random.randint(0, chance) < chance):
            cell = cells.pop()
        else:
            cell = random.choice(cells)
            cells.remove(cell)

        # cell = cells.pop()
        print cell
        (px, py), (nx, ny) = cell
        if ((nx, ny) not in visited):
            easel.create_line(px, py, nx, ny, width=cell_size, fill=easel_foreground)
            visited.append((nx, ny))
        
            #add neighbors
            neighbors = get_neighbors((nx, ny), visited)
            if (neighbors):
                random.shuffle(neighbors)
            cells += neighbors
            time.sleep(.01)
            root.update_idletasks()
    
        # visited += [i[1] for i in neighbors]
        

        # if (neighbors):
        #     cell = r.choice(neighbors)
        #     cells.remove(cell)
        #     print cell
        #     (px, py), (nx, ny) = cell
        #     easel.create_line(px, py, nx, ny, width=cell_size)

        #     neighbors = get_neighbors((nx, ny), visited)
        #     cells += neighbors
        #     visited += [i[1] for i in neighbors]

        
        



root = Tk()
root.title("Maze Generator")

mainFrame = Frame(root)

easel = None
easel = Canvas(mainFrame, width = easel_width, height = easel_height, \
               bg = easel_background)

easel.bind("<Configure>", configure)

mainFrame.pack(fill=BOTH, expand=YES)
easel.pack(fill=BOTH, expand=YES)

root.after(0, generate_maze)

root.bind("<Button-1>", generate_maze)

root.mainloop()


