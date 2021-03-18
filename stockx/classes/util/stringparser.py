import csv

class StringParser:
    def parse_keywords(self, file_path):
        with open(file_path) as keywords:
            keyword_file = keywords.read()
            keywords = keyword_file.split('\n')
            return keywords