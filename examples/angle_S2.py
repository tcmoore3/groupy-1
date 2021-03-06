import numpy as np

from groupy.order import *
from groupy.general import *
from groupy.mdio import *
from groupy.gbb import *


# --- user input ---
coverage = 0.2
file_name = 'example_inputs/peg6_' + str(coverage) + '.lammpstrj'

peg = Gbb()
peg.load_xyz('example_inputs/peg6.xyz')
peg.load_mass('example_inputs/peg6_mass.txt')

# --- system info ---
# atom indices of regions
substrate_ids = range(3200)
chain_ids = range(3200, 4360)

system_info = {'substrate': substrate_ids,
               'chains': chain_ids}

# --- main ---
all_S2 = list()
all_angles = list()

with open(file_name, 'r') as trj:
    while True:
        # read a frame
        try:
            xyz, types, step, box = read_frame_lammpstrj(trj)
        except:
            print "Reached end of '" + file_name + "'"
            break

        # filter out terminal hydrogen atoms
        notsub = xyz[system_info['chains']]
        notsub_types = types[system_info['chains']]
        all_chains = notsub[np.where(notsub_types != 11)]

        # split the coordinates into individual chains
        individual_chain_coords = np.split(all_chains,
                range(peg.n_atoms, len(all_chains), peg.n_atoms))

        # operate on each chain
        directors = np.empty(shape=(len(individual_chain_coords), 3))
        for i, xyz in enumerate(individual_chain_coords):
            temp_peg = copy.copy(peg)
            temp_peg.xyz = xyz
            temp_peg.unwrap(box)

            I = temp_peg.calc_inertia_tensor()
            director = calc_director(I)
            directors[i] = director
            angle = calc_angle(director, [0, 0, 1])
            if (angle >= 90) and (angle <= 180):
                angle -= 90
            all_angles.append(angle)

        Q = calc_Q_tensor(directors)
        S2 = calc_S2(Q)
        all_S2.append(S2)

print 'Average tilt angle:'
print u'%5.3f \u00B1 %5.3f' % (np.mean(all_angles), np.std(all_angles))
print 'Average nematic order parameter:'
print u'%5.3f \u00B1 %5.3f' % (np.mean(all_S2), np.std(all_S2))
