from django.shortcuts import  render,redirect
from django.views import View


# from pyspark.sql import SparkSession, Row
# from pyspark.sql.types import *
from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()

def pyspark_parser(View,file_name, account_name, container_name, relative_path):
    # account_name = "parserdatalake"
    # container_name = "parserfs"
    # relative_path = ""
    adls_path = 'abfss://%s@%s.dfs.core.windows.net/%s' % (container_name, account_name, relative_path)

    df_pyspark = spark.read.csv(adls_path + file_name, header=True, inferSchema=True)
    df_pyspark.show()
    name_list = df_pyspark.select("Name")
    name_array = [str(row.Name) for row in name_list.collect()]
    new_dictionary = {};
    for x in name_array:
        if x[0] == x.split("@")[1][0]:
            new_dictionary[x] = "100% Compliant"
        else:
            new_dictionary[x] = "0% Compliant"
    compliancy_csv = list(map(list, new_dictionary.items()))
    new_df_pyspark = spark.createDataFrame(compliancy_csv, ["Name", "Compliance Result"]).show()
    return new_df_pyspark


pyspark_parser("file_name","account_name", "container_name", "relative_path")