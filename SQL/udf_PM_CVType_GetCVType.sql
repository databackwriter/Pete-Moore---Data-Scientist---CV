DROP FUNCTION IF EXISTS dbo.udf_PM_CVType_GetCVType;
GO

CREATE FUNCTION dbo.udf_PM_CVType_GetCVType
(
    @EditID INT
)
RETURNS VARCHAR(255)
AS
BEGIN
    DECLARE @Return VARCHAR(255);

    SELECT @Return = cv.cvtype
    FROM dbo.CVType cv
        INNER JOIN dbo.Edit e
            ON cv.CVTypeid = e.CVTypefk
    WHERE e.editid = @EditID;
    RETURN @Return;

END;
GO
DROP PROCEDURE IF EXISTS dbo.usp_PM_CVType_GetCVType;
GO
CREATE PROCEDURE dbo.usp_PM_CVType_GetCVType @EditID INT
AS
SELECT dbo.udf_PM_CVType_GetCVType(@EditID) AS cvtype;
GO
EXEC usp_PM_CVType_GetCVType 2