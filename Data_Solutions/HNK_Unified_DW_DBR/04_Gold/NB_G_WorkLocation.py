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

# MAGIC %md
# MAGIC drop table  gold.dim_worklocation 

# COMMAND ----------

# MAGIC %sql
# MAGIC create table if not exists gold.dim_worklocation  (
# MAGIC SK_DIM_WORKLOCATION     BIGINT    not null
# MAGIC ,`Work Location`  		string
# MAGIC ,`Work Location ID`  	string    not null
# MAGIC , City  				string
# MAGIC ,`Type of Location`  	string
# MAGIC , Area  				string
# MAGIC , Country  				string
# MAGIC , ROW_HASH 				string
# MAGIC , DT_CREATED  			timestamp not null
# MAGIC , CREATED_BY  			string    not null
# MAGIC , DT_MODIFIED  			timestamp not null
# MAGIC , MODIFIED_BY 			string    not null)

# COMMAND ----------

max_index=spark.sql("select ifnull(max(SK_dim_worklocation),0) as index from gold.dim_worklocation").first()[0]
spark.conf.set("py_var.max_index",max_index)
max_index

# COMMAND ----------

# MAGIC %sql
# MAGIC create or replace view vw_insert as
# MAGIC select t1.*
# MAGIC ,(ROW_NUMBER () OVER (ORDER BY t1.`Work Location ID`) )+ ${py_var.max_index} as SK_DIM_WORKLOCATION
# MAGIC from silver.stg_dim_worklocation t1
# MAGIC left join gold.dim_worklocation t2
# MAGIC on t1.`Work Location ID` = t2.`Work Location ID`
# MAGIC where t2.SK_DIM_WORKLOCATION is null

# COMMAND ----------

# MAGIC %sql
# MAGIC MERGE INTO gold.dim_worklocation
# MAGIC USING silver.stg_dim_worklocation 
# MAGIC ON gold.dim_worklocation.`Work Location ID` = silver.stg_dim_worklocation.`Work Location ID`
# MAGIC WHEN MATCHED  and gold.dim_worklocation.ROW_HASH <> silver.stg_dim_worklocation.ROW_HASH THEN
# MAGIC   UPDATE SET
# MAGIC 			 `Work Location`      = silver.stg_dim_worklocation.`Work Location`
# MAGIC 			,`Work Location ID`   = silver.stg_dim_worklocation.`Work Location ID`
# MAGIC 			,`City`               = silver.stg_dim_worklocation.`City`  
# MAGIC 			,`Type of Location`   = silver.stg_dim_worklocation.`Type of Location`
# MAGIC 			,Area                 = silver.stg_dim_worklocation.Area
# MAGIC 			,Country              = silver.stg_dim_worklocation.Country 
# MAGIC             ,DT_MODIFIED          = current_timestamp()
# MAGIC             ,MODIFIED_BY          = 'Databricks'
# MAGIC             ,ROW_HASH             = sha2(concat(ifnull(silver.stg_dim_worklocation.`Work Location`,'')
# MAGIC 											   ,ifnull(silver.stg_dim_worklocation.`Work Location ID`,'')
# MAGIC 											   ,ifnull(silver.stg_dim_worklocation.`City`,'')
# MAGIC 											   ,ifnull(silver.stg_dim_worklocation.`Type of Location`,'')
# MAGIC 											   ,ifnull(silver.stg_dim_worklocation.Area,'')
# MAGIC 											   ,ifnull(silver.stg_dim_worklocation.Country,'')
# MAGIC 											   ),256)

# COMMAND ----------

# MAGIC %sql
# MAGIC MERGE INTO gold.dim_worklocation
# MAGIC USING vw_insert 
# MAGIC ON gold.dim_worklocation.SK_DIM_WORKLOCATION = vw_insert.SK_DIM_WORKLOCATION 
# MAGIC WHEN NOT MATCHED
# MAGIC   THEN INSERT (  SK_DIM_WORKLOCATION
# MAGIC                 ,`Work Location`  		
# MAGIC 			    ,`Work Location ID`  	
# MAGIC 			    , City  				
# MAGIC 			    ,`Type of Location`  	
# MAGIC 			    , Area  				
# MAGIC 			    , Country  				
# MAGIC 			    , ROW_HASH 				
# MAGIC 			    , DT_CREATED  			
# MAGIC 			    , CREATED_BY  			
# MAGIC 			    , DT_MODIFIED  			
# MAGIC 			    , MODIFIED_BY 	 			        
# MAGIC 				
# MAGIC   )
# MAGIC VALUES (
# MAGIC     vw_insert.SK_DIM_WORKLOCATION
# MAGIC    ,vw_insert.`Work Location`  		
# MAGIC    ,vw_insert.`Work Location ID`  	
# MAGIC    ,vw_insert.City  				
# MAGIC    ,vw_insert.`Type of Location`  	
# MAGIC    ,vw_insert.Area  				
# MAGIC    ,vw_insert.Country  				
# MAGIC    ,vw_insert.ROW_HASH 	
# MAGIC    ,current_timestamp()
# MAGIC    ,'Databricks'
# MAGIC    ,current_timestamp()
# MAGIC    ,'Databricks'
# MAGIC   )

# COMMAND ----------

spark.sql("select count(*) from gold.dim_worklocation").show()
