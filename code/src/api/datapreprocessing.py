import os
import json

class ChatHistoryProcessor:
    """
    A class to process chat history by combining JSON files into a single JSON array.
    """

    def __init__(self, input_directory: str, output_file: str):
        """
        Initializes the ChatHistoryProcessor with input and output paths.

        :param input_directory: Path to the directory containing JSON files
        :param output_file: Path to the output JSON file
        """
        self.input_directory = input_directory
        self.output_file = output_file

    def combine_json_files(self):
        """
        Reads all JSON files in the input directory, combines their contents into a JSON array,
        and writes the result to the output file.
        """
        if not os.path.isdir(self.input_directory):
            raise ValueError(f"The provided path '{self.input_directory}' is not a directory or does not exist.")

        combined_data = []

        # Iterate through all files in the input directory
        for filename in os.listdir(self.input_directory):
            if filename.endswith('.json'):
                file_path = os.path.join(self.input_directory, filename)
                with open(file_path, 'r', encoding='utf-8') as json_file:
                    try:
                        data = json.load(json_file)
                        combined_data.append(data)
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON from file {filename}: {e}")

        # Write the combined data to the output file
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
        with open(self.output_file, 'w', encoding='utf-8') as output_json_file:
            json.dump(combined_data, output_json_file, indent=4)