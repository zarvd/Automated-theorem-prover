class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''

    @classmethod
    def print_header(cls, s):
        print(cls.HEADER + s + cls.ENDC)

    @classmethod
    def print_ok(cls, s, color='BLUE'):
        if color.upper() == 'BLUE':
            print(cls.OKBLUE + s + cls.ENDC)
        elif color.upper() == 'GREEN':
            print(cls.OKGREEN + s + cls.ENDC)

    @classmethod
    def print_warning(cls, s):
        print(cls.WARNING + s + cls.ENDC)

    @classmethod
    def print_fail(cls, s):
        print(cls.FAIL + s + cls.ENDC)
