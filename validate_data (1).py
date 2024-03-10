import unittest
import pandas as pd
from field_data_processor import FieldDataProcessor
from weather_data_processor import WeatherDataProcessor

weather_df = pd.read_csv('sampled_weather_df.csv')
field_df = pd.read_csv('sampled_field_df.csv')

class TestDataValidation(unittest.TestCase):

    def setUp(self):
        config_params = {
            "sql_query": """
                SELECT *
                FROM geographic_features
                LEFT JOIN weather_features USING (Field_ID)
                LEFT JOIN soil_and_crop_features USING (Field_ID)
                LEFT JOIN farm_management_features USING (Field_ID)
            """,
            "db_path": 'sqlite:///Maji_Ndogo_farm_survey_small.db',
            "columns_to_rename": {'Annual_yield': 'Crop_type', 'Crop_type': 'Annual_yield'},
            "values_to_rename": {'cassaval': 'cassava', 'wheatn': 'wheat', 'teaa': 'tea'},
            "weather_csv_path": "https://raw.githubusercontent.com/Explore-AI/Public-Data/master/Maji_Ndogo/Weather_station_data.csv",
            "weather_mapping_csv": "https://raw.githubusercontent.com/Explore-AI/Public-Data/master/Maji_Ndogo/Weather_data_field_mapping.csv",
            "regex_patterns": {
                'Rainfall': r'(\d+(\.\d+)?)\s?mm',
                'Temperature': r'(\d+(\.\d+)?)\s?C',
                'Pollution_level': r'=\s*(-?\d+(\.\d+)?)|Pollution at \s*(-?\d+(\.\d+)?)'
            }
        }

        self.field_processor = FieldDataProcessor(config_params)
        self.weather_processor = WeatherDataProcessor(config_params)

    def test_read_weather_DataFrame_shape(self):
        self.weather_processor.process()
        weather_df = self.weather_processor.weather_df
        self.assertIsNotNone(weather_df)
        self.assertGreater(len(weather_df), 0)

    def test_read_field_DataFrame_shape(self):
        self.field_processor.process()
        field_df = self.field_processor.df
        self.assertIsNotNone(field_df)
        self.assertGreater(len(field_df), 0)

    def test_weather_DataFrame_columns(self):
        self.weather_processor.process()
        weather_df = self.weather_processor.weather_df
        expected_columns = ['Measurement', 'Message', 'Value', 'Weather_station_ID']
        self.assertListEqual(sorted(list(weather_df.columns)), sorted(expected_columns))

    def test_field_DataFrame_columns(self):
        self.field_processor.process()
        field_df = self.field_processor.df
        expected_columns = ['Field_ID', 'Elevation', 'Latitude', 'Longitude', 'Location', 'Slope',
                             'Rainfall', 'Min_temperature_C', 'Max_temperature_C', 'Ave_temps',
                             'Soil_fertility', 'Soil_type', 'pH', 'Pollution_level', 'Plot_size',
                             'Crop_type', 'Annual_yield', 'Standard_yield']
        
        # Filter out any columns not present in the expected_columns
        actual_columns = [col for col in field_df.columns if col in expected_columns]

        self.assertListEqual(sorted(actual_columns), sorted(expected_columns))

    def test_field_DataFrame_non_negative_elevation(self):
        self.field_processor.process()
        field_df = self.field_processor.df
        self.assertTrue((field_df['Elevation'] >= 0).all())

    def test_crop_types_are_valid(self):
        field_df = pd.read_csv('sampled_field_df.csv')
        valid_crop_type = ['cassava', 'wheat', 'tea', 'potato', 'banana', 'coffee', 'maize', 'rice','cassava ','wheat ','tea ']  # Define your 
        assert field_df['Crop_type'].isin(valid_crop_type).all()

    def test_positive_rainfall_values(self):
        self.weather_processor.process()
        weather_df = self.weather_processor.weather_df
        rainfall_values = weather_df.loc[weather_df['Measurement'] == 'Rainfall', 'Value']
        self.assertTrue((rainfall_values >= 0).all())

if __name__ == '__main__':
    unittest.main()


