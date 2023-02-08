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

dbutils.widgets.text("DESTINATION_TABLE_NAME","")
destination_table=dbutils.widgets.get("DESTINATION_TABLE_NAME")

# COMMAND ----------

# MAGIC %run ../01_Config/NB_Mount_DB

# COMMAND ----------

DF=spark.read.format("jdbc").option("url",jdbcUrl).option("query",  f"SELECT *  FROM [config].[CONFIG_FILE] where DESTIONATION_TABLE_NAME = '{destination_table}' ").load()#query("Select * from config.CONFIG_FILE")

#option("dbtable","config.CONFIG_FILE").filter("INPUT_FILE_NAME"=="DIM_WorkLocation.csv")

# COMMAND ----------

display(DF)

# COMMAND ----------

(spark.read.option("header","true").option("quote", "\"").option("escape", "\"").option("delimiter",DF.first()['DELIMITER']).csv(f"/mnt/dls/datamodel/{DF.first()['INPUT_FILE_PATH']}/{DF.first()['INPUT_FILENAME']}")
.withColumn("DT_CREATED",current_timestamp())
.withColumn("CREATED_BY",lit("Databricks"))
.withColumn("DT_MODIFIED",current_timestamp())
.withColumn("MODIFIED_BY",lit("Databricks"))
.write.mode('overwrite')
.saveAsTable(f"bronze.{destination_table}"))

# COMMAND ----------

spark.sql(f"select count(*) from bronze.{destination_table}").show()
