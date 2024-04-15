#!/usr/bin/env python
# coding: utf-8

# ## synapse spark
# 
# 
# 

# In[2]:


get_ipython().run_cell_magic('pyspark', '', "df = spark.read.load('abfss://files@datalakep9t0bu7.dfs.core.windows.net/sales/orders/*.csv', format='csv'\r\n## If\u202fheader\u202fexists\u202funcomment\u202fline\u202fbelow\r\n##, header=True\r\n)\r\ndisplay(df.limit(100))\n")


# In[3]:


get_ipython().run_cell_magic('pyspark', '', 'from pyspark.sql.types import *\r\nfrom pyspark.sql.functions import *\r\n\r\norderSchema = StructType([\r\n    StructField("SalesOrderNumber", StringType()),\r\n    StructField("SalesOrderLineNumber", IntegerType()),\r\n    StructField("OrderDate", DateType()),\r\n    StructField("CustomerName", StringType()),\r\n    StructField("Email", StringType()),\r\n    StructField("Item", StringType()),\r\n    StructField("Quantity", IntegerType()),\r\n    StructField("UnitPrice", FloatType()),\r\n    StructField("Tax", FloatType())\r\n    ])\r\n\r\ndf = spark.read.load(\'abfss://files@datalakep9t0bu7.dfs.core.windows.net/sales/orders/*.csv\', format=\'csv\', schema=orderSchema)\r\ndisplay(df.limit(100))\n')


# In[4]:


df.printSchema()


# In[10]:


customers = df['CustomerName', 'Email']
print(customers.count())
print(customers.distinct().count())
display(customers.distinct())


# In[11]:


customers = df.select("CustomerName", "Email").where(df['Item']=='Road-250 Red, 52')
print(customers.count())
print(customers.distinct().count())
display(customers.distinct())


# In[12]:


productSales = df.select("Item", "Quantity").groupBy("Item").sum()
display(productSales)


# In[13]:


yearlySales = df.select(year("OrderDate").alias("Year")).groupBy("Year").count().orderBy("Year")
display(yearlySales)


# In[14]:


df.createOrReplaceTempView("salesorders")

spark_df = spark.sql("SELECT * FROM salesorders")
display(spark_df)


# In[15]:


get_ipython().run_cell_magic('sql', '', 'SELECT YEAR(OrderDate) AS OrderYear,\r\n       SUM((UnitPrice * Quantity) + Tax) AS GrossRevenue\r\nFROM salesorders\r\nGROUP BY YEAR(OrderDate)\r\nORDER BY OrderYear;\n')


# In[18]:


get_ipython().run_cell_magic('sql', '', 'SELECT * FROM salesorders\n')


# In[19]:


sqlQuery = "SELECT CAST(YEAR(OrderDate) AS CHAR(4)) AS OrderYear, \
                SUM((UnitPrice * Quantity) + Tax) AS GrossRevenue \
            FROM salesorders \
            GROUP BY CAST(YEAR(OrderDate) AS CHAR(4)) \
            ORDER BY OrderYear"
df_spark = spark.sql(sqlQuery)
df_spark.show()


# In[20]:


from matplotlib import pyplot as plt

# matplotlib requires a Pandas dataframe, not a Spark one
df_sales = df_spark.toPandas()

# Create a bar plot of revenue by year
plt.bar(x=df_sales['OrderYear'], height=df_sales['GrossRevenue'])

# Display the plot
plt.show()


# In[23]:


# Clear the plot area
plt.clf()

# Create a bar plot of revenue by year
plt.bar(x=df_sales['OrderYear'], height=df_sales['GrossRevenue'], color='orange')

# Customize the chart
plt.title('Revenue by Year')
plt.xlabel('Year')
plt.ylabel('Revenue')
plt.grid(color='#95a5a6', linestyle='--', linewidth=2, axis='y', alpha=0.7)
plt.xticks(rotation=45)

# Show the figure
plt.show()


# In[24]:


# Clear the plot area
plt.clf()

# Create a Figure
fig = plt.figure(figsize=(8,3))

# Create a bar plot of revenue by year
plt.bar(x=df_sales['OrderYear'], height=df_sales['GrossRevenue'], color='orange')

# Customize the chart
plt.title('Revenue by Year')
plt.xlabel('Year')
plt.ylabel('Revenue')
plt.grid(color='#95a5a6', linestyle='--', linewidth=2, axis='y', alpha=0.7)
plt.xticks(rotation=45)

# Show the figure
plt.show()


# In[25]:


# Clear the plot area
plt.clf()

# Create a figure for 2 subplots (1 row, 2 columns)
fig, ax = plt.subplots(1, 2, figsize = (10,4))

# Create a bar plot of revenue by year on the first axis
ax[0].bar(x=df_sales['OrderYear'], height=df_sales['GrossRevenue'], color='orange')
ax[0].set_title('Revenue by Year')

# Create a pie chart of yearly order counts on the second axis
yearly_counts = df_sales['OrderYear'].value_counts()
ax[1].pie(yearly_counts)
ax[1].set_title('Orders per Year')
ax[1].legend(yearly_counts.keys().tolist())

# Add a title to the Figure
fig.suptitle('Sales Data')

# Show the figure
plt.show()


# In[26]:


import seaborn as sns

# Clear the plot area
plt.clf()

# Create a bar chart
ax = sns.barplot(x="OrderYear", y="GrossRevenue", data=df_sales)
plt.show()


# In[27]:


import seaborn as sns

# Clear the plot area
plt.clf()

# Create a bar chart
ax = sns.barplot(x="OrderYear", y="GrossRevenue", data=df_sales)
plt.show()


# In[28]:


# Clear the plot area
plt.clf()

# Set the visual theme for seaborn
sns.set_theme(style="whitegrid")

# Create a bar chart
ax = sns.barplot(x="OrderYear", y="GrossRevenue", data=df_sales)
plt.show()

