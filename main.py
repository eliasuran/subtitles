import sys

from app.lib.file_parser import Srt
from app.lib.init import parse_args
from app.subtitles.subtitles import Subtitles

def main():
    args = parse_args()
    srt = Srt()
    subtitles_object = srt.parse_file(args.file)
    
    s = Subtitles(subtitles_object["subtitles"])
    s.start()

if __name__ == "__main__":
    sys.exit(main())
