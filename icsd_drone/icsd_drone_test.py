import unittest
from icsd_drone.icsd_drone import IcsdDrone
import os
import json
from monty.serialization import dumpfn


class TestIcsdDrone(unittest.TestCase):
    def setUp(self):
        os.system('rm -rf test_files/out; mkdir -p test_files/out')
        self.drone = IcsdDrone()
        self.test_dir = os.path.join(os.path.dirname(__file__), '..', 'test_files')

    def test_valid_paths(self):
        for path in os.walk(self.test_dir):
            if path[0] == self.test_dir:
                self.assertTrue(len(self.drone.get_valid_paths(path)) > 0)

    def test_does_match_composition(self):
        self.assertTrue(self.drone.does_match_composition("SiO2", "SiO2"))
        self.assertFalse(self.drone.does_match_composition("Na0.2Al0.2SiO2", "Na0.4Al0.4Si2O4"))
        self.assertFalse(self.drone.does_match_composition("Na0.21Al0.2SiO2", "Na0.4Al0.4Si2O4"))
        self.assertFalse(self.drone.does_match_composition("HNa0.2Al0.2SiO2", "Na0.4Al0.4Si2O4"))

    def test_assimilate(self):
        self.drone.assimilate("test_files/CHA.cif")
        entry = self.drone.assimilate("test_files/CHA.json")

        # with open(, "w") as f:
            # json.dump(entry, f)
            # mo
        dumpfn(entry, "test_files/out/test.json")



    def test_to_from_dict(self):
        d = self.drone.as_dict()
        drone = IcsdDrone.from_dict(d)
        self.assertEqual(type(drone), IcsdDrone)
