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

        classic_drone = EmmetIcsdDrone()
        classic_data = classic_drone.assimilate(
            store_mongo=False
        )

        file_ID = path.split('/')[-1]
        jsonpath = "{0}/{1}.json".format(path, file_ID)

        with open(jsonpath) as f:
            self.metadata = json.load(f)


            data = {
                "_does_match_composition": self.does_match_composition(
                    self.strct.composition.formula, self.metadata['chemical_formula']),
                "_is_theoretical": self.metadata['theoretical_calculation'],
                "_doi": self.metadata['doi'],
            }

            important_entries = [
                "doi", "abstract", "temperature", "collection_code",
            ]

            data['_icsd_metadata'] = self.metadata

            found_bib, bibtex = get_bib_from_doi(self.metadata['doi'])
            if not found_bib:
                bibtex = ""

        # return()

        if 'snl' in data:
            if store_mongo:
                col.update_one({'icsd_id': int(file_ID)},{'$set': data},upsert=True)

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
