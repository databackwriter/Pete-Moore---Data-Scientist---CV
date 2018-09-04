#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 30 05:44:45 2018

@author: petermoore

file to include constants and functions that typically are called once and only once (for example those that read from yaml)
"""
# constants
PATH_FILE="/Users/petermoore/Documents/GitHub/Pete Moore - Data Scientist - CV/Python"
PATH_XL = "/Users/petermoore/Documents/GitHub/Pete Moore - Data Scientist - CV/Excel/Initial data model.xlsx"
PATH_CVYAML="/Users/petermoore/Documents/GitHub/Pete Moore - Data Scientist - CV/CV.yaml"
PATH_CONNYAML = "/Users/petermoore/connections.yaml"

# session set up
import os
os.chdir(PATH_FILE)
import sys
sys.path.append(PATH_FILE) #add local directory to path

# cvtype setup
#NB this is fundamental and hard-coded, whulst not strictly hardcoded, it should be defined once and only once **per session**
DICT_CVTYPE={
             1:{"cvtype": "Data Scientist", "legacycvtype":"DSFlag"},
             2:{"cvtype": "IT Director", "legacycvtype":"CIOFlag"},
             3:{"cvtype": "SQL Server Expert", "legacycvtype":"SQLFlag"},
             4:{"cvtype": "Non-executive Director", "legacycvtype":"NEDFlag"}
             }

DICT_COMPONENTDEFAULT={
            1:{"componentdefault":"Main heading","headerlevel":2,"prefix":"","suffix":"","indent":""},
            2:{"componentdefault":"Section heading","headerlevel":3,"prefix":"","suffix":"","indent":""},
            3:{"componentdefault":"Highlighted info","headerlevel":0,"prefix":"_","suffix":"_","indent":""},
            4:{"componentdefault":"Paragraph","headerlevel":0,"prefix":"","suffix":"","indent":""},
            5:{"componentdefault":"Organisaton name","headerlevel":4,"prefix":"","suffix":"","indent":""},
            6:{"componentdefault":"Job title","headerlevel":5,"prefix":"","suffix":"","indent":""},
            7:{"componentdefault":"Quote","headerlevel":0,"prefix":"_","suffix":"_","indent":""},
            8:{"componentdefault":"Bullet","headerlevel":0,"prefix":"* ","suffix":"","indent":""},
            9:{"componentdefault":"Skills","headerlevel":0,"prefix":"Skills:","suffix":"","indent":""},
            10:{"componentdefault":"Big learns","headerlevel":0,"prefix":"Big learns:","suffix":"","indent":""},
            11:{"componentdefault":"Grade","headerlevel":0,"prefix":"","suffix":"","indent":""}
        }
# cli setup
arghelp= "Provide a cvtype id, use:"# build argument help from dictionary
for k, v in DICT_CVTYPE.items(): arghelp += "\r\n" + " %s for %s" % (str(k), v["cvtype"])
from argparse import ArgumentParser, RawTextHelpFormatter
parser = ArgumentParser(description='Select CV Type')
parser = ArgumentParser(description='Select CV Type', formatter_class=RawTextHelpFormatter)
parser.add_argument("--cvtypeid", help=arghelp, type=int, default=1)
args = parser.parse_args()

def getDSNfromYAML(yamlfile):
    import yaml
    with open(yamlfile, 'r') as f:
        doc = yaml.load(f)
        pdsn = doc["sqlconn"]["DSN"]
        puser = doc["sqlconn"]["user"]
        ppassword = doc["sqlconn"]["password"]
    dsn="DSN="+pdsn+";UID="+puser+";PWD="+ppassword
    alchemydsn = "mssql+pyodbc://"+puser+":"+ppassword+"@"+pdsn
    return dsn, alchemydsn, pdsn, puser, ppassword

def getCVMetaDatafromYAML(yamlfile):
    import yaml
    with open(yamlfile, 'r') as f:
        doc=yaml.load(f)
        formattedname=doc["PersonNameBaseType"]["FormattedName"]
        import datetime
        timestamp=datetime.datetime.now().isoformat()
    return formattedname, timestamp

# database set up
DSN, ALCHEMYDSN, pdsn, puser, ppassword = getDSNfromYAML(yamlfile=PATH_CONNYAML)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
engine = create_engine(ALCHEMYDSN)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine.execution_options(isolation_level='READ COMMITTED'))
session = DBSession()






