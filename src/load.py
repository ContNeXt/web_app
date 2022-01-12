# -*- coding: utf-8 -*-
""" RUN ONCE TO CREATE THE DATABASE """

from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import inspect
from .models import Base, engine, Node, Network
from .constants import CONTEXT

import networkx as nx
from typing import List, Tuple
from tqdm import tqdm
import os
import csv

def list_files(dir:str) -> List:
    """ List all the files in a directory and it's sub-directories """
    # create a list of file and sub directories
    list_of_files = os.listdir(dir)
    all_files = list()
    # Iterate over all the entries
    for entry in list_of_files:
        # Create full path
        full_path = os.path.join(dir, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(full_path):
            all_files = all_files + list_files(full_path)
        else:
            all_files.append(full_path)
    return all_files


def check_tsv(all_files: List) -> Tuple[List, List, List, str]:
    """ Filters out all non-tsv files from the dictionary"""
    supplementary = []
    all_tsv_files = []
    properties = []
    interactome = None
    for file in all_files[:]:
        # Check the extension
        if file.endswith("coexp_network_edges.tsv"):
            all_tsv_files.append(file)
        elif file.endswith("overview.tsv") and \
            not file.endswith("FULL_cellline_overview.tsv")and \
            not file.endswith("FULL_celltype_overview.tsv")and \
            not file.endswith("FULL_tissue_overview.tsv"):
            # TODO make this cleaner
            # add to supplementary list
            supplementary.append(file)
        elif file.endswith("node_properties.tsv"):
            properties.append(file)
        elif file.endswith('interactome_edges.tsv'):
            print("Interactome: ",file)
            interactome = file
    return all_tsv_files, supplementary, properties, interactome


def create_node_set(list_tsv):
    """ Create a set of all the nodes """
    # init set of nodes
    list_of_nodes = set()
    # get a set of nodes
    for value in tqdm(list_tsv.values()):
        for node in value.nodes:
            list_of_nodes.add(node)
    return list_of_nodes


def add_edgelist(file_path, interacFlag=False):
    """ Create networkx edgelist from file"""
    # Open the file as an nx object
    if interacFlag:
        return nx.read_edgelist(file_path, delimiter='\t', encoding='utf-8', create_using=nx.DiGraph())

    network = nx.read_edgelist(file_path, comments='from', delimiter='\t', data=(
        ("direction", str),
        ("method", str),
        ("weight", float),), encoding='utf-8', create_using=nx.Graph())
    return network


def add_metadata_to_networks(supplementary_files: List):
    """ Add metadata to networks from list of supplementary tsv files, """
    network_metadata = {}
    for file in supplementary_files:
        with open(file, 'r') as f:
            csv_reader = csv.reader(f, delimiter='\t')
            header = next(csv_reader) # skip header
            for row in csv_reader:
                network_metadata.update({row[0].split(":")[1]: {'context': CONTEXT[os.path.basename(file).split("_")[0]] ,
                                                                'id': row[0],
                                                                'name': row[1]}})
    return network_metadata


def add_properties_to_nodes(property_files: List):
    """ Add properties to nodes from list of properties tsv files, """
    node_properties = {}
    for file in property_files:
        with open(file, 'r') as f:
            csv_reader = csv.reader(f, delimiter='\t')
            header = next(csv_reader) # skip header
            # In interactome, add extra column
            if os.path.basename(file) == 'interactome_node_properties.tsv':
                node_properties.update({os.path.basename(os.path.dirname(file)):{row[0]: {'connections': row[4],
                                                                         'rank': row[5],
                                                                         'housekeeping': row[6],
                                                                         'controllability': row[1]} for row in csv_reader}})
            else:
                node_properties.update({os.path.basename(os.path.dirname(file)):{row[0]: {'connections': row[1],
                                                                         'rank': row[2],
                                                                         'housekeeping': row[3]} for row in csv_reader}})

    return node_properties

'''
    Load database
'''

def load_database(data_source):
    """ Load the SQL-Alchemy Database with files from given directory """
    # Start database session
    Session = sessionmaker(bind=engine)
    session = Session()

    # Check if database exists
    if not database_exists(engine.url):
        # Create db
        create_database(engine.url)

    # Find all files
    all_files = list_files(data_source)
    # filter out all non-tsv, and get supplementary dict
    list_tsv, supplementary_source, properties_files, interactome = check_tsv(all_files=all_files)

    # counter
    debugger = int(0)
    # init list of nodes
    list_of_nodes = []

    metadata = add_metadata_to_networks(supplementary_files=supplementary_source)
    node_properties = add_properties_to_nodes(property_files=properties_files)

    # add interactome to db
    interactome = Network(identifier='interactome',
                          data=add_edgelist(interactome, interacFlag=True),
                          context='interactome',
                          name='interactome',
                          properties=node_properties.get('interactome'))
    # push to database
    session.add(interactome)
    session.commit()

    # add data from each file to database
    for file in tqdm(list_tsv, total=len(list_tsv)):
        key = os.path.basename(os.path.dirname(file))
        new_network = Network(identifier=metadata.get(key).get('id'),
                              data=add_edgelist(file),
                              context=metadata.get(key).get('context'),
                              name=metadata.get(key).get('name'),
                              properties=node_properties.get(key))

        for node in add_edgelist(file).nodes:
            # check if node is already in the database
            q = session.query(Node).filter(Node.name == node).first()
            if q:
                new_node = q
            else:
                new_node = Node(name=node)
                list_of_nodes.append({'node': node})
            # add relationship between nodes
            new_network.nodes_.append(new_node)
            session.add(new_node)

        debugger = debugger+1

        # push to database
        session.add(new_network)
        session.commit()


    return debugger


'''
    Check database 
'''

def is_ready():
    """Checks whether there's a valid database to load from"""
    # Check if database exists
    if not database_exists(engine.url):
        # Create db
        create_database(engine.url)
    # Check if database is empty
    if not inspect(engine).get_table_names():
        return False
    return True
