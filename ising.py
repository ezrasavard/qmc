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
        
        # initialize problem data
        self.J = None
        self.h = None
        self.adjacency = None
        self.description = None
        self.size = None
        self.spins_initial = None
        self.process_data_file()

        if spin_configuration:
            self.spins_initial = self.hex_to_spins(spin_configuration)
        else:
            self.randomize()

        # create a working copy
        self.spins = copy.copy(self.spins_initial)

        # calculate energies
        self.E_initial = self.calculate_E()
        self.E = self.E_initial
    
    
    def process_data_file(self):
        """Read data_file into usable data structures
        
        Create empty spin array
        Create structures for couplings between spins
        Create adjacency list for spins and neighbours
        """
        with open(self.data_file, 'r') as f:
            descrip = f.readline().strip()
        data = np.loadtxt(self.data_file, skiprows=1)
        
        # map spins to contiguous positive integer values
        max_spin = np.amax(data[:,(0,1)]).astype(int)
        unique_spins = np.unique(data[:,(0,1)]).astype(int)
        spin_map = np.zeros((max_spin + 1), dtype=int)
        for i, spin in enumerate(unique_spins):
            spin_map[spin] = i

        # build couplings matrix, spin array and adjacency list
        self.size = unique_spins.size
        self.spins_initial = np.zeros(self.size, dtype=int)
        self.J = np.zeros((self.size, self.size), dtype=float)
        # this is lower triangular with self-couplings on the diagonal
        for row in data:
            i = spin_map[row[0]]
            j = spin_map[row[1]]
            self.J[i,j] = row[2]
            
        self.h = np.diag(self.J)
        np.fill_diagonal(self.J,0)
        
        # about the adjacency list:
        # it is possible to just use h and J with the spins array
        # in order to do all the calculations using linear algebra,
        # but when these problems are sparse, an adjacency list works
        # much faster -- and in a spinglass, spins often have only two or
        # three neighbours
        self.adjacency = [[i, [j for j, x in enumerate(self.J[i]) if x != 0]] for i in xrange(self.size)]
        
        
    def calculate_E(self):
        
        return None
    
    
    def calculate_dE(self, i):
        pass
    
    @staticmethod
    def hex_to_spins(hex_spins, size):
        """Convert a hex string to a binary array with -1 in place of 0
        
        Consider the left end as the MSB
        This function takes user input, so we'll go crazy sanitizing it
        
        hex_spins: hex representation of spin configuration
        - allows, but doesn't require, a leading "0x"
        size: intended length of spin array
        - should be self.size when called from within the class
        """
        
        # remove whitespace
        hex_spins = "".join(hex_spins.split())
        
        # fail if symbols
        assert(hex_spins.isalnum() == True)

        # helper for doing the conversion
        s = lambda string: [1 if x=="1" else -1 for x in "{:b}".format(int(string, 16))]
        

        # handle overflow
        spins = []
        while len(hex_spins) > 4:
            spins += s(hex_spins[0:4])
            hex_spins = hex_spins[4:]
        spins += s(hex_spins)
        
        # installs trailing zeros, if any
        while len(spins) < size:
            spins.append(-1)
            
        # verify size wasn't too large
        assert(len(spins) == size)
        
        return spins
        
        
    @staticmethod
    def spins_to_hex(spins):
        
        spins = "".join([str(1) if x == 1 else str(0) for x in spins])
        
        return hex(int(spins,2))
    
    
    def randomize(self):
        """Set self.spins_initial to a random configuration"""
        
        self.spins_initial = [1 if np.random.random() > 0.5 else -1 for x in self.spins_initial]
    
    
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