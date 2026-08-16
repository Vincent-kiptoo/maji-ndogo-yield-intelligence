"""
This module centralizes all configuration parameters used throughout the pipeline, including database connection string,
SQL queris, data transformation rules, csv sources, and regex patterns for data extraction and validation
"""

db_path = "sqlite:///data/Maji_Ndogo_farm_survey_small.db"

sql_query = """
SELECT *
FROM geographic_features
LEFT JOIN weather_features USING (Field_ID)
LEFT JOIN soil_and_crop_features USING (Field_ID)
LEFT JOIN farm_management_features USING (Field_ID)
"""

columns_to_rename = {"Annual_yield": "Crop_type", "Crop_type": "Annual_yield"}

values_to_rename = {
    "cassaval": "cassava",
    "wheatn": "wheat",
    "teaa": "tea"
}

weather_mapping_csv = "https://raw.githubusercontent.com/Explore-AI/Public-Data/master/Maji_Ndogo/Weather_data_field_mapping.csv"
weather_csv_path = "https://raw.githubusercontent.com/Explore-AI/Public-Data/master/Maji_Ndogo/Weather_station_data.csv"

regex_patterns = {
    'Rainfall': r'(\d+(\.\d+)?)\s?mm',
     'Temperature': r'(\d+(\.\d+)?)\s?C',
    'Pollution_level': r'=\s*(-?\d+(\.\d+)?)|Pollution at \s*(-?\d+(\.\d+)?)'
    }

config_params = {
    "db_path": db_path,
    "sql_query": sql_query,
    "columns_to_rename": columns_to_rename,
    "values_to_rename": values_to_rename,
    "weather_mapping_csv": weather_mapping_csv,
    "weather_csv_path": weather_csv_path,
    "regex_patterns": regex_patterns,
}

