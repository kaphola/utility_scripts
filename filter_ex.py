"""Module to manage constants being used across all suites and packages"""
###################################################################################################################
# List of extensions with its compression level and block size
###################################################################################################################
# Extension having zero compression level and 64 k block size
EXTENSION_ZERO_COMPRESSION_SIXTY_FOUR_K_BLOCK = ['.m4p', '.m4v', '.m2ts', '.bz', '.bzip', '.bzip2', '.deb', '.gzip',
                                                 '.sit', '.sitx', '.z', '.tbz2', '.qt', '.mpa', '.ram', '.wma', '.dmg']

# Extension having zero compression level and 4 MB block size
EXTENSION_ZERO_COMPRESSION_FOUR_MB_BLOCK = ['.jpg', '.jpeg', '.gif', '.mpg', '.mpeg', '.zip', '.rar', '.jar', '.gz',
                                            '.mp3', '.swf', '.wmv', '.mov', '.tgz', '.cab', '.m4a', '.avi', '.bz2',
                                            '.rpm', '.mp4', '.ra', '.flac', '.iso', '.mkv', '.exe', '.7z']

# Extension having 4 compression level and 4 MB block size
EXTENSION_FOUR_MB_BLOCK = [
    # Executables
    ".dll", ".msi", ".com", ".drv", ".sys", ".cpl", ".ocx", ".msp",
    # Images
    ".bmp", ".png", ".tif", ".jpe", ".raw", ".pic", ".pct", ".pxr", ".sct", ".ico", ".psd",
    # Video
    ".divx", ".rmvb", ".rm", ".flv", ".3gp", ".swi", ".vob",
    # Audio
    ".ogg", ".wav", ".mpc", ".au", ".aiff", ".aac", ".ape",
    # Compressed
    ".tar",
    # Backup & Disk images
    ".vmdk", ".vhdx", ".vhd", ".bak", ".wim",
    # Contacts
    ".vcf"
    # Office
    ".doc", ".ppt", ".xls", ".docx", ".docm", ".xlsx", ".xlsm", ".xts", ".xltm", ".pptx", ".pptm", ".odt", ".odb",
    ".ods", ".odp", ".odg", ".odc",
    ".odf", ".odi", ".odm", ".ott", ".ots", ".otp", ".otg", ".otc", ".otf", ".oti", ".oth",
    # PDF
    ".pdf",
    # HTML
    ".html", ".htm",
    # No extension
    "",
    # misc
    ".log", ".txt", ".fcs", ".dmp",
]

# Extension having 4 compression level and 64 k block size
EXTENSION_SIXTY_FOUR_K_BLOCK = [".bin", ".custom"]
EXTENSION_ALL = EXTENSION_ZERO_COMPRESSION_SIXTY_FOUR_K_BLOCK + \
                EXTENSION_ZERO_COMPRESSION_FOUR_MB_BLOCK + \
                EXTENSION_FOUR_MB_BLOCK + \
                EXTENSION_SIXTY_FOUR_K_BLOCK