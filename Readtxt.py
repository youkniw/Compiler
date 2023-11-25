
class ReadTXT:
    def read_txt(txt_path):
        try:
            with open(txt_path, 'r') as file:
                return file.read()
        except Exception as e:
            print(e)
            return None
