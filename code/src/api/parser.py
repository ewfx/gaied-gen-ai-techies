import os
import eml_parser
import json
import datetime
from email import policy
from email.parser import BytesParser
from io import BytesIO

############################################## Parse chat history / training data:
class EMLParser: 

    def __init__(self, input_directory: str, output_directory: str):
        self.input_directory = input_directory
        self.output_directory = output_directory

    def get_eml_filenames(self, directory: str) -> list: 
        """
        Takes a local directory path as input and returns a list of .eml file names inside it.

        :param directory: Path to the local directory
        :return: List of .eml file names (not full paths)
        """
        if not os.path.isdir(directory):
            raise ValueError(f"The provided path '{directory}' is not a directory or does not exist.")

        return [f for f in os.listdir(directory) if f.endswith('.eml')]

    def parse_eml_file(self, filepath: str, filename: str) -> dict:
        """
        Parses an .eml file and extracts relevant email data into a structured JSON format.

        :param filepath: Path to the .eml file
        :param filename: Name of the .eml file
        :return: Dictionary representing the email content
        """
        with open(filepath, 'rb') as f:
            msg = BytesParser(policy=policy.default).parse(f)

        body_content = msg.get_body(preferencelist=('plain', 'html'))
        body_text = body_content.get_content() if body_content else ""

        attachments = []
        for part in msg.iter_attachments():
            attachments.append(part.get_filename())

        # Extract request type and sub-request type from filename
        name_parts = os.path.splitext(filename)[0].split("-")
        request_type = name_parts[0]
        sub_request_type = name_parts[1] if len(name_parts) > 1 else ""

        email_data = {
            "Request Type": request_type,
            "Sub Request Type": sub_request_type,
            "Subject": msg.get('Subject'),
            "Body": body_text,
            "Attachments": attachments,
            "Confidence score": 1
        }

        return email_data

    def process_eml_files(self):
        """
        Processes all .eml files in the input directory and saves each parsed email as an individual JSON file.

        :param directory: Path to the local directory
        :param output_directory: Directory to save the JSON output files
        """
        eml_files = self.get_eml_filenames(self.input_directory)
        os.makedirs(self.output_directory, exist_ok=True)

        for eml_file in eml_files:
            eml_path = os.path.join(self.input_directory, eml_file)
            email_data = self.parse_eml_file(eml_path, eml_file)

            json_filename = os.path.splitext(eml_file)[0] + ".json"
            json_filepath = os.path.join(self.output_directory, json_filename)

            with open(json_filepath, 'w', encoding='utf-8') as json_file:
                json.dump(email_data, json_file, indent=4)
    

    def EMLToJson(self, eml_string):
        # Convert the string into a BytesIO stream
        eml_bytes = BytesIO(eml_string.encode())

        # Parse the email content
        msg = BytesParser(policy=policy.default).parse(eml_bytes)

        # Extract subject
        subject = msg["subject"]

        # Extract body (handling plain and HTML content)
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == "text/plain":
                    body = part.get_payload(decode=True).decode(part.get_content_charset(), errors="ignore")
                    break  # Prefer plain text body
        else:
            body = msg.get_payload(decode=True).decode(msg.get_content_charset(), errors="ignore")
        
        # Extract attachments
        attachments = []
        for part in msg.walk():
            if part.get_content_disposition() == "attachment":
                file_name = part.get_filename()
                file_data = part.get_payload(decode=True)
                attachments.append({"filename": file_name})

        # Convert to JSON
        email_data = {
            "Subject": subject,
            "Body": body.strip(),
            "Attachments": attachments
        }
        
        return json.dumps(email_data, indent=4)
