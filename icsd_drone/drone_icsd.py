from pymatgen.apps.borg.hive import AbstractDrone
from pathlib import Path
import glob
import os
from pymatgen.util.provenance import StructureNL
from pymatgen import Structure, Composition
import json
from datetime import datetime


class DroneIcsd(AbstractDrone):

    def __init__(self):
        self.has_metadata = False
        self.has_cif = False

    def does_match_composition(self, formula1, formula2):
        c1 = Composition(formula1)
        c2 = Composition(formula2)

        return(c1.almost_equals(c2))

    def assimilate(self, path):
        if ".json" == Path(path).suffix:

            with open(path) as f:
                self.metadata = json.load(f)

            self.has_metadata = True

        elif ".cif" == Path(path).suffix:
            self.strct = Structure.from_file(filename=path)
            self.has_cif = True

        if self.has_metadata and self.has_cif:

            # Check whether composition from metadata and composition from
            # cif match.

            data = {
                "_does_match_composition": self.does_match_composition(
                    self.strct.composition.formula, self.metadata['chemical_formula']),
                "_is_theoretical": self.metadata['theoretical_calculation'],
                "_doi": self.metadata['doi']
            }
            # Compositional match
            # print(self.metadata['authors'])
            snl = StructureNL(
                struct_or_mol=self.strct,
                authors="Koki Muraoka <kmuraoka@lbl.gov>",
                projects="ICSD {}".format(self.metadata["ICSD_version"]),
                references="",
                data=data,
                # history=history,
                created_at=datetime.now()
                # authors=[author.strip() for author in self.metadata['authors'].split(";")]
            )

            return(snl)

        return()

    def get_valid_paths(self, path):
        (parent, subdirs, files) = path

        for pattern in ["*.json", "*.cif"]:
            if len(glob.glob(os.path.join(parent, pattern))) > 0:
                return([parent])
