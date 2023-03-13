import pandas as pd, seaborn as sns
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 800)
df = pd.read_csv("persona.csv")
df.head()
df.shape
df.nunique()
df.columns = df.columns.str.lower()
df.head()
df.info()
df.describe().T
#2.
df["source"].nunique()
df["source"].value_counts()
df.source

#3.
df["price"].nunique()
df["price"].value_counts()
pd.DataFrame(df.groupby("price").agg({"price": ["count", "sum", "mean"]}))

#4.
df.groupby("price").agg({"price" : ["count","sum"]})
df["price"].value_counts()
#5.
df["country"].value_counts()
#6
df.groupby("country").agg({"price" : ["sum", "count"]})
df.pivot_table("price", "country", aggfunc=["sum", "count"])

#7.
df.groupby("source").agg({"price" : ["count", "sum"]})
df.pivot_table("price", "source", aggfunc=["count", "sum"])

#8.
df.groupby("country").agg({"price" : ["sum", "count", "mean"]})
df.pivot_table("price", "country", aggfunc=["sum", "count", "mean"])

#9.
df.groupby("source").agg({"price": ["mean", "sum", "count"]})
df.pivot_table("price", "source", aggfunc=["mean", "sum", "count"])

#10.
df.groupby(["country", "source"]).agg({"price": ["mean", "sum", "count"]}).sort_values(by=('price', 'count'), ascending=False)
df.pivot_table("price", ["country", "source"], aggfunc="mean")
df.groupby(["country", "source"]).agg({"price": "mean"})
#11.
df.groupby(["country", "source", "sex", "age"])["price"].mean()
df.groupby(["country", "source", "sex", "age"]).agg({"price": "mean"})
df.pivot_table("price", ["country", "source", "sex", "age"],aggfunc="mean")

#görev3
agg_df = df.pivot_table("price", ["country", "source", "sex", "age"],aggfunc="mean").sort_values(by="price", ascending=False)

agg_df = agg_df.reset_index()
agg_df.head(20)

agg_df["age_cat"] = pd.cut(agg_df["age"], bins=[0, 18, 23, 30, 40, agg_df["age"].max()], labels=["0_18", "19_23", "24_30","31_40", "41_70"])
# customer level based

degerler = agg_df.values
agg_df["customer_level_based"] = [row[0].upper() + "_" + row[1].upper() + "_" + row[2].upper() + "_" + row[5] for row in agg_df.values]
agg_df.head()

agg_df["customer_level_based"] = agg_df["country"].str.upper() + "_" + agg_df["source"].str.upper() + "_" + agg_df["sex"].str.upper() + "_" + agg_df["age_cat"].astype("object")
agg_df.drop("customer_level_based2", axis=1, inplace=True)
############## güzel yöntemler ####################33
agg_df['CUSTOMERS_LEVELBASED'] = ['_'.join(col).upper() for col in agg_df.drop(["age",'price'], axis=1).values]
agg_df["customers_level_based"] = ['_'.join(i).upper() for i in agg_df.drop(["AGE", "PRICE"], axis=1).values]
agg_df.head()
agg_df['customers_level_based'] = agg_df[['country', 'source', 'sex', 'age_cat']].agg(lambda x: '_'.join(x).upper(), axis=1)

#######################################################################################333
agg_df["age_cat"] = agg_df["age_cat"].astype("object")
agg_df.groupby("customer_level_based")[["customer_level_based", "price"]].head()
agg_df["customer_level_based"].count()
# birden fazla aynı kategoride (customer level based) elemean olabileceğinden bunları tekilleştirerek price in ortalamasını aldık!
agg_new_df = agg_df.groupby("customer_level_based").agg({"price": ["mean"]}).reset_index()
agg_new_df["customer_level_based"].nunique()
agg_new_df["customer_level_based"].count()

agg_new_df.shape

# persona ları buluyoruz
agg_new_df.head()

agg_new_df["segment"] = pd.qcut(agg_new_df["price"],q=4, labels=["D", "C", "B", "A"])
agg_new_df = agg_new_df.sort_values(by="price", ascending=False)
agg_new_df.shape


agg_new_df.groupby("segment").agg({"price": ["mean", "max", "sum", "count"]})

new_user = "TUR_ANDROID_FEMALE_31_40"
new_user2 = "FRA_IOS_FEMALE_31_40"

agg_new_df[agg_new_df["customer_level_based"] == new_user]
agg_new_df[agg_new_df["customer_level_based"] == new_user2]

########## streamlit kütüphanesi
import streamlit as st

st.title("Kural Tabanlı Sınıflandırma")

agg_new_df
agg_df