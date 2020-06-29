import enum


class MusicLabel(enum.Enum):
    note = 0
    chord = 1
    rest = 2
    tempo = 3
    TimeSignature = 4
    KeySignature = 5
    other = 6
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
