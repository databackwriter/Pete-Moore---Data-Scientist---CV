#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 23 11:45:40 2018

@author: petermoore
"""

# program config
from constants import getCVMetaDatafromYAML, PATH_XL, PATH_CVYAML, DICT_CVTYPE, DICT_COMPONENTDEFAULT, session, args

# bespoke set up for CV writing
from datalib import sqlAppendCVType, sqlBuildComponentDefault,  sqlAppendCandidate, sqlAppendEdit, sqlAppendXLRow

# cv config
formattedname, timestamp = getCVMetaDatafromYAML(yamlfile=PATH_CVYAML)

def buildEdit(cvtypeid):

    d = {
         "formattedname": formattedname,
         "yamlfile": PATH_CVYAML,
         "editname": timestamp,
         "cvtypeid": cvtypeid}


    #build CV types
    newcvtype = sqlAppendCVType(session, DICT_CVTYPE, cvtypeid)

    #build components
    sqlBuildComponentDefault(session, DICT_COMPONENTDEFAULT)

    #add candidate (NB candidate uniquely idenfified by YAML path so bot always adding as new)
    newcandidate = sqlAppendCandidate(session, d)

    #add edit (NB edit uniquely indentified by fields including timestamp, so typically have a new one of these each time,
    #possibly this is something to remove in future, allowing an Edit to be defined by its flags)
    newedit = sqlAppendEdit(session, d, newcandidate, newcvtype)

    # turn the static CV intoa duynmaic one
    sqlAppendXLRow(session, newedit, newcandidate, PATH_XL)

    #close sql alchemy session
    session.close()

    # output editid (mostly for use when called from CLI)
    print(newedit.editid)

    # return editid
    return newedit.editid

if __name__ == "__main__":

    # get cvtype from args if available
    if args.cvtypeid:
        cvtypeid=args.cvtypeid
    # NB do this is in all cases
    if not cvtypeid in DICT_CVTYPE.keys():
        cvtypeid = 1 #CONVENTION if no cvtypeid provided then default to a Data Science CV

    # now go and build this edit of the CV!
    buildEdit(cvtypeid=cvtypeid)





