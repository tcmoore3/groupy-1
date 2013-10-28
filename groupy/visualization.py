import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pdb

# type: (color, vdw radius)
a_info = {'C': ('teal', 1.7),
          'H': ('white', 1.2),
          'O': ('red', 1.52),
          'N': ('blue', 1.55),
          'P': ('orange', 1.8)}


def splat(xyz, direction, types=None):
    """
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for i, atom in enumerate(xyz):
        if types:
            ax.scatter(atom[0], atom[1], atom[2],
                c=a_info[types[i]][0],
                marker='o',
                s=100 * a_info[types[i]][1] ** 3)
        else:
            ax.scatter(atom[0], atom[1], atom[2],
                marker='o',
                s=10)

    bounds = [xyz.min(), xyz.max()]
    ax.set_xlim(bounds)
    ax.set_ylim(bounds)
    ax.set_zlim(bounds)

    # TODO: robust way to choose origin
    ax.plot([0, 10*direction[0]], [1, 10*direction[1]], [2, 10*direction[2]], 
            c='k', linewidth=5)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()
