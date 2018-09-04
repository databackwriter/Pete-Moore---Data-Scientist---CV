#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 23 15:18:09 2018

@author: petermoore
"""

#see pythoncentral.io for more information on sqlalchemy set up:
#https://www.pythoncentral.io/introductory-tutorial-python-sqlalchemy/



from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from constants import Base, engine
# append if not exists
# adapted from the get_or_create function here: https://stackoverflow.com/questions/2546207/does-sqlalchemy-have-an-equivalent-of-djangos-get-or-create


localecho=False
def sqlAppendIfNotExists(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        if localecho: print("This record already exists in the " + instance.__tablename__ + " table")
    else:
        instance = model(**kwargs)
        session.add(instance)
    session.commit()
    return instance

class CVType(Base):
    __tablename__ = 'CVType'
    cvtypeid = Column(Integer, primary_key=True)
    cvtype = Column(String(255), nullable=False)
    legacycvtype= Column(String(255), nullable=False)
    def addappend(self, session):
        return sqlAppendIfNotExists(session, CVType,
                                 cvtype=self.cvtype,
                                 legacycvtype=self.legacycvtype)

class Candidate(Base):
    __tablename__ = 'Candidate'
    candidateid = Column(Integer, primary_key=True)
    formattedname = Column(String(255), nullable=False)
    yamlfile = Column(String(255), nullable=False)
    def addappend(self, session):
        return sqlAppendIfNotExists(session, Candidate,
                                 formattedname=self.formattedname,
                                 yamlfile=self.yamlfile)


class Edit(Base):
    __tablename__ = 'Edit'
    editid = Column(Integer, primary_key=True)
    editname = Column(String(255), nullable=False)
    candidatefk = Column(Integer, ForeignKey('Candidate.candidateid'))
    cvtypefk = Column(Integer, ForeignKey('CVType.cvtypeid'))
    Candidate = relationship(Candidate)
    CVType = relationship(CVType)
    def addappend(self, session):
        return sqlAppendIfNotExists(session, Edit,
                                 editname = self.editname,
                                 Candidate = self.Candidate,
                                 CVType = self.CVType)



class RoleType(Base):
    __tablename__='RoleType'
    roletypeid= Column( Integer, primary_key=True, nullable=False )
    roletype= Column( String(50), nullable=False )
    def addappend(self, session):
        return sqlAppendIfNotExists(session, RoleType,
                                       roletype=self.roletype)


class ComponentDefault(Base):
    __tablename__='ComponentDefault'
    componentdefaultid= Column( Integer, primary_key=True, nullable=False )
    componentdefault= Column( String(50), nullable=False )
    headerlevel= Column( Integer, nullable=True )
    prefix= Column( String(50), nullable=True )
    suffix= Column( String(50), nullable=True )
    indent= Column( String(50), nullable=True )
    def addappend(self, session):
        return sqlAppendIfNotExists(session, ComponentDefault,
                                    componentdefault=self.componentdefault,
                                    headerlevel= self.headerlevel,
                                    prefix= self.prefix,
                                    suffix= self.suffix ,
                                    indent= self.indent)

class Component(Base):
    __tablename__='Component'
    componentid= Column( Integer, primary_key=True, nullable=False )
    component= Column( String(50), nullable=False )
    def addappend(self, session):
        return sqlAppendIfNotExists(session, Component,
                                    component=self.component)


class Section(Base):
    __tablename__='Section'
    sectionid= Column( Integer, primary_key=True, nullable=False )
    section= Column( String(50), nullable=False )
    def addappend(self, session):
        return sqlAppendIfNotExists(session, Section,
                                       section=self.section)

class Opportunity(Base):
    __tablename__='Opportunity'
    opportunityid= Column( Integer, primary_key=True, nullable=False )
    opportunityname= Column( String(255), nullable=True )
    company= Column( String(255), nullable=True )
    city= Column( String(100), nullable=True )
    state= Column( String(100), nullable=True )
    county= Column( String(100), nullable=True )
    startmonth= Column( String(3), nullable=True )
    startyear= Column( Integer, nullable=True )
    startdate= Column( DateTime, nullable=True )
    endmonth= Column( String(3), nullable=True )
    endyear= Column( Integer, nullable=True )
    enddate= Column( DateTime, nullable=True )
    def addappend(self, session):
        return sqlAppendIfNotExists(session, Opportunity,
            opportunityname=self.opportunityname,
            company=self.company,
            city=self.city,
            state=self.state,
            county=self.county,
            startmonth=self.startmonth,
            startyear=self.startyear,
            startdate=self.startdate,
            endmonth=self.endmonth,
            endyear=self.endyear,
            enddate=self.enddate)

class CVText(Base):
    __tablename__='CVText'
    cvtextid= Column( Integer, primary_key=True, nullable=False )
    textforshow= Column( String(8000), nullable=False )
    defaultorderind= Column( Integer, nullable=False )
    parenttextfk= Column( Integer, nullable=False )
    groupind= Column( Integer, nullable=False )
    dsflag= Column( Integer, nullable=False )
    cioflag= Column( Integer, nullable=False )
    sqlflag= Column( Integer, nullable=False )
    nedflag= Column( Integer, nullable=False )
    roletypefk= Column( Integer, ForeignKey('RoleType.roletypeid'), nullable=False )
    componentfk= Column( Integer, ForeignKey('Component.componentid'), nullable=False )
    sectionfk= Column( Integer, ForeignKey('Section.sectionid'), nullable=False )
    opportunityfk= Column( Integer, ForeignKey('Opportunity.opportunityid'), nullable=False )
    RoleType = relationship(RoleType)
    Component = relationship(Component)
    Section = relationship(Section)
    Opportunity = relationship(Opportunity)
    def addappend(self, session):
        return sqlAppendIfNotExists(session, CVText,
            textforshow=self.textforshow,
            defaultorderind=self.defaultorderind,
            parenttextfk=self.parenttextfk,
            groupind=self.groupind,
            dsflag=self.dsflag,
            cioflag=self.cioflag,
            sqlflag=self.sqlflag,
            nedflag=self.nedflag,
            RoleType=self.RoleType,
            Component=self.Component,
            Section=self.Section,
            Opportunity=self.Opportunity)

class EditxText(Base):
    __tablename__='EditxText'
    editfk = Column(Integer, ForeignKey('Edit.editid'), primary_key=True)
    cvtextfk = Column(Integer, ForeignKey('CVText.cvtextid'), primary_key=True)
    orderind= Column( Integer, primary_key=False, nullable=False, default=0)
    Edit = relationship(Edit)
    CVText = relationship(CVText)

class ComponentDefaultxComponent(Base):
    __tablename__='ComponentDefaultxComponent'
    componentdefaultfk = Column(Integer, ForeignKey('ComponentDefault.componentdefaultid'), primary_key=True)
    componentfk = Column(Integer, ForeignKey('Component.componentid'), primary_key=True)
    ComponentDefault = relationship(ComponentDefault)
    Component = relationship(Component)


Base.metadata.create_all(engine)









