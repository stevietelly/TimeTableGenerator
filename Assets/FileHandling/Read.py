import json
import os
import sys

from Data.Validators.Structure import VALID_FILE_FOMARTS




class Read:
    def __init__(self, filename: str):
        """
        A class used to read json files and returns the contents
        param: filename
        param: filetype
        """
        self.fn = filename
        
 
        if not os.path.splitext(filename)[1].strip(".") in VALID_FILE_FOMARTS:
            print(f'Invalid File Formart: file({filename})')
            sys.exit(1)
        self.filetype = os.path.splitext(filename)[1].strip(".")

    def _handle_txt(self):
        config = {}
        # open the file in read mode
        with open(self.fn, 'r') as f:
            # read each line in the file
            for line in f:
                # split the line into key-value pairs
                key, value = line.strip().split(': ')
                # convert the value to an integer if it's a number
                if value.isnumeric():
                    value = int(value)
                # add the key-value pair to the dictionary
                config[key] = value

        return config

    def _handle_json(self):
        file = open(self.fn).read()
        content = json.loads(file)
        return content

    def extract(self)->dict:
        """
        Extract content from files

        return: json
        """
        return self._handle_json() if self.filetype == "json" else self._handle_txt()
       
