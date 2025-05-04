import sys

from app.lib.file_parser import Srt
from app.lib.init import parse_args
from app.subtitles.run import Runner

def main():
    args = parse_args()
    srt = Srt()
    subtitles_object = srt.parse_file(args.file)
    
    runner = Runner(subtitles_object["subtitles"])
    runner.run()

if __name__ == "__main__":
    sys.exit(main())
