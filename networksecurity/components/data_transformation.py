import sys
import os
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from networksecurity.constant.training_pipeline import TARGET_COLUMN
from networksecurity.constant.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS

from networksecurity.entity.artifact_entity import (
    DataTransformationArtifact,
    DataValidationArtifact
)

from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.exception.exception import NetworkSecurityException 
from networksecurity.logging.logger import logging
from networksecurity.utils.main_utils.utils import save_numpy_array_data,save_object

class DataTransformation:
    def __init__(self,data_validation_artifact:DataValidationArtifact,
                 data_transformation_config:DataTransformationConfig):
        try:
            self.data_validation_artifact:DataValidationArtifact=data_validation_artifact
            self.data_transformation_config:DataTransformationConfig=data_transformation_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    @staticmethod
    #staticmethod is an alternative to self, it allows the method to be called without an instance of the class.
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
#Reads a CSV file into a table (pandas DataFrame).

    def get_data_transformer_object(cls)->Pipeline:
        """
        It initialises a KNNImputer object with the parameters specified in the training_pipeline.py file
        and returns a Pipeline object with the KNNImputer object as the first step.

        Args:
          cls: DataTransformation

        Returns:
          A Pipeline object
        """
        logging.info(
            "Entered get_data_trnasformer_object method of Trnasformation class"
        )
        try:
           imputer:KNNImputer=KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
           logging.info(
                f"Initialise KNNImputer with {DATA_TRANSFORMATION_IMPUTER_PARAMS}"
            )
           processor:Pipeline=Pipeline([("imputer",imputer)])
           return processor
        except Exception as e:
            raise NetworkSecurityException(e,sys)
#Uses KNNImputer to fill in missing values by looking at nearby data points
        
    def initiate_data_transformation(self)->DataTransformationArtifact:
        logging.info("Entered initiate_data_transformation method of DataTransformation class")
        try:
            logging.info("Starting data transformation")
            train_df=DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df=DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)
#Reads the valid train and test CSV files
            ## training dataframe
            input_feature_train_df=train_df.drop(columns=[TARGET_COLUMN],axis=1)
            #Removes the label column (Result) from the training data — what’s left are the input features
            target_feature_train_df = train_df[TARGET_COLUMN]
            # Picks only the label column (Result) — this is the target/output we want to predict
            target_feature_train_df = target_feature_train_df.replace(-1, 0)
            #If the label has -1, it replaces it with 0 (probably to convert it into binary format 0 or 1).

            #testing dataframe
            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]
            target_feature_test_df = target_feature_test_df.replace(-1, 0)

            preprocessor=self.get_data_transformer_object()
#This calls a function that gives you a preprocessor pipeline — which contains a KNNImputer (used to fill missing values in the data).
            preprocessor_object=preprocessor.fit(input_feature_train_df)
            #The preprocessor learns from the training data — it finds patterns to understand how to fill in missing values.
            transformed_input_train_feature=preprocessor_object.transform(input_feature_train_df)
            transformed_input_test_feature =preprocessor_object.transform(input_feature_test_df)
            #Applies the learned rules to transform the training and test data (i.e., fills missing values using nearby data points).
             

            train_arr = np.c_[transformed_input_train_feature, np.array(target_feature_train_df) ]
            test_arr = np.c_[ transformed_input_test_feature, np.array(target_feature_test_df) ]
#This joins (column-wise using np.c_) the cleaned features and their corresponding labels (target_feature_train_df / target_feature_test_df) into one array for training and testing
 
            #save numpy array data
            save_numpy_array_data( self.data_transformation_config.transformed_train_file_path, array=train_arr, )
            save_numpy_array_data( self.data_transformation_config.transformed_test_file_path,array=test_arr,)
            #Saves the training and testing arrays as .npy files (compressed binary NumPy format) so they can be loaded easily later.
            save_object( self.data_transformation_config.transformed_object_file_path, preprocessor_object,)

            save_object( "final_model/preprocessor.pkl", preprocessor_object,)
            # Saves the preprocessor (KNNImputer) so that it can be reused

            #preparing artifacts

            data_transformation_artifact=DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )
            return data_transformation_artifact
# This returns structured info about what files were generated, which is passed to the next pipeline stage (e.g., ModelTrainer).

            
        except Exception as e:
            raise NetworkSecurityException(e,sys)

##SUMMARY:

#📄 Read the data files
#We took the cleaned files (from the last step) and opened them.

#✂️ Split the data into two parts:

#Inputs: all the things we’ll use to guess the result (like URLs, length, etc.)

# Result: the final answer (whether it’s phishing or not).

# We also changed the answers from -1 to 0, just to make it easier for the model.

# 🧹 Fixed missing blanks in the data
# Some rows may be missing information (blanks).
# We used a smart method (called KNN) to guess what those blanks might be and fill them in.

# 🔧 Applied that fixing tool to our data

# We "fitted" the tool on the training data to understand how to fix the blanks.
# This means it learned from the training data.

# Then used it to clean both train and test data. (transformed_input_train_feature and transformed_input_test_feature)

# 🧱 Stuck the input and result back together
# Now that everything is clean, we joined the inputs and the result together again.

# 💾 Saved everything

# We saved the cleaned train and test data to files.

# We also saved the tool we used (the "fixer") so we can reuse it later when new data comes in.

