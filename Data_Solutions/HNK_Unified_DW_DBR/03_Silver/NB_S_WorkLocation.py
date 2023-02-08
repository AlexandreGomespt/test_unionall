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
# MAGIC -- remove duplicates
# MAGIC create or replace view vw_worklocation as 
# MAGIC 
# MAGIC select * from (
# MAGIC select          `Work Location`
# MAGIC 				,`Work Location ID`
# MAGIC 				,`City`
# MAGIC 				,`Type of Location`
# MAGIC 				,Area
# MAGIC 				,Country 
# MAGIC                 ,ROW_NUMBER () OVER (partition by `Work Location ID` ORDER BY `Work Location`, `City`, `Type of Location`) as row_n
# MAGIC                 from bronze.dim_worklocation)
# MAGIC                 as t1
# MAGIC where t1.row_n=1

# COMMAND ----------

# MAGIC %sql
# MAGIC create or replace table silver.stg_dim_worklocation as
# MAGIC select          `Work Location`
# MAGIC 				,`Work Location ID`
# MAGIC 				,`City`
# MAGIC 				,`Type of Location`
# MAGIC 				,Area
# MAGIC 				,Country 
# MAGIC                 ,sha2(concat( ifnull(`Work Location`,'')
# MAGIC 							 ,ifnull(`Work Location ID`,'')
# MAGIC 							 ,ifnull(`City`,'')
# MAGIC 							 ,ifnull(`Type of Location`,'')
# MAGIC 							 ,ifnull(Area,'')
# MAGIC 							 ,ifnull(Country,'')
# MAGIC 							 )
# MAGIC 					 ,256) as ROW_HASH
# MAGIC                 ,current_timestamp() as DT_CREATED
# MAGIC                 ,'Databricks' as CREATED_BY
# MAGIC                 ,current_timestamp() as DT_MODIFIED
# MAGIC                 ,'Databricks' as MODIFIED_BY
# MAGIC from vw_worklocation
# MAGIC where `Work Location ID` is not null
# MAGIC -- drop null ID

# COMMAND ----------

spark.sql("select count(*) from silver.stg_dim_worklocation").show()
