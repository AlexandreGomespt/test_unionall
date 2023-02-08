CREATE   procedure [config].[SP_CONFIG_FILE] as 
	begin

	IF OBJECT_ID('tempdb..#config') IS NOT NULL
	begin
        drop table #config
	end

	CREATE TABLE #config(
	[INPUT_FILENAME] [nvarchar](255) NOT NULL,
	[INPUT_FILE_PATH] [nvarchar](255) NOT NULL,
	[NUMBER_OF_COLUMNS] [int] NOT NULL,
	[DELIMITER] [nvarchar](255) NULL,
	[DESTIONATION_TABLE_NAME] [nvarchar](255) NULL
) 		


						insert into #Config 
					    SELECT 
								*
								
						FROM 
						(
							--	([INPUT_FILENAME] 			,[INPUT_FILE_PATH] 		,[NUMBER_OF_COLUMNS] 	,[DELIMITER] ,[DESTIONATION_TABLE_NAME] )	
							     
						VALUES	('DIM_WorkLocation.csv'		,'raw'					,5						,','		,'DIM_WORKLOCATION'		    )
							   ,('DIM_OpCo LE.csv'			,'raw'					,6						,','		,'DIM_OPCO_LE'			    )
							--	([INPUT_FILENAME] 			,[INPUT_FILE_PATH] 		,[NUMBER_OF_COLUMNS] 	,[DELIMITER] ,[DESTIONATION_TABLE_NAME] )	
							)
						
						AS ents ([INPUT_FILENAME] 			,[INPUT_FILE_PATH] 		,[NUMBER_OF_COLUMNS] 	,[DELIMITER] ,[DESTIONATION_TABLE_NAME] )




	MERGE INTO [config].[Config_File] AS t
	USING #config AS s ON (t.[DESTIONATION_TABLE_NAME] = s.[DESTIONATION_TABLE_NAME])

	-- Updates
	WHEN MATCHED THEN UPDATE
	SET
	     t.[INPUT_FILE_PATH]				= s.[INPUT_FILE_PATH]
		,t.[NUMBER_OF_COLUMNS]				= s.[NUMBER_OF_COLUMNS]	
		,t.[DELIMITER]						= s.[DELIMITER]
	    ,t.[DESTIONATION_TABLE_NAME]		= s.[DESTIONATION_TABLE_NAME]
		

	-- Inserts
	WHEN NOT MATCHED THEN
	INSERT ( 
			  [INPUT_FILENAME]
			 ,[INPUT_FILE_PATH]			
			 ,[NUMBER_OF_COLUMNS]						
			 ,[DELIMITER]		
			 ,[DESTIONATION_TABLE_NAME]
							
	)
	VALUES (
			  [INPUT_FILENAME]
			 ,[INPUT_FILE_PATH]			
			 ,[NUMBER_OF_COLUMNS]						
			 ,[DELIMITER]		
			 ,[DESTIONATION_TABLE_NAME]	
	);
	end