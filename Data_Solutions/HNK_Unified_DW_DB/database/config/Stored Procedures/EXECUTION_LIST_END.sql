
CREATE procedure [config].[EXECUTION_LIST_END](@model_name nvarchar(255),@Group_name nvarchar(255), @Object_name nvarchar(255), @Status nvarchar(255), @ErrorMessage nvarchar(500) =NULL) 
as
begin
DECLARE @datetimevar datetime;
SET   @datetimevar=getdate();

update config.EXECUTION_LIST
set DT_END_EXECUTION =@datetimevar, FLG_IN_EXECUTION=0, FLG_HAS_FINISHED=1,STATUS=@Status, DURATION=convert(float,DATEDIFF(SECOND, DT_START_EXECUTION, @datetimevar)/60.0), [ERROR_MESSAGE]=@ErrorMessage
where MODEL_NAME=@model_name and GROUP_NAME=@Group_name and Object_Name=@Object_name
end


INSERT INTO [config].[EXECUTION_LIST_HIST]( [MODEL_NAME]
      ,[GROUP_NAME]
      ,[OBJECT_NAME]
      ,[OBJECT_TYPE]
      ,[SOURCE_OBJECT_PATH]
      ,[DESTINATION_OBJECT_PATH]
      ,[PERIODICITY]
      ,[PARAMETERS_LIST]
      ,[DT_START_EXECUTION]
      ,[DT_END_EXECUTION]
      ,[FLG_IN_EXECUTION]
      ,[FLG_HAS_FINISHED]
      ,[FLG_IS_ACTIVE]
      ,[DURATION]
      ,[STATUS]
      ,[ERROR_MESSAGE]
      ,[PIPELINE_ID]
      ,[DT_CREATED]
      ,[CREATED_BY]
      ,[DT_MODIFIED]
      ,[MODIFIED_BY])
SELECT [MODEL_NAME]
      ,[GROUP_NAME]
      ,[OBJECT_NAME]
      ,[OBJECT_TYPE]
      ,[SOURCE_OBJECT_PATH]
      ,[DESTINATION_OBJECT_PATH]
      ,[PERIODICITY]
      ,[PARAMETERS_LIST]
      ,[DT_START_EXECUTION]
      ,[DT_END_EXECUTION]
      ,[FLG_IN_EXECUTION]
      ,[FLG_HAS_FINISHED]
      ,[FLG_IS_ACTIVE]
      ,[DURATION]
      ,[STATUS]
      ,[ERROR_MESSAGE]
      ,[PIPELINE_ID]
      ,[DT_CREATED]
      ,[CREATED_BY]
      ,[DT_MODIFIED]
      ,[MODIFIED_BY]
  FROM [config].[EXECUTION_LIST]
  WHERE MODEL_NAME=@model_name and GROUP_NAME=@Group_name and Object_Name=@Object_name
--declare @date1 as datetime,
--@date2 as datetime;
--SET @date1 = '2010-10-11 12:15:35', @date2 = '2010-10-10 00:00:00';
--
--SELECT convert(float,DATEDIFF(SECOND, DT_START_EXECUTION, DT_END_EXECUTION)/60.0) AS difference
--from config.EXECUTION_LIST