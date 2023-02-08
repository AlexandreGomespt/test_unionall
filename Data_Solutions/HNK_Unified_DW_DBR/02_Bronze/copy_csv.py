# Databricks notebook source
#Author: Nuno Lopes
#Created date: 03/01/2022
#Last update date:09/01/2022
#Last update name:Nuno Lopes
#v0.1

# COMMAND ----------

import datetime

# COMMAND ----------

#widget para selecionar ficheiro a copiar
dbutils.widgets.text("input_filename","")
input_filename=dbutils.widgets.get("input_filename")
input_filename

# COMMAND ----------

#widget para selecionar formato de output (delta/parquet)
dbutils.widgets.dropdown("Output format: delta/parquet","parquet",["delta","parquet"])
output_format=dbutils.widgets.get("Output format: delta/parquet")
output_format


# COMMAND ----------

#Ler  ficheiro csv de configuração e criar temporary view para poder usar sparkSQL (Converter em SQL table)

spark.read.format('csv').options(header='true', inferschema='true', delimiter= ';').load("/mnt/datarepository/Config_files/config.csv").createOrReplaceTempView("vw_config")

# COMMAND ----------

#Variavél config é = à linha da tabela  tempview em que o valor da primeira coluna seja o inserido no widget f"" para inserir variáveis de python na string 

config=(spark.sql(f"select * from vw_config \
where Input_filename = '{input_filename}'"))

# COMMAND ----------

#Inserir valores da variável config em novas variáveis para usar no ficheiro de output

#input_filename = config.first()['Input_filename']
input_path = config.first()['Input_file_path']
#no_columns = config.first()['Number_of_columns']
delimiter = config.first()['Delimiter']
output_filename = config.first()['Output_filename']
#output_path = config.first()['Output_file_path']
output_path = f"{config.first()['Output_file_path']}/{str(datetime.datetime.today()).split()[0].replace('-','')}"

# COMMAND ----------

#validar se campos extraidos estao comforme o esperado:
try:
    assert delimiter!=''
except:
    raise Exception("Problema encontrado na coluna delimiter")

# COMMAND ----------

#validar se campos extraidos estao comforme o esperado:
try:
    spark.read.format('csv').options(header='true', delimiter= delimiter).load(f"/mnt/datarepository/Imported_files/{input_filename}")
except:
    raise Exception("Não foi possivel ler o ficheiro")

# COMMAND ----------

#Write  em formato parquet em que o delimiter é o definido no ficheiro de configuração e o nome e o path também
#faz overwrite se já houver um ficheiro com o mesmo nome na pasta de saída

spark.read.format('csv').options(header='true', delimiter= delimiter).load(f"/mnt/datarepository/Imported_files/{input_filename}").write.mode("overwrite").format(f"{output_format}").save(f"/mnt/datarepository/{output_path}/{output_filename}")

# COMMAND ----------

df = spark.read.format('csv').options(header='true', delimiter= delimiter).load(f"/mnt/datarepository/Imported_files/{input_filename}")

number_rows_input = df.count()
number_columns_input = len(df.columns)

#write.mode("overwrite").format(f"{output_format}").save(f"/mnt/datarepository/{output_path}/{output_filename}")

# COMMAND ----------

df.write.mode("overwrite").format(f"{output_format}").save(f"/mnt/datarepository/{output_path}/{output_filename}")

# COMMAND ----------

#Criar dataframe log a comparar os números de colunas e registos

spark.sql(f"insert into  config.log_ingestion       \
select  '{input_filename}'                          \
       ,'{output_filename}'							\
       ,'{output_path}'                             \
	   ,'{number_rows_input}'                       \
	   ,'{number_columns_input}'                    \
	   , current_timestamp()"
         )


# COMMAND ----------

display(spark.read.format(f'{output_format}').load(f"/mnt/datarepository/{output_path}/{output_filename}"))

