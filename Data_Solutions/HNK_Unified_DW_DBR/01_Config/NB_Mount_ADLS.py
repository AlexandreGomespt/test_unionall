# Databricks notebook source
# MAGIC %run ./NB_Set_Environment

# COMMAND ----------


dir=(dbutils.secrets.get(scope="AzureKeyVault",key="dataprocessing-tenant-id"))
endpoint=f"https://login.microsoftonline.com/{dir}/oauth2/token"
configs = {"fs.azure.account.auth.type": "OAuth",
          "fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
          "fs.azure.account.oauth2.client.id": dbutils.secrets.get(scope="AzureKeyVault",key="dataprocessing-app-id"),
          "fs.azure.account.oauth2.client.secret": dbutils.secrets.get(scope="AzureKeyVault",key="dataprocessing-app-secret"),
          "fs.azure.account.oauth2.client.endpoint": endpoint}

dbutils.fs.mount(
  source = f"abfss://dls@heiaepghr01{environment}wedls01.dfs.core.windows.net/datamodel",
  mount_point = "/mnt/dls/datamodel",
  extra_configs = configs)

# COMMAND ----------

# MAGIC %md
# MAGIC dbutils.fs.mounts()
