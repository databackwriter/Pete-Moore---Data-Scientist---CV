DROP PROCEDURE IF EXISTS dbo.usp_PM_ComponentDefaultxComponent_Add;
GO
CREATE PROCEDURE [dbo].[usp_PM_ComponentDefaultxComponent_Add] @ComponentFK INT
AS
BEGIN

    INSERT INTO dbo.ComponentDefaultxComponent
    (
        componentdefaultfk
      , componentfk
    )
    SELECT cd.componentdefaultid
         , c.componentid
    FROM dbo.ComponentDefault AS cd
        INNER JOIN dbo.Component AS c
            ON cd.componentdefault = c.component
        LEFT OUTER JOIN dbo.ComponentDefaultxComponent AS cdc
            ON cdc.componentdefaultfk = cd.componentdefaultid
               AND cdc.componentfk = c.componentid
    WHERE c.componentid = @ComponentFK
          AND cdc.componentdefaultfk IS NULL;

END;