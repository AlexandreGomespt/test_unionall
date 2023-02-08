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

# MAGIC %run ../01_Config/NB_Mount_DB

# COMMAND ----------

DF=spark.read.format("jdbc").option("url",jdbcUrl).option("query",  "SELECT *  FROM [config].[CONFIG_FILE] where INPUT_FILENAME = 'DIM_WorkLocation.csv' ").load()#query("Select * from config.CONFIG_FILE")

#option("dbtable","config.CONFIG_FILE").filter("INPUT_FILE_NAME"=="DIM_WorkLocation.csv")

# COMMAND ----------

(spark.read.option("header","true").option("delimiter",DF.first()['DELIMITER']).csv(f"/mnt/dls/datamodel/{DF.first()['INPUT_FILE_PATH']}/DIM_WorkLocation.csv")
.withColumn("DT_CREATED",current_timestamp())
.withColumn("CREATED_BY",lit("Databricks"))
.withColumn("DT_MODIFIED",current_timestamp())
.withColumn("MODIFIED_BY",lit("Databricks"))
.write.mode('overwrite')
.saveAsTable("bronze.DIM_WORKLOCATION"))

# COMMAND ----------

spark.sql("select count(*) from bronze.DIM_WORKLOCATION ").show()
