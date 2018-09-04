DROP FUNCTION IF EXISTS dbo.udf_PM_Candidate_GetFormattedName;
GO

CREATE FUNCTION dbo.udf_PM_Candidate_GetFormattedName
(
    @EditID INT
)
RETURNS VARCHAR(255)
AS
BEGIN
    DECLARE @Return VARCHAR(255);

    SELECT @Return = cd.formattedname
    FROM dbo.Candidate cd
        INNER JOIN dbo.Edit e
            ON cd.candidateid = e.candidatefk
    WHERE e.editid = @EditID;
    RETURN @Return;

END;
GO
DROP PROCEDURE IF EXISTS dbo.usp_PM_Candidate_GetFormattedName;
GO
CREATE PROCEDURE dbo.usp_PM_Candidate_GetFormattedName @EditID INT
AS
SELECT dbo.udf_PM_Candidate_GetFormattedName(@EditID) AS formattedname;


GO
EXEC usp_PM_Candidate_GetFormattedName 2