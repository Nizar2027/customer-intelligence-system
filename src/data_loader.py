import pandas as pd 
from pathlib import Path
import urllib.request
import tarfile
import zipfile
import os

#def reading_first_excel_file():
#return pd.read_excel(Path("data/excel/customers.xlsx"))
#def reading_second_excel_file():

    #return pd.read_excel(Path("data/excel/products.xlsx"))
#def reading_third_excel_file():
#return pd.read_excel(Path("data/excel/transactions.xlsx"))
#excel1=reading_first_excel_file()
#excel2=reading_second_excel_file()
#excel3=reading_third_excel_file()
#print(excel1.head())
#print(excel2.head())
#print(excel3.head())
#df1=excel3.merge(excel1, how='left',on='customer_id')
#df2=df1.merge(excel2, how='left',on='product_id')
#print(df1.head())
#print(df2.head())
#print(df2.columns)
#df2.to_csv("data/processed/customer_behavior.csv", index=False)





#def load_housing_data():
    #tarball_path = Path("datasets/housing.tgz")
    #if not tarball_path.is_file():
        #Path("datasets").mkdir(parents=True, exist_ok=True)
       # url = "https://github.com/ageron/data/raw/main/housing.tgz"
       # urllib.request.urlretrieve(url, tarball_path)
   # with tarfile.open(tarball_path) as housing_tarball:
           # housing_tarball.extractall(path="datasets")
    #return pd.read_csv(Path("datasets/housing/housing.csv"))


def load_online_retail_data():
    dataset_dir = Path("data/raw")
    zip_path = dataset_dir / "online-retail-dataset.zip"

    # Create folder if not exists
    dataset_dir.mkdir(parents=True, exist_ok=True)

    # Download dataset if not already downloaded
    if not zip_path.exists():
        os.system(
            "kaggle datasets download -d ulrikthygepedersen/online-retail-dataset "
            "-p data/raw --force"
        )

    # Extract zip file
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(dataset_dir)

    # Load CSV (check actual filename)
    csv_path = dataset_dir / "online_retail.csv"

    return pd.read_csv(csv_path)

# Run function
my_data = load_online_retail_data()
print(my_data.head())



    




