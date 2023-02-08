# Databricks notebook source
# MAGIC %sql
# MAGIC CREATE SCHEMA if not exists temporary location '/mnt/dls/datamodel/datalake_db/temporary';
# MAGIC CREATE SCHEMA if not exists bronze    location '/mnt/dls/datamodel/datalake_db/bronze';
# MAGIC CREATE SCHEMA if not exists silver    location '/mnt/dls/datamodel/datalake_db/silver';
# MAGIC CREATE SCHEMA if not exists gold      location '/mnt/dls/datamodel/datalake_db/gold';
