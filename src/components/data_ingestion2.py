# import os 
# import sys 
# from src.exception import CustomException
# from src.logger import logging
# import pandas as pd


# from sklearn.model_selection import train_test_split
# from dataclasses import dataclass

# class DataIngestionConfig:
#     train_data_path:str=os.path.join('artifact',"train.csv")
#     test_data_path:str=os.path.join('artifacts',"test.csv")
#     raw_data_path:str=os.path.join('artifact',"data.csv")



# class DataIngestion:
#     def __init__(self):
#         self.ingestion_congif=DataIngestionConfig()


#     def initiate_data_ingestion(self):
#         logging.info('enterd the data ingesion method or component')
#         try:
#             df=pd.read_csv('notebook\data\loan.csv')
#             logging.info('read the dataset as dataframe')
            
#             os.makedirs(self.ingestion_congif.train_data_path)
#             df.to_csv(self.ingestion_congif.raw_data_path,index=False,header=True)

#             logging.info("train test split initiated")
#             train_set,test_set=train_test_split(df,test_size=0.2,random_state=42)

#             train_set.to_csv(self.ingestion_congif.test_data_path,index=false,header=true)

#             logging.info("Ingestion of the data iss completed")

#             return(
#                 self.ingestion_congif.train_data_path,
#                 self.ingestion_congif.test_data_path
#             )




#         except Exception as e:
#             raise CustomException(e,sys)
        

#     if __name__=="__main__":
#          obj=DataIngestion()
#          obj.initiate_data_ingestion()
        
import os
import sys 
from src.exception import CustomException
from src.logger import logging
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

# --- 1. Configuration Class (Defines Output Paths) ---
# @dataclass automatically handles the creation of __init__ methods
@dataclass
class DataIngestionConfig:
    # Set a consistent base directory for all artifacts
    artifacts_dir: str = os.path.join('artifacts') 
    
    # Define the full paths for the output files
    train_data_path: str = os.path.join(artifacts_dir, "train.csv")
    test_data_path: str = os.path.join(artifacts_dir, "test.csv")
    raw_data_path: str = os.path.join(artifacts_dir, "data.csv")


# --- 2. Data Ingestion Class (Handles Logic) ---
class DataIngestion:
    def __init__(self):
        # Instantiate the config to get the paths
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info('Entered the data ingestion method or component')
        try:
            # 1. Read Data
            # Note: This assumes 'loan.csv' is located in your project root at 'notebook/data/'
            df = pd.read_csv('notebook/data/loan.csv') 
            logging.info('Read the dataset as dataframe')
            
            # 2. Create Artifacts Directory
            # Use os.path.dirname() to extract the directory path from the full file path
            # The 'exist_ok=True' prevents an error if the directory already exists
            os.makedirs(self.ingestion_config.artifacts_dir, exist_ok=True)
            logging.info(f"Created artifacts directory: {self.ingestion_config.artifacts_dir}")

            # 3. Save Raw Data
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)
            logging.info("Raw data saved to artifacts folder.")

            # 4. Split Data
            logging.info("Initiating train test split")
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)

            # 5. Save Split Data
            # Correctly saving the train set to the train path
            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            
            # Correctly saving the test set to the test path
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)

            logging.info("Ingestion of the data is completed")

            # Return the paths to be used by the next component (Data Transformation)
            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )

        except Exception as e:
            # Re-raise the exception using your custom exception handling
            raise CustomException(e, sys)

# --- 3. Execution Block ---
if __name__ == "__main__":
    try:
        obj = DataIngestion()
        train_path, test_path = obj.initiate_data_ingestion()
        
        # At this point, you would typically call your data transformation component:
        # data_transformer = DataTransformation()
        # data_transformer.initiate_data_transformation(train_path, test_path)
        
        logging.info(f"Train data saved at: {train_path}")
        logging.info(f"Test data saved at: {test_path}")

    except Exception as e:
        # This catches any remaining exceptions not handled inside the method
        logging.error(f"Data Ingestion process failed: {e}")