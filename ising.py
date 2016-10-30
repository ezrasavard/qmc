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
        
        # declare problem data
        self.description = None
        self.size = None
        self.scaling_factor = 1
        
        # declare soon-to-be numpy arrays
        # these will be made non-writable
        self.J = None
        self.h = None
        self.adjacency = None
        self.spins_initial = None
        
        # populate problem data
        data = self._process_data_file()
        self._process_data(data)

        if spin_configuration:
            self.spins_initial = tuple(self.hex_to_spins(spin_configuration, self.size))
        else:
            self.randomize()
        
        # create working copies
        # these values are intended to be accessed and modified by a solver
        self.spins = [s for s in self.spins_initial]
        
        # calculate initial energy
        self.E_initial = self.calculate_E()
        self.E = self.E_initial
    
    
    def _process_data_file(self):
        """Read data_file, set description and return array"""
        
        with open(self.data_file, 'r') as f:
            self.description = f.readline().strip()
        data = np.loadtxt(self.data_file, skiprows=1)

        return data
        
        
    def _process_data(self, data):
        """data array into usable data structures
        
        Create empty spin array
        Create structures for couplings between spins
        Create adjacency list for spins and neighbours
        """
        # map spins to contiguous positive integer values
        max_spin = np.amax(data[:,:-1]).astype(int)
        unique_spins = np.unique(data[:,:-1]).astype(int)
        spin_map = np.zeros((max_spin + 1), dtype=int)
        for i, spin in enumerate(unique_spins):
            spin_map[spin] = i

        # build couplings matrix, spin array and adjacency list
        self.size = unique_spins.size
        self.J = np.zeros((self.size, self.size), dtype=float)
        # this is lower triangular with self-couplings on the diagonal
        for i, j, J in data:
            i = spin_map[int(i)]
            j = spin_map[int(j)]
            self.J[i,j] = J
        
        self.scaling_factor = np.max(np.absolute(self.J))
        self.J /= self.scaling_factor
        self.h = np.diag(self.J).copy()
        np.fill_diagonal(self.J,0)
        self.J += np.transpose(self.J)
        
        # about the adjacency list:
        # it is possible to just use h and J with the spins array
        # in order to do all the calculations using linear algebra,
        # but when these problems are sparse, an adjacency list works
        # much faster -- and in a spinglass, spins often have only two or
        # three neighbours
        self.adjacency = [[j for j, x in enumerate(self.J[i]) if x != 0] for i in xrange(self.size)]
        
        # lock arrays to prevent accidental mutations
        self.J.flags.writeable = False
        self.h.flags.writeable = False
        
        
    def calculate_E(self):
        """Calculates the energy of the classical spin configuration

        This isn't done often, so optimizing for speed isn't important
        """
    
        E = 0
        for i, spin in enumerate(self.spins):
            Ei = self.h[i]
            Ei += 0.5*sum(self.spins[j]*self.J[i,j] for j in self.adjacency[i])
            E += Ei*spin
            
        return E
    
    
    def calculate_dE(self, i):
        """Calculate the difference in energy from flipping a single spin i"""
        
        dE = self.h[i]
        dE += sum(self.spins[j]*self.J[i,j] for j in self.adjacency[i])
        dE *= self.spins[i]

        return -2*dE
    
    
    @staticmethod
    def hex_to_spins(hex_spins, size):
        """Convert a hex string to a binary tuple with -1 in place of 0
        
        Consider the left end as the MSB
        This function takes user input, so we'll be careful
        
        hex_spins: hex representation of spin configuration
        - allows, but doesn't require, a leading "0x"
        size: intended length of spin tuple
        - should be self.size when called from within the class
        """
        
        # sanitize input
        if len(hex_spins) > 1:
            hex_spins = hex_spins[2:] if hex_spins[1].lower() == "x" else hex_spins
        hex_spins.rstrip("L")
        hex_spins = "".join(hex_spins.split())
        assert(hex_spins.isalnum() == True)


        # helper for doing the conversion
        s = lambda string: [1 if x=="1" else -1 for x in "{:04b}".format(int(string, 16))]
        
        # handle overflow
        spins = []
        for char in hex_spins:
            spins += s(char)
        
        # removing leading "zeros" resulting from fixed width binary
        while len(spins) > size:
            spins = spins[1:]
            
        # installs trailing "zeros", if needed
        while len(spins) < size:
            spins.append(-1)
        
        # verify size wasn't too large
        assert(len(spins) == size)
        return spins
        
        
    @staticmethod
    def spins_to_hex(spins):
        """Return a hex string representation of the spin configuration array"""

        spins = "".join([str(1) if x == 1 else str(0) for x in spins])
        hex_string = ""
        while len(spins) > 4:
            hex_string = hex(int(spins[-4:],2))[2:] + hex_string
            spins = spins[:-4]
        hex_string = hex(int(spins,2)) + hex_string
        
        return hex_string
    
    
    def randomize(self):
        """Set self.spins_initial to a random configuration"""
        
        self.spins_initial = tuple(1 if np.random.random() > 0.5 else -1 for x in range(self.size))
        
    
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
        ret += "\nInitial energy: {}".format(self.E_initial*self.scaling_factor)
        ret += "\nCurrent energy: {}".format(self.E*self.scaling_factor)

        return ret


if __name__ == "__main__":
    test = SpinGlass()
    print test