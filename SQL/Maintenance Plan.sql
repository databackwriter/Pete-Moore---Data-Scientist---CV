--```{sql, echo=TRUE, eval=FALSE}
USE [msdb]
GO
DECLARE @jobId BINARY(16)
EXEC  msdb.dbo.sp_add_job @job_name=N'Back up TufteCV on startup', 
		@enabled=1, 
		@notify_level_eventlog=0, 
		@notify_level_email=2, 
		@notify_level_page=2, 
		@delete_level=0, 
		@description=N'Backs up the TufteCV database on startup ', 
		@category_name=N'[Uncategorized (Local)]', 
		@owner_login_name=N'sa', @job_id = @jobId OUTPUT
select @jobId
GO
EXEC msdb.dbo.sp_add_jobserver @job_name=N'Back up TufteCV on startup', @server_name = N'73D40AA1D1C1'
GO
USE [msdb]
GO
EXEC msdb.dbo.sp_add_jobstep @job_name=N'Back up TufteCV on startup', @step_name=N'Backup TufteCV to local device', 
		@step_id=1, 
		@cmdexec_success_code=0, 
		@on_success_action=1, 
		@on_fail_action=2, 
		@retry_attempts=0, 
		@retry_interval=0, 
		@os_run_priority=0, @subsystem=N'TSQL', 
		@command=N'USE master;
GO

IF NOT EXISTS
(
    SELECT *
    FROM sys.configurations AS c
    WHERE c.name = ''Show Advanced Options''
)
BEGIN
    EXEC sys.sp_configure @configname = ''Show Advanced Options'' -- varchar(35)
                        , @configvalue = 1;                     -- int
    RECONFIGURE WITH OVERRIDE;
END;
GO
IF NOT EXISTS
(
    SELECT *
    FROM sys.configurations AS c
    WHERE c.name = ''Agent XPs''
)
BEGIN
    EXEC sys.sp_configure @configname = ''Agent XPs'' -- varchar(35)
                        , @configvalue = 1;         -- int
    RECONFIGURE WITH OVERRIDE;
END;
GO
IF NOT EXISTS
(
    SELECT *
    FROM sys.configurations AS c
    WHERE c.name = ''Agent XPs''
)
BEGIN
    EXEC sys.sp_configure @configname = ''Agent XPs'' -- varchar(35)
                        , @configvalue = 1;         -- int
    RECONFIGURE WITH OVERRIDE;
END;
GO
USE [master];
GO
IF NOT EXISTS
(
    SELECT *
    FROM sys.backup_devices AS bd
    WHERE bd.name = ''TufteCV''
)
    EXEC master.sys.sp_addumpdevice @devtype = N''disk''
                                  , @logicalname = N''TufteCV''
                                  , @physicalname = N''/var/opt/mssql/data/TufteCV.bak'';
GO
BACKUP DATABASE TufteCV TO TufteCV;
GO
DECLARE @CopyLocalCommand NVARCHAR(512)
    = ''docker cp '' + @@SERVERNAME + '':/var/opt/mssql/data/TufteCV.bak /Users/petermoore/Documents/Data'';
PRINT @CopyLocalCommand;


', 
		@database_name=N'master', 
		@flags=0
GO
USE [msdb]
GO
EXEC msdb.dbo.sp_update_job @job_name=N'Back up TufteCV on startup', 
		@enabled=1, 
		@start_step_id=1, 
		@notify_level_eventlog=0, 
		@notify_level_email=2, 
		@notify_level_page=2, 
		@delete_level=0, 
		@description=N'Backs up the TufteCV database on startup ', 
		@category_name=N'[Uncategorized (Local)]', 
		@owner_login_name=N'sa', 
		@notify_email_operator_name=N'', 
		@notify_page_operator_name=N''
GO
USE [msdb]
GO
DECLARE @schedule_id int
EXEC msdb.dbo.sp_add_jobschedule @job_name=N'Back up TufteCV on startup', @name=N'Back up TufteCV scheduled for start up', 
		@enabled=1, 
		@freq_type=64, 
		@freq_interval=1, 
		@freq_subday_type=0, 
		@freq_subday_interval=0, 
		@freq_relative_interval=0, 
		@freq_recurrence_factor=1, 
		@active_start_date=20180816, 
		@active_end_date=99991231, 
		@active_start_time=0, 
		@active_end_time=235959, @schedule_id = @schedule_id OUTPUT
select @schedule_id
GO

--```