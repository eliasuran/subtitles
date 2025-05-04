from app.lib.time import time_str_to_ms


class SrtFileParser:
    def __init__(self):
        self.file_example_str = '''
        1
        00:00:00,000 --> 00:00:03,680
        (aaaaaa)
        
        2
        00:00:23,500 --> 00:00:24,559
        What's she doing?
        
        3
        00:00:24,800 --> 00:00:25,829
        My gosh.
        
        4
        00:00:29,730 --> 00:00:31,899
        What did I do wrong?
        
        5
        00:00:32,399 --> 00:00:33,469
        - What did I...
        - Darn it.
        '''

        self.subtitle_instance_standard_format = {
            "id": 1, #int serial starting at 1
            "start": 0, #start time in ms int
            "end": 3680000, #end time in ms int
            "text_list": ["Hello","world"] #text to display. maybe just store this as one string?
        }

        self.subtitles_object_standard_format = {
            "version": "05042024",
            "subtitles": [] # array of subtitle_instance_standard_format
        }


    def validate_file(self):
        #read meta
        pass


    def parse_srt_file(self,path:str) -> dict:
        parsed_file = {**self.subtitles_object_standard_format,"subtitles":[]}

        f = open(path)
        #assuming file is valid here, if not will just panic at some point
        file_as_str = f.read()

        for section in file_as_str.split("\n\n"):
            split_section = section.split("\n")

            id = split_section[0]
            if id == "":
                continue

            start_to_end = split_section[1]
            start,end = start_to_end.replace(",",":").split(" --> ")
            text_list = split_section[2:]

            parsed_file["subtitles"].append({
                "id": id,
                "start": time_str_to_ms(start),
                "end": time_str_to_ms(end),
                "text_list": text_list
            })

        return parsed_file
