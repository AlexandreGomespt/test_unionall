CREATE     procedure [config].[SP_Execution_List_Data] as 
	begin

	IF OBJECT_ID('tempdb..#config') IS NOT NULL
	begin
        drop table #config
	end

	CREATE TABLE #config(
	[PK_Execution_List] [int] Primary Key,
	[Model_Name] [nvarchar](255) NOT NULL,
	[Group_Name] [nvarchar](255) NOT NULL,
	[Object_Name] [nvarchar](255) NOT NULL,
	[Object_Type] [nvarchar](255) NOT NULL,
	[Source_Object_Path] [nvarchar](255) NULL,
	[Destination_Object_Path] [nvarchar](255) NULL,
	[Periodicity] [nvarchar](255) NOT NULL,
	[Parameters_List] [nvarchar](255) NULL,
	[FLG_Is_Active] [bit] NOT NULL
) 		


						insert into #Config 
					    SELECT 
								*
								
						FROM 
						(
							--	([PK_Execution_List]	,[Model_Name]		,[Group_Name] ,	[Object_Name]		,[Object_Type]      ,[Source_Object_Path] ,[Destination_Object_Path]  ,[Periodicity]  ,[Parameters_List] ,[FLG_Is_Active] )	
						VALUES	(1						,'People Insights'	,'Extract_In' ,'Extract_In'			,'Notebook'			,'Folder1/'			  ,'Folder2/'				  ,'Daily'		  ,''				 ,1)
							   ,(2						,'People Review'	,'Extract'	  ,'Extract_files01'	,'Notebook'			,'Folder1/'			  ,'Folder2/'				  ,'Daily'		  ,''				 ,1)
							   ,(3						,'People Review'	,'Extract'	  ,'Extract_files02'	,'Notebook'			,'Folder1/'			  ,'Folder2/'				  ,'Daily'		  ,''				 ,1)
							   ,(4						,'People Review'	,'Extract'	  ,'Extract_files03'	,'Notebook'			,'Folder1/'			  ,'Folder2/'				  ,'Daily'		  ,''				 ,1)
							   ,(5						,'People Review'	,'Transform'  ,'Transform_files01'	,'Notebook'			,'Folder1/'			  ,'Folder2/'				  ,'Daily'		  ,''				 ,1)
							   ,(6						,'People Review'	,'Transform'  ,'Transform_files02'	,'Notebook'			,'Folder1/'			  ,'Folder2/'				  ,'Daily'		  ,''				 ,1)				
							   ,(7						,'People Review'	,'Transform'  ,'Transform_files03'	,'Notebook'			,'Folder1/'			  ,'Folder2/'				  ,'Daily'		  ,''				 ,1)
							   ,(8						,'People Review'	,'Extract'	  ,'Extract_files04'	,'Notebook'			,'Folder1/'			  ,'Folder2/'				  ,'Daily'		  ,''				 ,1)
							   ,(9						,'People Review'	,'Extract'	  ,'Extract_files05'	,'Notebook'			,'Folder1/'			  ,'Folder2/'				  ,'Daily'		  ,''				 ,1)
							   ,(10						,'People Review'	,'Load'		  ,'Load'				,'Notebook'			,'Folder1/'			  ,'Folder2/'				  ,'Daily'		  ,''				 ,1)
							   ,(11 					,'RCM'				,'Extract_RCM','Extract_RCM1'		,'Notebook'			,'Folder1/'			  ,'Folder2/'				  ,'Daily'		  ,''				 ,1)
							   ,(12 					,'RCM'				,'Extract_01' ,'Extract_RCM2'		,'Notebook'			,'Folder1/'			  ,'Folder2/'				  ,'Daily'		  ,''				 ,1)
							   ,(13 					,'RCM'				,'Extract_02' ,'Extract_RCM3'		,'Notebook'			,'Folder1/'			  ,'Folder2/'				  ,'Daily'		  ,''				 ,1)
							   ,(14 					,'RCM'				,'Load_RCM'	  ,'Load_RCM'		    ,'Notebook'			,'Folder1/'			  ,'Folder2/'				  ,'Daily'		  ,''				 ,1)
							--	([PK_Execution_List]	,[Model_Name]		,[Group_Name] ,	[Object_Name]		,[Object_Type]      ,[Source_Object_Path] ,[Destination_Object_Path]  ,[Periodicity]  ,[Parameters_List] ,[FLG_Is_Active] )	
						)
						AS ents ([PK_Execution_List]	,[Model_Name]		,[Group_Name] ,	[Object_Name]		,[Object_Type]      ,[Source_Object_Path] ,[Destination_Object_Path]  ,[Periodicity]  ,[Parameters_List] ,[FLG_Is_Active] )	
						


	MERGE INTO [config].[Execution_List] AS t
	USING #config AS s ON (t.[PK_Execution_List] = s.[PK_Execution_List])

	-- Updates
	WHEN MATCHED THEN UPDATE
	SET
		 t.[Model_Name]								= s.[Model_Name]	
		,t.[Group_Name] 							= s.[Group_Name]	
		,t.[Object_Name]							= s.[Object_Name]	
		,t.[Object_Type]      						= s.[Object_Type]	
		,t.[Source_Object_Path] 					= s.[Source_Object_Path]	
		,t.[Destination_Object_Path]  				= s.[Destination_Object_Path]	
		,t.[Periodicity]  							= s.[Periodicity]	
		,t.[Parameters_List]  						= s.[Parameters_List]	
		,t.[FLG_Is_Active]							= s.[FLG_Is_Active]
						

		

	-- Inserts
	WHEN NOT MATCHED THEN
	INSERT ( 
			   [PK_Execution_List]
			  ,[Model_Name]
			  ,[Group_Name] 
			  ,[Object_Name]		
			  ,[Object_Type]      
			  ,[Source_Object_Path] 
			  ,[Destination_Object_Path]  
			  ,[Periodicity]  
			  ,[Parameters_List]  
			  ,[FLG_Is_Active]
						

	)
	VALUES (
			   [PK_Execution_List]
			  ,[Model_Name]
			  ,[Group_Name] 
			  ,[Object_Name]		
			  ,[Object_Type]      
			  ,[Source_Object_Path] 
			  ,[Destination_Object_Path]  
			  ,[Periodicity]  
			  ,[Parameters_List]  
			  ,[FLG_Is_Active]
	);
	end