CREATE   procedure [config].[SP_CONFIG_OBJECT_DEPENDENCY_DATA] as 
	begin

	IF OBJECT_ID('tempdb..#config') IS NOT NULL
	begin
        drop table #config
	end

	CREATE TABLE #config(
    [PK_Object_DEPENDENCY] [int] Primary Key
   ,[Model_Name] [nvarchar](255) NOT NULL
   ,[Group_Object_Name] [nvarchar](255) NOT NULL
   ,[Object_Name] [nvarchar](255) NOT NULL
   ,[DEPENDENCY_Object_Name] [nvarchar](255) NOT NULL
   ,[FLG_Is_Active] [bit] NOT NULL
) 		


						insert into #Config 
					    SELECT 
								*
								
						FROM 
						(
							--	([PK_Object_DEPENDENCY]	,[Model_Name]			,[Group_Object_Name]	,[Object_Name]			,[DEPENDENCY_Object_Name] ,[FLG_Is_Active] )	
						VALUES	(1						,'People Review'		,'Extract'				,'Extract_files03'		,'Extract_files02'		  ,1)
							   ,(2						,'People Review'		,'Extract'				,'Extract_files02'		,'Extract_files01'		  ,1)
							--	([PK_Object_DEPENDENCY]	,[Model_Name]			,[Group_Object_Name]	,[Object_Name]			,[DEPENDENCY_Object_Name] ,[FLG_Is_Active] )	
						)
						AS ents ([PK_Object_DEPENDENCY]	,[Model_Name]			,[Group_Object_Name]	,[Object_Name]			,[DEPENDENCY_Object_Name] ,[FLG_Is_Active] )	
						


	MERGE INTO [config].[Config_Object_DEPENDENCY] AS t
	USING #config AS s ON (t.[PK_Object_DEPENDENCY] = s.[PK_Object_DEPENDENCY])

	-- Updates
	WHEN MATCHED THEN UPDATE
	SET
		 t.[Model_Name]								= s.[Model_Name]
		,t.[Group_Object_Name]						= s.[Group_Object_Name]
		,t.[Object_Name]							= s.[Object_Name]
		,t.[DEPENDENCY_Object_Name]					= s.[DEPENDENCY_Object_Name]
		,t.[FLG_Is_Active]							= s.[FLG_Is_Active]

						

		

	-- Inserts
	WHEN NOT MATCHED THEN
	INSERT ( 
			   [PK_Object_DEPENDENCY]
			  ,[Model_Name]								
			  ,[Group_Object_Name]						
			  ,[Object_Name]							
			  ,[DEPENDENCY_Object_Name]					
			  ,[FLG_Is_Active]							
						

	)
	VALUES (
			   [PK_Object_DEPENDENCY]
			  ,[Model_Name]								
			  ,[Group_Object_Name]						
			  ,[Object_Name]							
			  ,[DEPENDENCY_Object_Name]					
			  ,[FLG_Is_Active]	
	);
	end