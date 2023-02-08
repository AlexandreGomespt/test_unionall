create procedure [config].[SP_EXECUTION_LIST_TO_RUN1] as
begin
--truncate table [config].[EXECUTION_LIST_TO_RUN];
	WITH cte0 AS (
						SELECT	DISTINCT	 t1.[Model_Name]
											,t1.[Group_Name]
											,t1.[Object_Name]
											,t2.[Dependancy_Object_Name]
											,t1.DT_End_Execution
								FROM 
								
								(select exec_list.* from 
								[config].[Execution_List] exec_list
								inner join config.CONFIG_MODEL t3
						 on t3.MODEL_NAME=exec_list.MODEL_NAME
						WHERE   ( (t3.PERIODICITY='Monthly' and GETDATE() > DATEADD(month, 1, t3.[DT_LAST_SUCCESS_EXECUTION]) )
						
									OR (t3.PERIODICITY='Daily' and 
									ISNULL( TRY_CONVERT(date,[DT_LAST_SUCCESS_EXECUTION],23),TRY_CONVERT(date,DATEADD(DAY,-1,GETDATE()),103))< CONVERT(date,getdate(),23)
									    )
						         )
						AND t3.FLG_IS_ACTIVE =1
								) as t1 

								LEFT JOIN 
								[config].[Config_Object_Dependancy]  t2 on  t1.[Model_Name]	= t2.[Model_Name]
																		and t1.[Group_Name]	= t2.[Group_Object_Name]
																		and t1.[Object_Name]= t2.[Object_Name]
								where t1.FLG_Is_Active =1  
								AND (	(ISNULL( TRY_CONVERT(DATE,DT_End_Execution,103),TRY_CONVERT(date,DATEADD(DAY,-1,GETDATE()),103)) <  TRY_CONVERT(date,GETDATE(),103)
											and t1.Periodicity='Daily' 
										) 
										or  
										(  t1.Periodicity='Daily' AND 
											(ISNULL( TRY_CONVERT(DATE,DT_End_Execution,103),TRY_CONVERT(date,DATEADD(DAY,-1,GETDATE()),103)) =  TRY_CONVERT(date,GETDATE(),103)
											and t1.Status='Failed')
										)
								    )
								OR  (   t1.Periodicity='Monthly'  AND 
									
										(DATEADD(DAY,1,EOMONTH(GETDATE(),-1)) > ISNULL( TRY_CONVERT(DATE,DT_End_Execution,103),TRY_CONVERT(date,DATEADD(month,-1,GETDATE()),103))		
										)
										OR
										(
										(DATEADD(DAY,1,EOMONTH(GETDATE(),-1)) = ISNULL( TRY_CONVERT(DATE,DT_End_Execution,103),TRY_CONVERT(date,DATEADD(month,-1,GETDATE()),103))	)
										and t1.Status='Failed'
										)
									)
		), 
		cte ( [Model_Name],[Group_Name],[Object_Name], [Dependancy_Object_Name], [level], [path]) AS (
						
						SELECT  distinct
											 [Model_Name]
											,[Group_Name]
											,[Object_Name]
											,[Dependancy_Object_Name]
											,[Level]=  1 
											--,[path_hir]	 = CAST([Parent Position Code] AS VARCHAR(1000))
											,[path]	 = ISNULL(CAST([Dependancy_Object_Name] AS VARCHAR(1000)),'')
						FROM cte0
						
								UNION ALL
						SELECT   c.[Model_Name]
								,c.[Group_Name]
								,c.[Object_Name]
								,c.[Dependancy_Object_Name]
								,[level]							= cte.[level] + 1
								,[path]								= CAST((c.[Dependancy_Object_Name] + '|' + cte.[path]) AS VARCHAR(1000))
						FROM cte0 c 
						INNER JOIN cte 
						ON c.[Dependancy_Object_Name]     = cte.[Object_Name] 
						where [level]<20
		),
		Object_table AS(
					SELECT DISTINCT  t1.*
					FROM cte AS t1
		
		
						INNER JOIN 
					(
						SELECT  [Model_Name]
							   ,[Group_Name]
							   ,[Object_Name]
							   ,[level_max] =	MAX([level]) 

							   
							   FROM cte
							   GROUP BY  [Model_Name]
										,[Group_Name]
										,[Object_Name]
					) AS t2 
						ON  t1.[Model_Name]	  =   t2.[Model_Name] 
						AND t1.[Group_Name]	  =   t2.[Group_Name] 
						AND t1.[Object_Name]  =	  t2.[Object_Name]
						AND t2.level_max=t1.level
		),


		-----------------------------------------------------

		cte0_g AS (
						SELECT t2.[Group_Dependancy_ID]
							,t2.[Model_Name]
							,t2.[Group_Name]
							,t2.[Dependancy_Model_Name]
							,t2.[Dependancy_Group_Name]
						FROM [config].[Config_Model] t1 
						
						LEFT JOIN [config].[Config_Group_Dependancy] t2 ON t1.Model_Name = t2.Model_Name
					
					--troquei left por inner e [config].[Execution_List]
					    inner JOIN Object_table t3          ON t3.Group_Name = t2.Group_Name
						LEFT JOIN [config].[Config_Model] t4			  ON t4.Model_Name = t1.Model_Name 	
						
						WHERE t4.[FLG_Is_Active]=1 AND ISNULL(TRY_CONVERT(DATE,t4.[DT_Last_Success_Execution],103),'1900-01-01') <> TRY_CONVERT(DATE,GETDATE(),103)
						AND   t4.[Periodicity]='Daily'
						
								
		), 
		cte_g ([Group_Dependancy_ID], [Model_Name], [Group_Name],[Dependancy_Model_Name] ,[Dependancy_Group_Name], [level], [path]) AS (
						
						SELECT DISTINCT 
											 [Group_Dependancy_ID]
											,[Model_Name]
											,[Group_Name]
											,[Dependancy_Model_Name]
											,[Dependancy_Group_Name]
											,[Level]=  1 
											--,[path_hir]	 = CAST([Parent Position Code] AS VARCHAR(1000))
											,[path]	 = ISNULL(CAST([Dependancy_Group_Name] AS VARCHAR(1000)),'')
						FROM cte0_g
						
								UNION ALL
						SELECT   c.[Group_Dependancy_ID]
								,c.[Model_Name]
								,c.[Group_Name]
								,c.[Dependancy_Model_Name]
								,c.[Dependancy_Group_Name] 
								,[level]							= cte_g.[level] + 1
								,[path]								= CAST((c.[Dependancy_Group_Name] + '|' + cte_g.[path]) AS VARCHAR(1000))
						FROM cte0_g c 
						INNER JOIN cte_g 
						ON c.[Dependancy_Group_Name]     = cte_g.[Group_Name] and 
						c.[Model_Name]		    = cte_g.[Model_Name] 
						--where [level]<20
		),
		Group_table AS(
					SELECT DISTINCT  t1.*
					FROM cte_g AS t1
		
		
						INNER JOIN 
					(
						SELECT  [Model_Name]
							   ,[Group_Name]
							   ,[level_max] =	MAX([level]) 

							   
							   FROM cte_g
							   GROUP BY [Model_Name],[Group_Name]
		
					) AS t2 
						ON t1.[Model_Name]	=   t2.[Model_Name] 
						AND t1.[level]		=   t2.[level_max] 
						and t1.[Group_Name]	=   t2.[Group_Name]
		),

		---------------------------------------------------

		cte0_m AS (
						SELECT   distinct 
										 t1.[Model_Name]
										 
										 ,case when [Dependancy_Model_Name] = t1.[Model_Name] then NULL else [Dependancy_Model_Name] end as [Dependancy_Model_Name]
					     FROM [config].[Config_Group_Dependancy] t1
						 inner join (select distinct model_name from Object_table) t2 
						 on t1.Model_Name=t2.Model_Name
						
								
		), 
		cte_m ( [Model_Name],[Dependancy_Model_Name],  [level], [path]) AS (
						
						SELECT DISTINCT 
											 
											 [Model_Name]
											,[Dependancy_Model_Name]
											,[Level]=  1 
											--,[path_hir]	 = CAST([Parent Position Code] AS VARCHAR(1000))
											,[path]	 = ISNULL(CAST([Dependancy_Model_Name] AS VARCHAR(1000)),'')
						FROM cte0_m
						
								UNION ALL
						SELECT   c.[Model_Name]
								,c.[Dependancy_Model_Name]
								,[level]							= cte_m.[level] + 1
								,[path]								= CAST((c.[Dependancy_Model_Name] + '|' + cte_m.[path]) AS VARCHAR(1000))
						FROM cte0_m c 
						INNER JOIN cte_m 
						ON c.[Dependancy_Model_Name]     = cte_m.[Model_Name] 
						where [level]<20
		),
		Model_tabel AS(
					SELECT DISTINCT  t1.*
					FROM cte_m AS t1
		
		
						INNER JOIN 
					(
						SELECT  [Model_Name]
							   ,[level_max] =	MAX([level]) 

							   
							   FROM cte_m
							   GROUP BY [Model_Name]
		
					) AS t2 
						ON t1.[Model_Name]	=   t2.[Model_Name] 
						AND t1.[level]		=   t2.[level_max] 
		)
		--------------
	insert into	[config].[EXECUTION_LIST_TO_RUN](	
	 [MODEL_NAME]					
	,[GROUP_NAME]					
	,[OBJECT_NAME]					
	,[OBJECT_TYPE]					
	,[SOURCE_OBJECT_PATH]			
	,[DESTINATION_OBJECT_PATH]		
	,[PARAMETERS_LIST]				
	,[MODEL_ORDER]					
	,[GROUP_ORDER]					
	,[OBJECT_ORDER]					)				
select distinct
 t1.model_name
,t1.group_name
,t3.object_name
,t4.[OBJECT_TYPE]
,t4.[SOURCE_OBJECT_PATH]
,t4.[DESTINATION_OBJECT_PATH]
,t4.[PARAMETERS_LIST]
--,t1.dependancy_model_name
--,t1.dependancy_group_name
,t2.level as [MODEL_ORDER] 
,t1.level as [GROUP_ORDER]
, t3.level as [OBJECT_ORDER]
from Group_table t1
left join Model_tabel t2
on t1.model_name=t2.model_name
left join Object_table t3 on t1.model_name=t3.model_name and t1.group_name=t3.group_name
left join  [config].[EXECUTION_LIST] t4 on
t3.Model_Name=t4.MODEL_NAME 
and t3.Group_Name=t4.GROUP_NAME 
and t3.Object_Name=t4.OBJECT_NAME
where t3.object_name is not null
-- reset attributes from execution list
--UPDATE CONFIG.EXECUTION_LIST 
--set DT_START_EXECUTION = NULL, DT_END_EXECUTION=Null, [STATUS]=NULL, DURATION=NULL, FLG_HAS_FINISHED=0,FLG_IN_EXECUTION=0, [ERROR_MESSAGE]=NULL
--FROM CONFIG.EXECUTION_LIST  T2
--INNER JOIN config.EXECUTION_LIST_TO_RUN T1 ON T1.[MODEL_NAME]=T2.[MODEL_NAME] AND T1.[GROUP_NAME]=T2.[GROUP_NAME] AND T1.[OBJECT_NAME]=T2.[OBJECT_NAME]

end