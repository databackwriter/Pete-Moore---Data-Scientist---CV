#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 20 10:25:36 2018

@author: petermoore
"""
def isNaNLocal(x):
    return x != x


def sqldf(sql,con):
    import pyodbc
    import pandas as pd
    conn = pyodbc.connect(con, autocommit=True)
    df = pd.read_sql(sql,conn)
    return df
#this append is different to others because it uses PYODBC and not sqlalchemy
def sqlPYODBCAppendEditxText(con, params):
    import pyodbc
    conn = pyodbc.connect(con, autocommit=True)
    crsr = conn.cursor()
    crsr.execute("{CALL dbo.usp_PM_EditxText_Add (?,?)}", params)
    crsr.close()
    conn.close()

def sqlPYODBCAppendComponentDefaultxComponent(con, params):
    import pyodbc
    conn = pyodbc.connect(con, autocommit=True)
    crsr = conn.cursor()
    crsr.execute("{CALL dbo.usp_PM_ComponentDefaultxComponent_Add (?)}", params)
    crsr.close()
    conn.close()

## adapted from the get_or_create function here: https://stackoverflow.com/questions/2546207/does-sqlalchemy-have-an-equivalent-of-djangos-get-or-create
#def sqlAppendIfNotExists(session, model, **kwargs):
#    instance = session.query(model).filter_by(**kwargs).first()
#    if instance:
#        return instance
#    else:
#        instance = model(**kwargs)
#        session.add(instance)
#        return instance

# append cv types (NB nature of the CV type means that we are adding differently here, we loop through and also do an identity insert)
def sqlAppendCVType(session, d, cvtypeid):

        from CVObjectClasses import CVType
        newcvtype = CVType()
        for k, v in d.items():
            nc=CVType()
            nc.cvtypeid=k
            nc.cvtype=v['cvtype']
            nc.legacycvtype=v['legacycvtype']
            latestcvtype = nc.addappend(session)
            if k == cvtypeid:
                newcvtype = latestcvtype
        return newcvtype


def sqlBuildComponentDefault(session, d):

        from CVObjectClasses import ComponentDefault
#        from constants import DICT_COMPONENTDEFAULT
#        d=DICT_COMPONENTDEFAULT
        newComponentDefault = ComponentDefault()
        for k, v in d.items():
            nc=ComponentDefault()
            nc.componentdefaultid=k
            nc.componentdefault=v['componentdefault']
            nc.headerlevel=v['headerlevel']
            nc.prefix=v['prefix']
            nc.suffix=v['suffix']
            nc.indent=v['indent']
            newComponentDefault = nc.addappend(session)
        return newComponentDefault

def sqlAppendComponent(session, d):
        #Component fields
        from CVObjectClasses import Component
        # component fields
        nc=Component()
        nc.component=d['Component']
        return nc.addappend(session)

def sqlAppendCandidate(session, d):
        #Candidate fields
        from CVObjectClasses import Candidate
        nc=Candidate()
        nc.formattedname=d['formattedname']
        nc.yamlfile=d['yamlfile']
        return nc.addappend(session)

def sqlAppendEdit(session, d, candidateout, cvtypeout):
        #Edit fields
        from CVObjectClasses import Edit
        ne=Edit()
        ne.editname=d['editname']
        ne.Candidate=candidateout
        ne.CVType=cvtypeout
        return ne.addappend(session)


def sqlAppendRoleType(session, d):
        #RoleType fields
        from CVObjectClasses import RoleType
        nr=RoleType()
        nr.roletype=d['RoleType']
        return nr.addappend(session)



def sqlAppendSection(session, d):
        #Section fields
        from CVObjectClasses import Section
        # Section fields
        ns=Section()
        ns.section=d['Section']
        return ns.addappend(session)

def sqlAppendOpportunity(session, d):
        #Opportunity fields
        from CVObjectClasses import Opportunity
        no=Opportunity()
        no.opportunityname=d['OpportunityName']
        no.company=d['Company']
        no.city=d['City']
        no.state=d['State']
        no.county=d['County']
        no.startmonth=d['StartMonth']
        no.startyear=d['StartYear']
        no.startdate=d['StartDate']
        no.endmonth=d['EndMonth']
        no.endyear=d['EndYear']
        no.enddate=d['EndDate']
        return no.addappend(session)

def sqlAppendCVText(session, d, newroletype, newcomponent, newsection, newopportunity):
        #CVText fields
        from CVObjectClasses import CVText
        ncv=CVText()
        ncv.textforshow=d['TextforShow']
        ncv.defaultorderind=d['DefaultOrderInd']
        ncv.parenttextfk=d['ParentTextFK']
        ncv.groupind=d['GroupInd']
        ncv.dsflag=d['DSFlag']
        ncv.cioflag=d['CIOFlag']
        ncv.sqlflag=d['SQLFlag']
        ncv.nedflag=d['NEDFlag']
        ncv.RoleType=newroletype
        ncv.Component=newcomponent
        ncv.Section=newsection
        ncv.Opportunity=newopportunity
        return ncv.addappend(session)

def sqlAppendXLRow(session, newedit, newcandidate,  xlpath):
    # cv raw data
    import pandas as pd
    from constants import DSN
    xldf=pd.read_excel(xlpath)
    for index, row in xldf.iterrows():
        d = row.to_dict() # this step is seemingly unnecessary, however, I want the "append" functions to behave with dictionaries so that they may be called  from elsewhere PM
        newroletype = sqlAppendRoleType(session, d)
        newcomponent = sqlAppendComponent(session, d)
        newsection = sqlAppendSection(session, d)
        newopportunity = sqlAppendOpportunity(session, d)
        ncvout = sqlAppendCVText(session, d,  newroletype, newcomponent, newsection, newopportunity)
        placeboreturn=newroletype.__tablename__ + "--" +newcomponent.__tablename__+ "--" +newsection.__tablename__+ "--" +newopportunity.__tablename__+ "--" +ncvout.__tablename__

        #give components their defaults in the first instance
        componentparams=[newcomponent.componentid]
        sqlPYODBCAppendComponentDefaultxComponent(DSN,componentparams)


    # cross reference editand text elements
    editparams=[newedit.editid, newcandidate.candidateid]
    sqlPYODBCAppendEditxText(DSN,editparams)

    return placeboreturn






