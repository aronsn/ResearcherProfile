DROP SCHEMA IF EXISTS researcherprofile;

DROP USER IF EXISTS Researcher;

CREATE SCHEMA researcherprofile;

USE researcherprofile;

CREATE USER Researcher IDENTIFIED BY 'password';

GRANT SELECT ON * TO Researcher;

GRANT INSERT ON * TO Researcher;

GRANT UPDATE ON * TO Researcher;

GRANT DELETE ON * TO Researcher;

CREATE TABLE Conference
(
ConferenceName CHAR(80),
ConferenceField CHAR(40),
ConferenceTime DATE,
ConferenceLocation CHAR(30),
Link CHAR(70),
CONSTRAINT ConferencePK PRIMARY KEY(ConferenceName, ConferenceTime)
);

CREATE TABLE Project
(
ProjectName CHAR(80),
ProjectField CHAR(40),
ProjectStart DATE,
ProjectLocation CHAR(30),
CONSTRAINT ProjectPK PRIMARY KEY(ProjectName, ProjectStart)
);

-- Test data
INSERT INTO Conference VALUES('NOKIOS', 'HCI', '2019-10-29', 'Norway, Trondheim', 'nokios.no');
INSERT INTO Conference VALUES('ICBDC ', 'Big Data', '2019-05-10', 'China, Guangzhou', 'icbdc.org');
INSERT INTO Conference VALUES('Paranoia', 'HCI', '2019-05-21', 'Norway, Oslo', 'paranoia.watchcom.no');
INSERT INTO Conference VALUES('ICISD', 'HCI', '2019-04-24 ', 'United Kingdom, London', 'waset.org/conference/2019/04/london/ICISD');
INSERT INTO Conference VALUES('AI and big data expo', 'Big data', '2019-11-13 ', 'United States, California', 'ai-expo.net');
INSERT INTO Conference VALUES('AI and big data expo', 'Big data', '2019-06-19 ', 'Netherlands, Amsterdam', 'ai-expo.net');
INSERT INTO Conference VALUES('AI and big data expo', 'Big data', '2019-04-25 ', 'United Kingdom, London', 'ai-expo.net');
INSERT INTO Conference VALUES('The Data Sciense Conference', 'Big data', '2019-05-23 ', 'United States, Boston', 'thedatascienceconference.com');
INSERT INTO Conference VALUES('Modern Data Management Summit', 'Open data', '2019-02-26 ', 'United States, San Francisco', 'theinnovationenterprise.com/summits');
INSERT INTO Conference VALUES('Data Fest 2019', 'Open data', '2019-03-11 ', 'Scotland, Multiple venues', 'datafest.global');
INSERT INTO Conference VALUES('Open data science conference', 'Open data', '2019-05-1 ', 'United States, Boston', 'odsc.com');
INSERT INTO Conference VALUES('Enterprise Data World', 'Open data', '2019-03-17 ', 'United States, Boston', 'edw2019.dataversity.net/index.cfm');
INSERT INTO Conference VALUES('Strata Data Conference', 'Open data', '2019-04-29 ', 'United States, London', 'https://conferences.oreilly.com/strata');
INSERT INTO Conference VALUES('Data conference 	', ' Software Engineering ', '2019-03-25 ', 'United States, San Francisco', 'conferences.oreilly.com/strata/strata-ca');
INSERT INTO Conference VALUES('ICSE	', 'Software Engineering education ', '2019-05-25 ', 'Canada, Montréal', '2019.icse-conferences.org');
INSERT INTO Conference VALUES('ISEE ', 'Software Engineering education', '2019-02-19 ', 'Germany, Stuttgart', 'wikicfp.com/cfp/servlet/event.showcfp?eventid=83157&copyownerid=93302');
INSERT INTO Conference VALUES('CSEE&T', 'Software Engineering education ', '2019-01-08 ', 'United States, Hawaii', 'easychair.org/cfp/CSEET31');
INSERT INTO Conference VALUES('GohperCon', 'Software Engineering ', '2019-07-24 ', 'United States, San Diego', 'gophercon.com');
INSERT INTO Conference VALUES('ApacheCon', 'Software Engineering', '2019-09-09 ', 'United States, Las Vegas', 'apachecon.com/acna19/index.html');


INSERT INTO Project VALUES('Researching cloud', 'Big data ', '2020-10-11 ', 'United States, Conneticut');
INSERT INTO Project VALUES('Designing cloud', 'Software Engineering ', '2020-12-19 ', 'United States, Conneticut');
INSERT INTO Project VALUES('Creating cloud', 'Software Engineering ', '2021-01-21 ', 'United States, Conneticut');
INSERT INTO Project VALUES('Car sales', 'Software Engineering ', '2018-09-05 ', 'Norway, Oslo');
INSERT INTO Project VALUES('Data warehouse', ' Big data', '2018-06-07 ', 'Madagascar');
INSERT INTO Project VALUES('Data silo', 'Big data', '2019-05-09 ', 'United States, Maine');
INSERT INTO Project VALUES('Research saving hospital data ', 'Open data', '2019-07-24 ', 'Norway');
INSERT INTO Project VALUES('Research new way of hospital data', 'Open data', '2019-010-01 ', 'Norway');
INSERT INTO Project VALUES('Testing new way of saving hospital data', 'Big data ', '2019-012-09 ', 'Norway');
INSERT INTO Project VALUES('Implementing New way of saving hospital data', 'Software engineering', '2021-03-09 ', 'Norway');
