from pymatgen.apps.borg.hive import AbstractDrone
from pathlib import Path
import glob
import os
from pymatgen.util.provenance import StructureNL
from pymatgen import Structure, Composition
import json
from datetime import datetime
from doi2bib.crossref import get_bib_from_doi
from emmet.borg.icsd_to_mongo import icsdDrone as EmmetIcsdDrone
from pymongo import MongoClient


class IcsdDrone2019(AbstractDrone):

    def does_match_composition(self, formula1, formula2):
        c1 = Composition(formula1)
        c2 = Composition(formula2)

        return(c1.almost_equals(c2))

    def assimilate(self, path, dbhost='localhost', dbport = 27017, dbname='ICSD', collection_name='ICSD_files', store_mongo=True):
        '''
        path: directory that stores cif file and metadata file
        '''
        if store_mongo:
            client = MongoClient(dbhost,dbport)
            db = client[dbname]
            col = db[collection_name]

        classic_drone = EmmetIcsdDrone()   # Modify this!!!! -> StrucrtureNL -> Structure
        data = classic_drone.assimilate(
            path, store_mongo=False
        )

        file_ID = path.split('/')[-1]
        jsonpath = "{0}/{1}.json".format(path, file_ID)

        # Verify paths!!
        # If possible

        # SNL's bibtex things:

        with open(jsonpath) as f:

            # data["snl"]["about"]["authors"] += [{
            #     "name": "Koki Muraoka",
            #     "email": "kmuraoka@lbl.gov"
            # }]

            cifmetatadata

            metadata d


            is_valid <- False

            # db == medatada.id

            icsd_web_metadata = json.load(f)

            # Possible implicit Hydrogen
            icsd_web_metadata["_does_match_composition"] = self._does_match_composition(
                data['formula_reduced'], icsd_web_metadata['chemical_formula'])
            data["icsd_web_metadata"] = icsd_web_metadata

        return(data)

    def get_valid_paths(self, path):
        '''
        Even if there is no corresponding metadata,
        parsing goes on.
        '''
        classic_drone = EmmetIcsdDrone()
        return(classic_drone.get_valid_paths(path))


def main():
    pass


if __name__ == '__main__':
    main()
