import os

class JavaFileSearch:
    
    def test(self):
        directory_path = "C:\\Users\\eminy\\Documents"  # Replace this with your directory path
        search_string = "JavaFileSearch"  # The string you want to search for
        self.search_string(directory_path, search_string)
        print("Search is DONE")

    def search_string(self, directory_path, search_string):
        java_files = self.find_java_files(directory_path)

        for file in java_files:
            try:
                line_numbers = self.contains_string_index_line(file, search_string)
                if line_numbers:
                    print(f"Found '{search_string}' in file: {file} LineNumbers: {line_numbers}")
            except IOError as e:
                print(e)

    def find_java_files(self, directory):
        java_files = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".java"):
                    java_files.append(os.path.join(root, file))
        return java_files

    def contains_string_index_line(self, file, search_string):
        result_line_number = []
        with open(file, 'r', encoding='utf-8') as reader:
            line_number = 0
            for line in reader:
                line_number += 1
                if search_string in line:
                    result_line_number.append(line_number)
        return result_line_number

if __name__ == "__main__":
    java_file_search = JavaFileSearch()
    java_file_search.test()