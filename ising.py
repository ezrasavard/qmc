import copy
import numpy as np

class SpinGlass(object):
    """An Ising Spin Glass Configuration"""
    
    def __init__(self,
                 data_file="sample_data/ising32.txt",
                 spin_configuration=None):
        """Process a data file and optionally a starting spin configuration
        
        data_file has K+1 columns and some string in the first line
        - The first K columns are positive integer spin IDs
        - The last column is the coupling between the spins
        - Solver is at present designed to work with K = 2 only
        
        spin_configuration is a value in hex that represents the spins using
        binary 1 (spin up) and 0 (spin down), packed into hex for shorthand
        readability
        """
        
        # store argument values
        self.data_file = data_file
        self.spin_configuration = spin_configuration
        
        self.couplings, self.adj, self.description = self.process_data()
        
        if spin_configuration:
            self.spins_initial = self.hex_to_spins(spin_configuration)
        else:
            self.spins_initial = self.randomize()
            
        # create a working copy
        self.spins = copy.copy(self.spins_initial)
        
        # calculate energies
        self.E_initial = self.calculate_E()
        self.E = self.E_initial
    
    
    def process_data(self):
        """Read data_file into usable data structures
        
        Create matrix of couplings between spins
        Create adjacency list for spins and neighbours
        """
        data = np.loadtxt(self.data_file, skiprows=1)
        with open(self.data_file) as f:
            descrip = f.readline().strip()

        couplings = None
        adj_list = None
        
        return couplings, adj_list, descrip
        
        
    def calculate_E(self):
        
        return None
    
    def hex_to_spins(self, hex_spins):
        pass
    
    def spins_to_hex(self, spins):
        pass
    
    def randomize(self):
        pass
    
    def __repr__(self):
        
        return '{}(data_file={}, spin_configuration={})'.format(self.__class__,
            self.data_file, self.spin_configuration)
        
    def __str__(self):
        
        ret = "Ising Spin Glass"
        ret += "\nData file: {}".format(self.data_file)
        ret += "\nProblem description: {}".format(self.description)
        ret += "\nInitial configuration: {}".format(
            self.spins_to_hex(self.spins_initial))
        ret += "\nCurrent configuration: {}".format(
            self.spins_to_hex(self.spins))
        ret += "\nInitial energy: {}".format(self.E_initial)
        ret += "\nCurrent energy: {}".format(self.E)

        return ret

if __name__ == "__main__":
    test = SpinGlass()
    print test