#This file runs the ETL pipeline

import os
import sys
import json

from dotenv import load_dotenv     #to call .env
load_dotenv()

MONGO_DB_URL=os.getenv("MONGO_DB_URL")
print(MONGO_DB_URL)


import certifi           #to check if the https has trusted certificates
ca=certifi.where()

import pandas as pd
import numpy as np
import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys) #sys used for more detailed info about error
        
    def csv_to_json_convertor(self,file_path):
        try:
            data=pd.read_csv(file_path)
            data.reset_index(drop=True,inplace=True) #drop the serial number column (index)
            records=list(json.loads(data.T.to_json()).values()) #convert a pandas DataFrame into a list of dictionaries
            #data.T → Flips the DataFrame (rows become columns and vice versa).
            #.to_json() → Turns the flipped DataFrame into a JSON string (text format).
            #json.loads(...) → Turns that JSON string back into a Python dictionary.
            #.values() → Takes only the data (not the keys like "0", "1", etc.).
            #list(...) → Converts that data into a list.
            return records
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def insert_data_mongodb(self,records,database,collection):
        try:
            self.database=database
            self.collection=collection
            self.records=records

            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL)
            self.database = self.mongo_client[self.database]
            
            self.collection=self.database[self.collection]
            self.collection.insert_many(self.records)
            return(len(self.records))
        except Exception as e:
            raise NetworkSecurityException(e,sys)

#if __name__ == "__main__" is like saying: “Only start cooking directly if I’m reading original recipe — not if someone copied my ingredients into their recipe (then start cooking when told so).”
#meaning if the class is called somewhere else then don't use the following commands directly unless said seperately. only use here directly
if __name__=='__main__':
    FILE_PATH="Network_Data\phisingData.csv"
    DATABASE="vivekranarajput999"
    Collection="NetworkData"
    networkobj=NetworkDataExtract()
    records=networkobj.csv_to_json_convertor(file_path=FILE_PATH)
    print(records)
    no_of_records=networkobj.insert_data_mongodb(records,DATABASE,Collection)
    print(no_of_records)
        


