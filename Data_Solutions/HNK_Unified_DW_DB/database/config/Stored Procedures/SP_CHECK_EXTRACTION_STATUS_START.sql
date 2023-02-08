  create procedure config.SP_CHECK_EXTRACTION_STATUS_START (@model_name nvarchar(255), @pipeline_id nvarchar(255))as
  begin 
  declare @periodicity nvarchar(255);

  set @periodicity = (select PERIODICITY from config.CONFIG_MODEL
						where MODEL_NAME=@model_name)

  insert into [config].[CHECK_EXTRACTION_STATUS]([MODEL_NAME],[PERIODICITY],[DT_START_EXECUTION],[PIPELINE_ID])
  values(@model_name,@periodicity,GETDATE(),@pipeline_id)



  end