# Databricks notebook source
sqlContext.clearCache()
#from pyspark.sql.functions import monotonically_increasing_id
from pyspark.sql.functions import *
spark.conf.set("spark.databricks.optimizer.dynamicPartitionPruning","true")
spark.conf.set("spark.databricks.delta.properties.defaults.autoOptimize.optimizeWrite","true")
spark.conf.set("spark.databricks.delta.properties.defaults.autoOptimize.autoCompact","true")

# COMMAND ----------

spark.conf.set("spark.databricks.delta.properties.defaults.minWriterVersion" , "5") 
spark.conf.set("spark.databricks.delta.properties.defaults.minReaderVersion" , "2") 
spark.conf.set("spark.databricks.delta.properties.defaults.columnMapping.mode" , "name") 

# COMMAND ----------

# MAGIC %sql
# MAGIC create or replace view vw_dim_opco_le as 
# MAGIC select   `LE (ID)`
# MAGIC 		,`LE ID`
# MAGIC 		,`Legal Entity Key`
# MAGIC 		,`Legal Entity Name`
# MAGIC 		,`RE ID`
# MAGIC 		,`Reporting Entity Name`
# MAGIC 		,`OpCo ID`
# MAGIC 		, OpCo
# MAGIC 		, Country
# MAGIC 		, Region
# MAGIC 		, Wave
# MAGIC 		,`Technical Key`
# MAGIC 		,`Go Live Date`
# MAGIC 		,`OpCo Nationality`
# MAGIC 		,`Regional Nationality`
# MAGIC 		,`OpCo Cons Group` 
# MAGIC         from (
# MAGIC 				select 
# MAGIC 						`LE (ID)`
# MAGIC 						,`LE ID`
# MAGIC 						,`Legal Entity Key`
# MAGIC 						,`Legal Entity Name`
# MAGIC 						,`RE ID`
# MAGIC 						,`Reporting Entity Name`
# MAGIC 						,`OpCo ID`
# MAGIC 						, OpCo
# MAGIC 						, Country
# MAGIC 						, Region
# MAGIC 						, Wave
# MAGIC 						,`Technical Key`
# MAGIC 						,`Go Live Date`
# MAGIC 						,`OpCo Nationality`
# MAGIC 						,`Regional Nationality`
# MAGIC 						,`OpCo Cons Group` 
# MAGIC 						,ROW_NUMBER () OVER (partition by `LE ID` ORDER BY `Legal Entity Key` ,`Legal Entity Name` ) as row_n
# MAGIC 				from bronze.dim_opco_le
# MAGIC 				where `LE ID` is not null) as t1
# MAGIC 				where t1.row_n=1 

# COMMAND ----------

# MAGIC %sql
# MAGIC create or replace table silver.stg_dim_opco_le as
# MAGIC select   `LE (ID)`
# MAGIC 		,`LE ID`
# MAGIC 		,`Legal Entity Key`
# MAGIC 		,`Legal Entity Name`
# MAGIC 		,`RE ID`
# MAGIC 		,`Reporting Entity Name`
# MAGIC 		,`OpCo ID`
# MAGIC 		, OpCo
# MAGIC 		, Country
# MAGIC 		, Region
# MAGIC 		, Wave
# MAGIC 		,`Technical Key`
# MAGIC 		,`Go Live Date`
# MAGIC 		,`OpCo Nationality`
# MAGIC 		,`Regional Nationality`
# MAGIC 		,`OpCo Cons Group`
# MAGIC         ,sha2(concat(ifnull(`Legal Entity Key`,'')
# MAGIC 					,ifnull(`Legal Entity Name`,'')
# MAGIC 					,ifnull(`RE ID`,'')
# MAGIC 					,ifnull(`Reporting Entity Name`,'')
# MAGIC 					,ifnull(`OpCo ID`,'')
# MAGIC 					,ifnull( OpCo,'')
# MAGIC 					,ifnull( Country,'')
# MAGIC 					,ifnull( Region,'')
# MAGIC 					,ifnull( Wave,'')
# MAGIC 					,ifnull(`Technical Key`,'')
# MAGIC 					,ifnull(`Go Live Date`,'')
# MAGIC 					,ifnull(`OpCo Nationality`,'')
# MAGIC 					,ifnull(`Regional Nationality`,'')
# MAGIC 					,ifnull(`OpCo Cons Group`,'')
# MAGIC 					 )
# MAGIC 					 ,256) as ROW_HASH
# MAGIC         ,current_timestamp() as DT_CREATED
# MAGIC         ,'Databricks' as CREATED_BY
# MAGIC         ,current_timestamp() as DT_MODIFIED
# MAGIC         ,'Databricks' as MODIFIED_BY
# MAGIC         from vw_dim_opco_le

# COMMAND ----------

spark.sql("select count(*) from silver.stg_dim_opco_le").show()
