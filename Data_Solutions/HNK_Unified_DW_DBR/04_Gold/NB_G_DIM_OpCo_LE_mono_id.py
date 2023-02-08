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
# MAGIC set  `Legal Entity Key`  ='nunoo', row_hash=hash('nunoo')
# MAGIC where `LE ID` in ('ATCT','BRUU') 

# COMMAND ----------

# MAGIC %sql
# MAGIC create or replace view vw_update_end_date as
# MAGIC select t1.*, t2.SK_DIM_OPCO_LE 
# MAGIC from silver.stg_dim_opco_le t1
# MAGIC left join (select * from  gold.dim_opco_le  where DT_END is null) as t2 
# MAGIC on t1.`LE ID` = t2.`LE ID` 
# MAGIC where t1.row_hash <> t2.row_hash 

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from vw_update_end_date

# COMMAND ----------

# MAGIC %sql
# MAGIC MERGE INTO gold.dim_opco_le
# MAGIC USING vw_update_end_date 
# MAGIC ON gold.dim_opco_le.SK_DIM_OPCO_LE = vw_update_end_date.SK_DIM_OPCO_LE 
# MAGIC WHEN MATCHED  THEN
# MAGIC   UPDATE SET
# MAGIC 			 DT_END      = current_timestamp()

# COMMAND ----------

# MAGIC %sql
# MAGIC create or replace view vw_insert as
# MAGIC select t1.*, NULL as SK_DIM_OPCO_LE
# MAGIC ,(select ifnull(max(SK_DIM_OPCO_LE),0)+1 from gold.dim_opco_le )+monotonically_increasing_id() as Id 
# MAGIC 
# MAGIC from silver.stg_dim_opco_le t1
# MAGIC left join (select * from  gold.dim_opco_le  where DT_END is null) as t2 
# MAGIC on t1.`LE ID` = t2.`LE ID` 
# MAGIC where t2.SK_DIM_OPCO_LE is null  or t1.row_hash <> t2.row_hash

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from  vw_insert

# COMMAND ----------

# MAGIC %md
# MAGIC insert into gold.dim_opco_le (
# MAGIC                  `LE (ID)`					
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
# MAGIC                 ,MODIFIED_BY )
# MAGIC select   vw_insert.`LE (ID)`					
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
# MAGIC    ,'Databricks' from vw_insert

# COMMAND ----------

# MAGIC %sql
# MAGIC MERGE INTO gold.dim_opco_le
# MAGIC USING vw_insert 
# MAGIC ON gold.dim_opco_le.SK_DIM_OPCO_LE = vw_insert.SK_DIM_OPCO_LE 
# MAGIC WHEN NOT MATCHED
# MAGIC   THEN INSERT ( SK_DIM_OPCO_LE
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

# MAGIC %sql
# MAGIC select * from gold.dim_opco_le

# COMMAND ----------

spark.sql("select count(*) from gold.dim_worklocation").show()
