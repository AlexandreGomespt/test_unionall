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
# MAGIC drop table gold.dim_opco_le

# COMMAND ----------

# MAGIC %sql
# MAGIC create table if not exists gold.dim_opco_le (
# MAGIC SK_DIM_OPCO_LE     BIGINT not null  
# MAGIC --GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1)
# MAGIC ,`LE (ID)`					string
# MAGIC ,`LE ID`                    string not null
# MAGIC ,`Legal Entity Key`         string
# MAGIC ,`Legal Entity Name`        string
# MAGIC ,`RE ID`                    string
# MAGIC ,`Reporting Entity Name`    string
# MAGIC ,`OpCo ID`                  string
# MAGIC , OpCo                      string
# MAGIC , Country                   string
# MAGIC , Region                    string
# MAGIC , Wave                      string
# MAGIC ,`Technical Key`            string
# MAGIC ,`Go Live Date`             string
# MAGIC ,`OpCo Nationality`         string
# MAGIC ,`Regional Nationality`     string
# MAGIC ,`OpCo Cons Group`          string
# MAGIC , ROW_HASH 					string	  not null
# MAGIC , DT_START                  timestamp not null
# MAGIC , DT_END                    timestamp
# MAGIC , DT_CREATED  				timestamp not null
# MAGIC , CREATED_BY  				string    not null
# MAGIC , DT_MODIFIED  				timestamp not null
# MAGIC , MODIFIED_BY 				string    not null)

# COMMAND ----------

# MAGIC %md
# MAGIC update silver.stg_dim_opco_le 
# MAGIC set  `Legal Entity Key`  ='n321unoo312', row_hash=hash('nun321oo123')
# MAGIC where `LE ID` in ('ATCT','BRUU') 

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE VIEW vw_update_end_date as
# MAGIC SELECT 		 t1.*
# MAGIC 			,t2.SK_DIM_OPCO_LE 
# MAGIC             
# MAGIC 			FROM silver.stg_dim_opco_le t1
# MAGIC 			LEFT JOIN (SELECT * FROM  gold.dim_opco_le 
# MAGIC 									WHERE DT_END IS NULL) AS t2 
# MAGIC 			ON t1.`LE ID` = t2.`LE ID` 
# MAGIC 			WHERE t1.row_hash <> t2.row_hash 

# COMMAND ----------

# MAGIC %sql
# MAGIC MERGE INTO gold.dim_opco_le
# MAGIC USING vw_update_end_date 
# MAGIC ON gold.dim_opco_le.SK_DIM_OPCO_LE = vw_update_end_date.SK_DIM_OPCO_LE 
# MAGIC WHEN MATCHED  THEN
# MAGIC   UPDATE SET
# MAGIC 			 DT_END      = current_timestamp()
# MAGIC             ,DT_MODIFIED = current_timestamp()
# MAGIC             ,MODIFIED_BY = 'Databricks'

# COMMAND ----------

max_index=spark.sql("select ifnull(max(SK_DIM_OPCO_LE),0) as index from gold.dim_opco_le").first()[0]
spark.conf.set("py_var.max_index",max_index)
max_index

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE VIEW vw_insert AS
# MAGIC SELECT 	  t1.*
# MAGIC 		, NULL as SK_DIM_OPCO_LE
# MAGIC 		, (ROW_NUMBER () OVER (ORDER BY t1.`LE ID`) )+ ${py_var.max_index} as id
# MAGIC FROM silver.stg_dim_opco_le t1
# MAGIC LEFT JOIN (SELECT * FROM  gold.dim_opco_le  
# MAGIC 					WHERE DT_END IS NULL) as t2 
# MAGIC 		ON t1.`LE ID` = t2.`LE ID` 
# MAGIC 
# MAGIC 		WHERE t2.SK_DIM_OPCO_LE IS NULL  OR t1.row_hash <> t2.row_hash

# COMMAND ----------

# MAGIC %sql
# MAGIC MERGE INTO gold.dim_opco_le
# MAGIC USING vw_insert 
# MAGIC ON gold.dim_opco_le.SK_DIM_OPCO_LE = vw_insert.SK_DIM_OPCO_LE 
# MAGIC WHEN NOT MATCHED
# MAGIC   THEN INSERT (   SK_DIM_OPCO_LE
# MAGIC                 ,`LE (ID)`					
# MAGIC 				,`LE ID`                    
# MAGIC 				,`Legal Entity Key`         
# MAGIC 				,`Legal Entity Name`        
# MAGIC 				,`RE ID`                    
# MAGIC 				,`Reporting Entity Name`    
# MAGIC 				,`OpCo ID`                  
# MAGIC 				, OpCo                      
# MAGIC 				, Country                   
# MAGIC 				, Region                    
# MAGIC 				, Wave                      
# MAGIC 				,`Technical Key`            
# MAGIC 				,`Go Live Date`             
# MAGIC 				,`OpCo Nationality`         
# MAGIC 				,`Regional Nationality`     
# MAGIC 				,`OpCo Cons Group`          
# MAGIC 				, ROW_HASH 
# MAGIC                 ,DT_START
# MAGIC                 ,DT_CREATED  			
# MAGIC                 ,CREATED_BY  			
# MAGIC                 ,DT_MODIFIED  			
# MAGIC                 ,MODIFIED_BY 				
# MAGIC   )
# MAGIC VALUES (
# MAGIC     vw_insert.ID
# MAGIC    ,vw_insert.`LE (ID)`					
# MAGIC    ,vw_insert.`LE ID`                    
# MAGIC    ,vw_insert.`Legal Entity Key`         
# MAGIC    ,vw_insert.`Legal Entity Name`        
# MAGIC    ,vw_insert.`RE ID`                    
# MAGIC    ,vw_insert.`Reporting Entity Name`    
# MAGIC    ,vw_insert.`OpCo ID`                  
# MAGIC    ,vw_insert.OpCo                      
# MAGIC    ,vw_insert.Country                   
# MAGIC    ,vw_insert.Region                    
# MAGIC    ,vw_insert.Wave                      
# MAGIC    ,vw_insert.`Technical Key`            
# MAGIC    ,vw_insert.`Go Live Date`             
# MAGIC    ,vw_insert.`OpCo Nationality`         
# MAGIC    ,vw_insert.`Regional Nationality`     
# MAGIC    ,vw_insert.`OpCo Cons Group`          
# MAGIC    ,vw_insert.ROW_HASH 
# MAGIC    ,current_timestamp()
# MAGIC    ,current_timestamp()
# MAGIC    ,'Databricks'
# MAGIC    ,current_timestamp()
# MAGIC    ,'Databricks'
# MAGIC   )

# COMMAND ----------

spark.sql("select count(*) from gold.dim_opco_le").show()
