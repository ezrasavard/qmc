from nose.tools import assert_equals, assert_raises
import numpy as np

import ising

class TestIsing:
    
    def setup(self):
        self.p = ising.SpinGlass("sample_data/evil.txt")

    def teardown(self):
        pass
    
    def test_delta_calcs(self):
        """Flip random spins 10000 times or until an error appears"""
        for count in xrange(10000):
            i = np.random.randint(0, self.p.size)
            print self.p.size
            dE = self.p.calculate_dE(i)
            E0 = self.p.calculate_E()
            self.p.spins[i] ^= True
            diff = self.p.calculate_E() - E0
            print "count: {}".format(count)
            print "spin: {}".format(i)
            print "adj: {}".format(self.p.adjacency[i])
            print "J: {}".format([self.p.J[i,j] for j in self.p.adjacency[i]])
            print "J-sym: {}".format([self.p.J[j,i] for j in self.p.adjacency[i]])
            print "J-shape: {}".format(self.p.J.shape)
            # floating point can be weird
            assert_equals(abs(diff - dE) > 1e-6, False)
    
    def convert_equals(self, x):
        """Helper to compare hex inputs and outputs"""
        
        ret = self.p.spins_to_hex(self.p.hex_to_spins(x))
        x = int(x,16)
        ret = int(ret,16)
        assert_equals(x, ret)
    
    def test_conversions(self):
        """Convert back and forth between hex and spin representations"""
        
        self.convert_equals("0x4")
        self.convert_equals("4")
        self.convert_equals("0x7fff00ff")
        self.convert_equals("0x86dcfc84376fb61ad808a166fe5ae0ffbb10b34577980dfaaa74cef69e08ef8d780170c79a5bc4a77b19f8da7e5af55cf9bb295e1f3041d3df1ba5da6543a5325fe5d304bc5c3d2e40b4bc6da5fac1c0aaf0ede5650604dc7ab7ddc93aedafe10efc12fffd1f9839327160fbd0166fca77f4d15b5cd310000000000000000000")
        
        assert_raises(AssertionError, self.p.hex_to_spins, "-4")
        assert_raises(AssertionError, self.p.hex_to_spins, "FF FF")