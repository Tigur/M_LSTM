from . import options
from . import m_classes as m
class ScoreTooShort(Exception):
    message = ''


    def __init__(self,trimmed_score_len):
        self.trimmed_sc = trimmed_score_len
        self.message = (f'{m.bcolors.FAIL} ERR :Score too short ! \n Expected length of the fragment : ' + str(options.fragment_len) + '\n'
        'current score len : {m.bcolors.ENDC}' + str(self.trimed_sc))



