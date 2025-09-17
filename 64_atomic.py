# Dictionary of atomic weights for common elements
atomic_weights = {
    'H': 1.008, 'He': 4.0026, 'Li': 6.941, 'Be': 9.0122, 'B': 10.811, 'C': 12.011,
    'N': 14.007, 'O': 15.999, 'F': 18.9984032, 'Ne': 20.1797, 'Na': 22.99, 'Mg': 24.305,
    'Al': 26.9815386, 'Si': 28.0855, 'P': 30.973762, 'S': 32.065, 'Cl': 35.453, 'Ar': 39.948,
    'K': 39.0983, 'Ca': 40.078, 'Sc': 44.955912, 'Ti': 47.867, 'V': 50.9415, 'Cr': 51.9961,
    'Mn': 54.938045, 'Fe': 55.845, 'Co': 58.933195, 'Ni': 58.6934, 'Cu': 63.546, 'Zn': 65.38,
    'Ga': 69.723, 'Ge': 72.64, 'As': 74.9216, 'Se': 78.96, 'Br': 79.904, 'Kr': 83.798,
    'Rb': 85.4678, 'Sr': 87.62, 'Y': 88.90585, 'Zr': 91.224, 'Nb': 92.90638, 'Mo': 95.96,
    'Tc': 98, 'Ru': 101.07, 'Rh': 102.9055, 'Pd': 106.42, 'Ag': 107.8682, 'Cd': 112.411,
    'In': 114.818, 'Sn': 118.71, 'Sb': 121.76, 'Te': 127.6, 'I': 126.90447, 'Xe': 131.293,
    'Cs': 132.9054519, 'Ba': 137.327, 'La': 138.90547, 'Ce': 140.116, 'Pr': 140.90765,
    'Nd': 144.242, 'Pm': 145, 'Sm': 150.36, 'Eu': 151.964, 'Gd': 157.25, 'Tb': 158.92535,
    'Dy': 162.5, 'Ho': 164.93032, 'Er': 167.259, 'Tm': 168.93421, 'Yb': 173.054, 'Lu': 174.967,
    'Hf': 178.49, 'Ta': 180.94788, 'W': 183.84, 'Re': 186.207, 'Os': 190.23, 'Ir': 192.217,
    'Pt': 195.084, 'Au': 196.966569, 'Hg': 200.59, 'Tl': 204.3833, 'Pb': 207.2, 'Bi': 208.9804,
    'Po': 209, 'At': 210, 'Rn': 222, 'Fr': 223, 'Ra': 226, 'Ac': 227, 'Th': 232.03806,
    'Pa': 231.03588, 'U': 238.02891, 'Np': 237, 'Pu': 244, 'Am': 243, 'Cm': 247, 'Bk': 247,
    'Cf': 251, 'Es': 252, 'Fm': 257, 'Md': 258, 'No': 259, 'Lr': 262, 'Rf': 267, 'Db': 268,
    'Sg': 271, 'Bh': 272, 'Hs': 270, 'Mt': 276, 'Ds': 281, 'Rg': 281, 'Cn': 285, 'Nh': 286,
    'Fl': 289, 'Mc': 290, 'Lv': 293, 'Ts': 294, 'Og': 294
}

def calculate_molecular_weight(formula):
    # Initialize the total weight
    total_weight = 0.0
    
    # Initialize a pointer to keep track of the current position in the formula
    i = 0
    
    while i < len(formula):
        # Find the element symbol
        element = formula[i]
        if element not in atomic_weights:
            raise ValueError(f"Unknown element: {element}")
        
        # Find the number of atoms of this element
        j = i + 1
        while j < len(formula) and formula[j].isdigit():
            j += 1
        
        # If no number is provided, default to 1
        num_atoms = int(formula[i+1:j] or 1)
        
        # Add the weight of this element to the total weight
        total_weight += atomic_weights[element] * num_atoms
        
        # Move the pointer to the next element
        i = j
    
    return total_weight

# Example usage
formula = "H2O"
molecular_weight = calculate_molecular_weight(formula)
print(f"The molecular weight of {formula} is {molecular_weight:.3f} g/mol")
