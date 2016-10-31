import bitarray
import numpy as np
import prettytable

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

        # process an input hex string configuration, or randomize
        if spin_configuration:
            self.spins_initial = self.hex_to_spins(spin_configuration)
        else:
            self.randomize()
        
        # create working copies
        # these values are intended to be accessed and modified by a solver
        self.spins = self.spins_initial.copy()
        
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
        for i, j, J in data[data[:,0].argsort()]:
            i = spin_map[int(i)]
            j = spin_map[int(j)]
            # print "i: {}, j: {}, J: {}".format(i, j, J)
            if i >= j:
                self.J[i,j] = J
            else:
                self.J[j,i] = J
        
        if np.max(np.absolute(self.J)) > 1:
            self.scaling_factor = 1e5
        self.J /= self.scaling_factor
        self.h = np.diag(self.J).copy()
        np.fill_diagonal(self.J, 0)
        # ensure J is formed properly
        assert(self.J.any() == True)
        assert(np.triu(self.J).any() == False)
        assert(np.tril(self.J).any() == True)
        
        self.J = np.tril(self.J)
        assert(np.triu(self.J).any() == False)
        self.J += np.tril(self.J).T
        
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
        for i in xrange(self.size):
            Ei = self.h[i]
            Ei += 0.5*sum((1 if self.spins[j] else -1)*self.J[i,j] for j in self.adjacency[i])
            if not self.spins[i]:
                Ei *= -1
            E += Ei
            
        return E
    
    
    def calculate_dE(self, i):
        """Calculate the difference in energy from flipping a single spin i"""
        
        dE = self.h[i]
        dE += sum((1 if self.spins[j] else -1)*self.J[i,j] for j in self.adjacency[i])
        if not self.spins[i]:
            dE *= -1

        return -2*dE
    
    
    def hex_to_spins(self, hex_spins):
        """Convert a hex string to a big endian binary array
        
        This function takes user input, so we'll be careful
        
        hex_spins: hex representation of spin configuration
        - allows, but doesn't require, a leading "0x"
        """
        
        # purely alphanumeric strings only
        assert(hex_spins.isalnum())
        
        binary = '{:0{}b}'.format(int(hex_spins,16), self.size)
        spins = bitarray.bitarray(binary)

        return spins
        

    def spins_to_hex(self, spins=None):
        """Return a hex string representation of the spin configuration bitarray"""
        
        if spins:
            spins = bitarray.bitarray(spins)
        else:
            spins = self.spins
        hex_spins = "0x{:x}".format(int(spins.to01(),2))
        
        return hex_spins
    
    
    def randomize(self):
        """Set self.spins_initial to a random configuration"""
        
        spins = [np.random.random() > 0.5 for x in range(self.size)]
        self.spins_initial = bitarray.bitarray(spins)
    
    def get_spin(self, i):
        """Return spin as +/- 1"""
        
        return 1 if self.spins[i] else -1
    
    
    def flip_spin(self, i):
        """Flip a spin between up and down states"""
        
        self.spins[i] ^= True
    
    
    def __repr__(self):
        
        return '{}(data_file="{}", spin_configuration="{}")'.format(self.__class__, self.data_file, self.spins_to_hex(self.spins))
        
        
    def __str__(self):
        
        ret = "\nIsing Spin Glass\n"
        x = prettytable.PrettyTable(["Field", "Value"])
        x.align["Field"] = "l"
        x.align["Value"] = "l"
        x.add_row(["data file", self.data_file])
        x.add_row(["description", self.description])
        x.add_row(["initial config", self.spins_to_hex(self.spins_initial)])
        x.add_row(["current config", self.spins_to_hex(self.spins)])
        x.add_row(["initial energy", self.E_initial*self.scaling_factor])
        x.add_row(["current energy", self.E*self.scaling_factor])
        
        return ret + x.get_string()


if __name__ == "__main__":
    test = SpinGlass()
    print test