DROP PROCEDURE IF EXISTS dbo.usp_PM_EditxText_Add;
GO
CREATE PROCEDURE [dbo].[usp_PM_EditxText_Add]
    @EditFK INT
  , @CandidateFK INT
AS
BEGIN																										  

    DECLARE @L VARCHAR(255);
    SELECT @L = ct.legacycvtype
    FROM dbo.Edit AS e
        INNER JOIN dbo.Candidate AS c
            ON c.candidateid = e.candidatefk
        INNER JOIN dbo.CVType AS ct
            ON ct.cvtypeid = e.cvtypefk
    WHERE e.editid = @EditFK
          AND c.candidateid = @CandidateFK;

    DECLARE @LSQL NVARCHAR(512)
        = 'SELECT @EditFK
     , ct.cvtextid
     , ROW_NUMBER() OVER ( ORDER BY ( SELECT   NULL  ) ) AS localorderind
FROM dbo.CVText AS ct
    LEFT OUTER JOIN dbo.EditxText AS et
        ON et.cvtextfk = ct.cvtextid
           AND et.editfk = @EditFK
WHERE ct.#L > 0
AND et.editfk IS NULL
ORDER BY ct.groupind
       , ct.nedflag;'
          , @Params NVARCHAR(512) = '@EditFK INT';

    SELECT @LSQL = REPLACE(@LSQL, '#L', QUOTENAME(@L));


    INSERT INTO dbo.EditxText
    (
        editfk
      , cvtextfk
      , orderind
    )
    EXEC sys.sp_executesql @script = @LSQL
                         , @params = @Params
                         , @EditFK = @EditFK;

END;





GO
EXEC [dbo].[usp_PM_EditxText_Add] @EditFK  =3, @CandidateFK = 1





