from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging


## configuration of the Data Ingestion Config

from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact
import os
import sys
import numpy as np
import pandas as pd
import pymongo
from typing import List
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL=os.getenv("MONGO_DB_URL")

#converting the MONGO_DB_URL to a pandas dataframe:
class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)

#Takes in a configuration object (DataIngestionConfig)
#Stores it in self.data_ingestion_config so all other methods can use it
        
    def export_collection_as_dataframe(self):
        """
        Read data from mongodb
        """
        try:
            database_name=self.data_ingestion_config.database_name
            collection_name=self.data_ingestion_config.collection_name
            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL)
            collection=self.mongo_client[database_name][collection_name]
#Connects to MongoDB using the URL from your .env file
#Selects the right database and collection
            df=pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df=df.drop(columns=["_id"],axis=1)
            
            df.replace({"na":np.nan},inplace=True)
            return df
#Reads the entire collection
#Converts it into a DataFrame
#Removes MongoDB’s _id column (not useful for ML)
#Replaces any string "na" with proper missing values (np.nan)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
   #Saves the raw DataFrame (fetched from MongoDB) into a CSV file — this file is called the "Feature Store".
    def export_data_into_feature_store(self,dataframe: pd.DataFrame):
        try:
            feature_store_file_path=self.data_ingestion_config.feature_store_file_path
            #creating folder
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            return dataframe
#Writes the DataFrame to a .csv file and returns the DataFrame
#This file is stored in the feature store directory defined in the config
        except Exception as e:
            raise NetworkSecurityException(e,sys)

#Takes the DataFrame and splits it into training and testing sets.
    def split_data_as_train_test(self,dataframe: pd.DataFrame):
        try:
            train_set, test_set = train_test_split(
                dataframe, test_size=self.data_ingestion_config.train_test_split_ratio
            )
            #Uses train_test_split() to split the data , Ratio is decided by config
            logging.info("Performed train test split on the dataframe")

            logging.info(
                "Exited split_data_as_train_test method of Data_Ingestion class"
            )
            
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            
            os.makedirs(dir_path, exist_ok=True)
            
            logging.info(f"Exporting train and test file path.")
            
            train_set.to_csv(
                self.data_ingestion_config.training_file_path, index=False, header=True
            )

            test_set.to_csv(
                self.data_ingestion_config.testing_file_path, index=False, header=True
            )
            logging.info(f"Exported train and test file path.")
#Saves both sets as separate .csv files (paths from config)
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
#This is the main method that calls all other steps in the right order.
    def initiate_data_ingestion(self):
        try:
            dataframe=self.export_collection_as_dataframe()
            #Calls export_collection_as_dataframe() → gets data from MongoDB
            dataframe=self.export_data_into_feature_store(dataframe)
            #Then calls export_data_into_feature_store() → saves it to a CSV
            self.split_data_as_train_test(dataframe)
            #Then calls split_data_as_train_test() → splits into train/test CSVs
            dataingestionartifact=DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_file_path,
                                                        test_file_path=self.data_ingestion_config.testing_file_path)
            return dataingestionartifact
            #Finally, returns a DataIngestionArtifact — a small object that stores the paths to the generated train and test files
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
