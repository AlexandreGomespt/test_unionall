create     procedure [Config].[SP_Config_Model_Config_Object_Data] as 
	begin

	IF OBJECT_ID('tempdb..#config') IS NOT NULL
	begin
        drop table #config
	end

	CREATE TABLE #config(
	[Config_Model_ID] [int] NOT NULL,
	[Config_Object_ID] [int] NOT NULL,
	[FLG_Active] [bit] NOT NULL,
) 		


						insert into #Config 
					    SELECT 
								*
								
						FROM 
						(
							--	([Config_Model_ID]						,[Config_Object_ID]			,[FLG_Active])	
						VALUES	(1										,1							,1)
							   ,(1										,2							,1)
							   ,(1										,3							,1)
							   ,(1										,101						,1)
							   ,(1										,102						,1)
							   ,(1										,103						,1)
							   ,(1										,201						,1)
							   ,(1										,202						,1)
							   ,(1										,203			     		,1)
							   ,(2										,1							,1)
							   ,(2										,2							,1)
							   ,(2										,3							,1)
							   ,(2										,101						,0)
							   ,(2										,102						,0)
							   ,(2										,103						,0)
							   ,(2										,201						,0)
							   ,(2										,202						,0)
							   ,(2										,203			     		,0)
							--	([Config_Model_ID]						,[Config_Object_ID]			,[FLG_Active])	
						)
						
						AS ents ([Config_Model_ID]						,[Config_Object_ID]			,[FLG_Active])




	MERGE INTO [config].[Config_Model_Config_Object] AS t
	USING #config AS s ON (t.[Config_Model_ID]  = s.[Config_Model_ID]
					   and t.[Config_Object_ID] = s.[Config_Object_ID])

	-- Updates
	WHEN MATCHED THEN UPDATE
	SET
	     t.[FLG_Active]						= s.[FLG_Active]

	-- Inserts
	WHEN NOT MATCHED THEN
	INSERT ( 
			 [Config_Model_ID]	
			,[Config_Object_ID]
			,[FLG_Active] 

	)
	VALUES (
			 [Config_Model_ID]	
			,[Config_Object_ID]
			,[FLG_Active] 
	);
	end