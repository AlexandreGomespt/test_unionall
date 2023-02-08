CREATE     procedure [config].[SP_CONFIG_GROUP_DEPENDENCY_DATA] as 
	begin

	IF OBJECT_ID('tempdb..#config') IS NOT NULL
	begin
        drop table #config
	end

	CREATE TABLE #config(
	[PK_GROUP_DEPENDENCY] [int] NOT NULL  Primary Key,
	[Model_Name] [nvarchar](255) NOT NULL,
	[Group_Name] [nvarchar](255) NOT NULL,
	[DEPENDENCY_Model_Name] [nvarchar](255) NULL,
	[DEPENDENCY_Group_Name] [nvarchar](255) NULL,
) 		


						insert into #Config 
					    SELECT 
								*
								
						FROM 
						(
							--	([PK_GROUP_DEPENDENCY]			,[Model_Name]						,[Group_Name]		,[DEPENDENCY_Model_Name]	,[DEPENDENCY_Group_Name])	
						VALUES	(1								,'People Insights'					,'Extract_In'		,NULL						,NULL					)
							   ,(2								,'People Review'					,'Extract'			,'People Insights'		    ,'Extract_In'			)
							   ,(3								,'People Review'					,'Transform'		,'People Review'		    ,'Extract'			    )
							   ,(4								,'People Review'					,'Load'				,'People Review'			,'Transform'			)
							   ,(5								,'People Review'					,'Admin'			,'People Review'			,NULL					)		   
							   ,(6								,'RCM'								,'Extract_RCM'		,NULL						,NULL					)
							   ,(7								,'RCM'								,'Extract_01'		,NULL						,NULL					)
						--	   ,(8								,'RCM'								,'Extract_02'		,NULL						,NULL					)
							   ,(8								,'RCM'								,'Extract_02'		,'RCM'						,'Extract_01'			)					
							   ,(10								,'RCM'								,'Load_RCM'			,'RCM'						,'Extract_RCM'			)
							--	([PK_GROUP_DEPENDENCY]			,[Model_Name]						,[Group_Name]		,[DEPENDENCY_Model_Name]	,[DEPENDENCY_Group_Name])
							)
						
						AS ents ([PK_GROUP_DEPENDENCY]			,[Model_Name]						,[Group_Name]		,[DEPENDENCY_Model_Name]	,[DEPENDENCY_Group_Name])




	MERGE INTO [config].[Config_Group_DEPENDENCY] AS t
	USING #config AS s ON (t.[PK_GROUP_DEPENDENCY] = s.[PK_GROUP_DEPENDENCY])

	-- Updates
	WHEN MATCHED THEN UPDATE
	SET
		 t.[Model_Name]								= s.[Model_Name]	
	    ,t.[Group_Name]								= s.[Group_Name]
		,t.[DEPENDENCY_Model_Name]				    = s.[DEPENDENCY_Model_Name]
		,t.[DEPENDENCY_Group_Name]					= s.[DEPENDENCY_Group_Name]

		

	-- Inserts
	WHEN NOT MATCHED THEN
	INSERT ( 
			  [PK_GROUP_DEPENDENCY] 
			 ,[Model_Name] 
			 ,[Group_Name] 
			 ,[DEPENDENCY_Model_Name]
			 ,[DEPENDENCY_Group_Name]
							
	)
	VALUES (
			  [PK_GROUP_DEPENDENCY] 
			 ,[Model_Name] 
			 ,[Group_Name] 
			 ,[DEPENDENCY_Model_Name]
			 ,[DEPENDENCY_Group_Name]
	);
	end