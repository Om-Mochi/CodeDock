class Debug:
    # Reset
    RESET = "\033[0m"

    # Text colors
    BLACK   = "\033[30m"
    RED     = "\033[91m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    BLUE    = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN    = "\033[96m"
    WHITE   = "\033[97m"

    # Styles
    BOLD      = "\033[1m"
    DIM       = "\033[2m"
    UNDERLINE = "\033[4m"

    # ---- Color print helpers ----
    @staticmethod
    def red(*msg):     print(f"{Debug.RED}{msg}{Debug.RESET}")
    @staticmethod
    def green(*msg):   print(f"{Debug.GREEN}{msg}{Debug.RESET}")
    @staticmethod
    def yellow(*msg):  print(f"{Debug.YELLOW}{msg}{Debug.RESET}")
    @staticmethod
    def blue(*msg):    print(f"{Debug.BLUE}{msg}{Debug.RESET}")
    @staticmethod
    def magenta(*msg):print(f"{Debug.MAGENTA}{msg}{Debug.RESET}")
    @staticmethod
    def cyan(*msg):    print(f"{Debug.CYAN}{msg}{Debug.RESET}")
    @staticmethod
    def white(*msg):   print(f"{Debug.WHITE}{msg}{Debug.RESET}")

    # ---- Style helpers ----
    @staticmethod
    def bold(*msg):      print(f"{Debug.BOLD}{msg}{Debug.RESET}")
    @staticmethod
    def underline(*msg): print(f"{Debug.UNDERLINE}{msg}{Debug.RESET}")

    # ---- Combined helpers ----
    @staticmethod
    def error(*msg):
        print(f"{Debug.BOLD}{Debug.RED}[ERROR]{Debug.RESET} {msg}")

    @staticmethod
    def warn(*msg):
        print(f"{Debug.YELLOW}[WARN]{Debug.RESET} {msg}")

    @staticmethod
    def info(*msg):
        print(f"{Debug.CYAN}[INFO]{Debug.RESET} {msg}")

    @staticmethod
    def success(*msg):
        print(f"{Debug.GREEN}[OK]{Debug.RESET} {msg}")
