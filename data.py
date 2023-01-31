import pandas as pd
import simplejson
import json
from tqdm import tqdm

## Dynamic read

# file = pd.ExcelFile('globalmart.xlsx')
# sheets = file.sheet_names
# for sheet in sheets:
#     globals()[sheet+'_df'] = file.parse(sheet)

# print(transactions_df.head())
transaction_df = pd.read_excel("globalmart.xlsx", sheet_name="transactions", engine="openpyxl")
products_df = pd.read_excel("globalmart.xlsx", sheet_name="products", engine="openpyxl")
orders_df = pd.read_excel("globalmart.xlsx", sheet_name="orders", engine="openpyxl")
customers_df = pd.read_excel("globalmart.xlsx", sheet_name="customers", engine="openpyxl")
vendors_df = pd.read_excel("globalmart.xlsx", sheet_name="vendors", engine="openpyxl")

def record_to_json(record):
    final_record = {}
    columns = record.columns
    values = record.values[0]
    for index in range(len(columns)):
        final_record[columns[index]] = values[index]
    
    return final_record


def count_of_data():
    return len(transaction_df)


def fetch_sales_data(start=1, limit=30):
    ## Give assigmnet to above created deataframe as global
    global transaction_df
    global products_df
    global orders_df
    global customers_df
    global vendors_df

    ## In products_df, there is unnamed column
    for col in products_df.columns: 
        if 'Unnamed' in col: 
            products_df.drop(col, axis=1, inplace=True)

    ## there are some nan values in products, thus fill out that nan with null
    products_df = products_df.fillna("null")

    ## In orders_df there is one column, that is in datetime64, thus for conversion in json we needs that into str. Thus convert thta into str
    orders_df["order_purchase_date"] = orders_df["order_purchase_date"].astype(str)
    products_df["sizes"] = products_df["sizes"].astype(str) ## it was considered as datetime object
    # print(orders_df.dtypes)

    data = []
    start_range = start-1
    end_range = (start+limit) - 1
    for i in tqdm(range(start_range, end_range)):
        # single_record = {}
        transaction = transaction_df[transaction_df.index==i]
        single_record_json = record_to_json(transaction)

        ## Now single records contains order_id and product_id
        order_id = single_record_json["order_id"]
        
        ## Now fetch the details from the orders tables
        order = orders_df[orders_df["order_id"]==order_id]
        order_json = record_to_json(order)
        single_record_json["order"] = order_json
        
        ## As order_id is already there is nested orders key then delete the order_id key
        single_record_json.pop("order_id")
        
        ## Now order have 2 different ids, that are customer_id and vendor_id thus fetch the attribute from there
        customer_id = single_record_json["order"]["customer_id"]
        vendor_id = single_record_json["order"]["vendor_id"]

        ## Now fetch the details from the customers table
        customer = customers_df[customers_df["customer_id"]==customer_id]

        try:
            ## Now remove the columns that are of address and store it in separate df
            address_attr = ["zip_code", "region", "country", "city", "state"]
            other_attr = [col for col in customer.columns if col not in address_attr]
            customer_address = customer[address_attr]
            customer = customer[other_attr]
            customer_json = record_to_json(customer)
            customer_address_json = record_to_json(customer_address)
            single_record_json["order"]["customer"] = customer_json
            single_record_json["order"]["customer"]["address"] = customer_address_json
        except IndexError as err:
            print(f"{i+1} row has no records for customers")

        vendor = vendors_df[vendors_df["VendorID"]==vendor_id]
        vendor_json = record_to_json(vendor)
        single_record_json["order"]["vendor"] = vendor_json

        ## As customer_id is already there is nested orders key then delete the separate customer_id key
        single_record_json["order"].pop("customer_id")
        single_record_json["order"].pop("vendor_id")
        
        
        product_id = single_record_json["product_id"]
        product = products_df[products_df["product_id"]==product_id]
        product_json = record_to_json(product)
        single_record_json["product"] = product_json

        ## Now pop the product_id, as it is there inside the nested product dictionary
        single_record_json.pop("product_id")
        # print(simplejson.dumps(single_record_json, ignore_nan=True)) ## reference:- https://stackoverflow.com/questions/28639953/python-json-encoder-convert-nans-to-null-instead
        
        ## Now append this to transactions list
        data.append(single_record_json)


    final_data = {}
    final_data["data"] = data

    ## Debug the code from here:-
    # for i in final_data["data"]:
    #     try:
    #         json_object = json.dumps(i) #, sort_keys=True, default=True)
    #     except TypeError as err:
    #         print(i)

    # exit()

    return final_data
    # json_object = simplejson.dumps(final_data, ignore_nan=True)

    # return json_object


if __name__ == '__main__':
    data = fetch_sales_data(1000)
    json_object = simplejson.dumps(data, ignore_nan=True)
    with open("sales_json.json", "w") as file:
        file.write(json_object)
