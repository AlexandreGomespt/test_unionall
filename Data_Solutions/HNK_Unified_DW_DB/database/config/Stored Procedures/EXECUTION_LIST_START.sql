CREATE procedure [config].[EXECUTION_LIST_START](@model_name nvarchar(255),@Group_name nvarchar(255), @Object_name nvarchar(255), @Pipeline_ID nvarchar(255)) 
as
begin
update config.EXECUTION_LIST
set DT_START_EXECUTION =GETDATE(), FLG_IN_EXECUTION=1, DURATION=NULL, STATUS=NULL, PIPELINE_ID=@Pipeline_ID
where MODEL_NAME=@model_name and GROUP_NAME=@Group_name and Object_Name=@Object_name
end