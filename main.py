import sys

from app.lib.init import parse_args
from app.lib.srt_parser import SrtFileParser
from app.subtitles.subtitles import SubtitlesClass

def main():
    args = parse_args()
    subtitles_object = SrtFileParser().parse_srt_file(args.file)
    
    s = SubtitlesClass(subtitles_object["subtitles"])
    s.start()

if __name__ == "__main__":
    sys.exit(main())
