from nose.tools import assert_equals, assert_raises

import ising

class TestIsing:
 
    def setup(self):
        self.problem = ising.SpinGlass()
 
    def teardown(self):
        pass

    
    def test_hex_to_spins(self):
        assert_equals(self.problem.hex_to_spins("0x4", 3), (1,-1,-1))
        assert_equals(self.problem.hex_to_spins("4", 3), (1,-1,-1))
        assert_equals(self.problem.hex_to_spins("4", 4), (1,-1,-1,-1))
        assert_raises(AssertionError, self.problem.hex_to_spins, "0x4", 2)
        assert_raises(AssertionError, self.problem.hex_to_spins, "-4", 3)
        assert_equals(self.problem.hex_to_spins("FFFF FFFF", 32),
            (1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1))
            
    def test_spins_to_hex(self):
        assert_equals(self.problem.spins_to_hex([1,-1,-1]), "0x4")
        assert_equals(self.problem.spins_to_hex([1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1]), "0xffffffff")
        assert_equals(self.problem.spins_to_hex([1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1,
            -1, -1, -1, -1, -1, -1, -1, -1,
            1, 1, 1, 1, 1, 1, 1, 1]), "0x7fff00ff")
        assert_equals(self.problem.spins_to_hex([-1, -1, -1]), "0x0")
        assert_equals(self.problem.spins_to_hex([1, 1, 1, -1, -1]), "0x1c")
        assert_equals(self.problem.spins_to_hex([1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1,
            -1, -1, -1, -1, -1, -1, -1, -1,
            1, 1, 1, 1, 1, 1, 1, 1]), "0x7fffffffffffffffffff00ff")
