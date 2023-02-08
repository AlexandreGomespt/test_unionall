  CREATE procedure [config].[SP_CHECK_EXTRACTION_STATUS_END] (@model_name nvarchar(255), @pipeline_id nvarchar(255), @FLG_SUCCESS nvarchar(255))as
  begin 
	declare @DT_END_EXECUTION datetime = getdate();
	declare @dt_next datetime;
	declare @periodicity nvarchar(255) ;

	update [config].[CHECK_EXTRACTION_STATUS]
	set DT_END_EXECUTION=@DT_END_EXECUTION, FLG_SUCCESS=@FLG_SUCCESS
	where [MODEL_NAME]=@model_name and [PIPELINE_ID]=@pipeline_id



    set @periodicity=(SELECT[PERIODICITY]

	FROM [config].[CONFIG_MODEL]
	where MODEL_NAME=@model_name)

	if @FLG_SUCCESS=1
	begin
			if @periodicity='Daily'
				begin
					set @dt_next = (select DATEADD(DAY, 1, try_convert(date,@DT_END_EXECUTION,23)))
				end
  
			else if @periodicity='Monthly'
				begin
					 set @dt_next = (select DATEADD(MONTH, 1, try_convert(date,@DT_END_EXECUTION,23)))
				end




			update [config].[CONFIG_MODEL]
			set [DT_LAST_SUCCESS_EXECUTION]=@DT_END_EXECUTION,  [DT_NEXT_EXECUTION]=@dt_next
			where [MODEL_NAME]=@model_name
	end

  end