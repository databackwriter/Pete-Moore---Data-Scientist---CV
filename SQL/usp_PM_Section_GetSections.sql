DROP PROCEDURE IF EXISTS dbo.usp_PM_Section_GetSections
GO
CREATE PROCEDURE dbo.usp_PM_Section_GetSections
AS
SELECT s.sectionid
     , s.section
FROM dbo.Section AS s
WHERE s.sectionid BETWEEN 2 AND 6
ORDER BY s.sectionid;