CREATE   procedure [config].[SP_CONFIG_MODEL_DATA] as 
	begin

	IF OBJECT_ID('tempdb..#config') IS NOT NULL
	begin
        drop table #config
	end

	CREATE TABLE #config(
	[PK_CONFIG_MODEL] [int] NOT NULL Primary Key,
	[Model_Name] [nvarchar](255) NOT NULL,
	[Periodicity] [nvarchar](255) NULL,
	[DT_LAST_SUCCESS_EXECUTION] datetime,
	[FLG_Is_Active] [bit] NOT NULL,
) 		


						insert into #Config 
					    SELECT 
								*
								
						FROM 
						(
							--	([PK_Config_Model]			,[Model_Name]						,[Periodicity]		,[DT_LAST_SUCCESS_EXECUTION]	,[FLG_Is_Active])	
						VALUES	(1							,'People Insights'					,'Daily'			,NULL								,1			 )
							   ,(2							,'People Review'					,'Daily'			,NULL								,1			 )
							   ,(3							,'RCM'								,'Monthly'			,'2022-12-22'					,1			 )
							--	([PK_Config_Model]			,[Model_Name]						,[Periodicity]		,[DT_LAST_SUCCESS_EXECUTION]	,[FLG_Is_Active])	
							)
						
						AS ents ([PK_CONFIG_MODEL]			,[Model_Name]						,[Periodicity]		,[DT_LAST_SUCCESS_EXECUTION]    ,[FLG_Is_Active])




	MERGE INTO [config].[Config_Model] AS t
	USING #config AS s ON (t.[PK_CONFIG_MODEL] = s.[PK_CONFIG_MODEL])

	-- Updates
	WHEN MATCHED THEN UPDATE
	SET
	     t.[Model_Name]					= s.[Model_Name]
		,t.[Periodicity]				= s.[Periodicity]	
		,t.[DT_LAST_SUCCESS_EXECUTION]  = s.[DT_LAST_SUCCESS_EXECUTION]
	    ,t.[FLG_Is_Active]				= s.[FLG_Is_Active]
		

	-- Inserts
	WHEN NOT MATCHED THEN
	INSERT ( 
			  [PK_CONFIG_MODEL]			
			 ,[Model_Name]						
			 ,[Periodicity]		
			 ,[DT_LAST_SUCCESS_EXECUTION]
			 ,[FLG_Is_Active]	
							
	)
	VALUES (
			  [PK_CONFIG_MODEL]			
			 ,[Model_Name]						
			 ,[Periodicity]		
			 ,[DT_LAST_SUCCESS_EXECUTION]
			 ,[FLG_Is_Active]	
	);
	end