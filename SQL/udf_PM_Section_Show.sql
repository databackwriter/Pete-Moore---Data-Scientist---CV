DROP FUNCTION IF EXISTS dbo.udf_PM_Section_Show;
GO
CREATE FUNCTION dbo.udf_PM_Section_Show
(
    @editid INT
  , @sectionid INT
  , @roletypeid INT
)
RETURNS TABLE --· Introduction of per-consultant MI using SQL Server and ASP.	 --note bullets are appearing as ascii=183
AS
RETURN
(
    SELECT cd.formattedname
         , cv.cvtype
         , e.editname
         , s.section
         , rt.roletypeid
         , ct.textforshow
         , ct.groupind
         , c.component
         , ct.cvtextid
         , et.orderind
         , cdf.headerlevel
         , cdf.prefix
         , cdf.suffix
         , cdf.indent
    FROM dbo.CVText AS ct
        INNER JOIN dbo.Component AS c
            ON c.componentid = ct.componentfk
        LEFT OUTER JOIN dbo.Opportunity AS o
            ON o.opportunityid = ct.opportunityfk
               AND o.opportunityid > 1 --ignore that being born was an oportunity :-)
        INNER JOIN dbo.Section AS s
            ON s.sectionid = ct.sectionfk
        INNER JOIN dbo.RoleType AS rt
            ON rt.roletypeid = ct.roletypefk
        INNER JOIN dbo.EditxText AS et
            ON et.cvtextfk = ct.cvtextid
        INNER JOIN dbo.Edit AS e
            ON e.editid = et.editfk
        INNER JOIN dbo.CVType AS cv
            ON cv.cvtypeid = e.cvtypefk
        INNER JOIN dbo.Candidate AS cd
            ON cd.candidateid = e.candidatefk
        INNER JOIN dbo.ComponentDefaultxComponent AS cdc
            ON cdc.componentfk = c.componentid
        INNER JOIN dbo.ComponentDefault AS cdf
            ON cdf.componentdefaultid = cdc.componentdefaultfk
    WHERE s.sectionid = @sectionid
          AND
          (
              rt.roletypeid = @roletypeid
              OR rt.roletypeid = 1 --1 means all role types
              OR @roletypeid = 1
          )
          AND e.editid = @editid
);

GO



DROP PROCEDURE IF EXISTS dbo.usp_PM_Section_Show;
GO
CREATE PROCEDURE dbo.usp_PM_Section_Show
    @editid INT
  , @sectionid INT
  , @roletypeid INT = 1
AS
BEGIN
    SELECT u.textforshow
         , u.groupind
         , u.component
         , u.cvtextid
         , u.orderind
    FROM dbo.udf_PM_Section_Show(@editid, @sectionid, @roletypeid) u
    ORDER BY u.orderind;


END;

GO

EXEC dbo.usp_PM_Section_Show 2, 1, 3;

