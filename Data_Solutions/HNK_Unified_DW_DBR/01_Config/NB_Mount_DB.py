# Databricks notebook source
# MAGIC %run ./NB_Set_Environment

# COMMAND ----------

# MAGIC %md
# MAGIC sql_pw=dbutils.secrets.get(scope="SecretScope",key="secret-pass-sql-sgfundos")
# MAGIC sql_user=dbutils.secrets.get(scope="SecretScope",key="secret-user-sql-sgfundos")
# MAGIC sql_servername=dbutils.secrets.get(scope="SecretScope",key="secret-servername-sql-sgfundos")

# COMMAND ----------

jdbcHostname="sql-dev-unified-model.database.windows.net"
jdbcPort=1433
jdbcDatabase="DEV_01_HNK_Unified"
jdbcUsername="SQL_Admin"
jdbcPassword="7032Zup0!sAa"
jdbcDriver="com.microsoft.sqlserver.jdbc.SQLServerDriver"

jdbcUrl = f"jdbc:sqlserver://{jdbcHostname}:{jdbcPort};databaseName={jdbcDatabase};user={jdbcUsername};password={jdbcPassword};encrypt=true;loginTimeout=30";

# COMMAND ----------

# MAGIC %md
# MAGIC spark.read.format("jdbc").option("url",jdbcUrl).option("dbtable","config.CONFIG_FILE").load().show()

# COMMAND ----------

# MAGIC %md
# MAGIC dbutils.fs.mounts()
