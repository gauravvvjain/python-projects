import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler, LabelEncoder
from pipeline.utils.file_utils import setup_logger

logger = setup_logger('transform_engine')

class TransformEngine:
    def __init__(self, data: pd.DataFrame):
        self.data = data.copy()

    def normalize_numerical_columns(self) -> None:
        """Min-Max normalize the numerical columns to [0, 1]."""
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        if not numeric_cols.empty:
            scaler = MinMaxScaler()
            self.data[numeric_cols] = scaler.fit_transform(self.data[numeric_cols])
            logger.info(f"Normalized numerical columns using MinMaxScaler: {list(numeric_cols)}")

    def standardize_numerical_columns(self) -> None:
        """Standardize the numerical columns (z-score scaling)."""
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        if not numeric_cols.empty:
            scaler = StandardScaler()
            self.data[numeric_cols] = scaler.fit_transform(self.data[numeric_cols])
            logger.info(f"Standardized numerical columns using StandardScaler: {list(numeric_cols)}")

    def encode_categorical_columns(self) -> None:
        """Label encode strings/categorical data into numerical representation."""
        categorical_cols = self.data.select_dtypes(exclude=[np.number]).columns
        if not categorical_cols.empty:
            for col in categorical_cols:
                encoder = LabelEncoder()
                # Ensure no NaN values exist before encoding as LabelEncoder fails on NaN
                # We assume handling missing values was done prior in the cleaning stage.
                try:
                    self.data[col] = encoder.fit_transform(self.data[col].astype(str))
                except Exception as e:
                    logger.error(f"Error encoding column {col}: {str(e)}")
            logger.info(f"Label encoded categorical columns: {list(categorical_cols)}")

    def generate_features(self) -> None:
        """
        Generate new features.
        As a generic implementation, we create polynomial features (e.g., squared) of the top numerical features.
        """
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        
        # We only take the first two numeric columns to demonstrate feature generation.
        # This can be customized as per dataset.
        if len(numeric_cols) >= 2:
            col1 = numeric_cols[0]
            col2 = numeric_cols[1]
            new_col_name = f"{col1}_times_{col2}"
            self.data[new_col_name] = self.data[col1] * self.data[col2]
            logger.info(f"Generated new feature: {new_col_name}")

        elif len(numeric_cols) == 1:
            col1 = numeric_cols[0]
            new_col_name = f"{col1}_squared"
            self.data[new_col_name] = self.data[col1] ** 2
            logger.info(f"Generated new feature: {new_col_name}")

    def run_transformation_pipeline(self, scale_method='standardize') -> pd.DataFrame:
        """Run all transformation steps in sequence."""
        logger.info("Starting data transformation pipeline...")
        
        # Let's perform only one scaling method according to the argument
        if scale_method == 'normalize':
            self.normalize_numerical_columns()
        else:
            self.standardize_numerical_columns()
            
        self.encode_categorical_columns()
        self.generate_features()
        
        logger.info("Data transformation completed successfully.")
        return self.data
