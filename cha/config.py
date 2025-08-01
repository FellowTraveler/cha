# NOTE: do NOT modify any of the "import" lines below, just the variables!
from pathlib import Path
import importlib.util
import os

from cha import local


def lazy_tool(module_path, class_name):
    return {"_lazy_tool": True, "module_path": module_path, "class_name": class_name}


# system prompt
INITIAL_PROMPT = """
You are Cha, a lightweight CLI AI assistant for terminal-based interactions with models from multiple providers like OpenAI and Anthropic. Provide concise, clear, and accurate answers based on user input. Be brief but ensure responses fully address the query without omitting key details. Engage with warmth and intellectual curiosity, adapting to the user's tone for natural conversation. Maintain professionalism, relying on facts and logic. Handle tasks like chat, file processing, and commands as directed, but never assume or automate beyond explicit requests. Write complete, smooth sentences without hesitation or abrupt changes.

NOTE: For all of your responses, do not use em dashes (—) or hyphen-like interruptions to break sentences abruptly. Avoid any form of sentence interruption or abrupt breaks with dashes. Instead, write complete, smooth, and clear sentences without using dashes to indicate hesitation, interruption, or change in thought.
""".strip()

# editor system prompt
EDITOR_SYSTEM_PROMPT = """
You are a code editor. Modify the provided file according to the user's request. Return only the complete modified file content, no explanations or markdown formatting. Preserve all formatting and structure unless specifically requested to change it.
""".strip()

# key words
MULTI_LINE_SEND = "\\"
MULTI_LINE_MODE_TEXT = "\\"
CLEAR_HISTORY_TEXT = "!c"
EXIT_STRING_KEY = "!q"
HELP_PRINT_OPTIONS_KEY = "!h"
LOAD_MESSAGE_CONTENT = "!l"
LOAD_MESSAGE_CONTENT_ADVANCED = "!f"
RUN_ANSWER_FEATURE = "!w"
RUN_QUICK_SEARCH_FEATURE = "!s"
TEXT_EDITOR_INPUT_MODE = "!t"
SWITCH_MODEL_TEXT = "!m"
SWITCH_PLATFORM_TEXT = "!p"
USE_CODE_DUMP = "!d"
EXPORT_FILES_IN_OUTPUT_KEY = "!e"
PICK_AND_RUN_A_SHELL_OPTION = "!x"
ENABLE_OR_DISABLE_AUTO_SD = "!u"
LOAD_HISTORY_TRIGGER = "!hs"
RUN_EDITOR_ALIAS = "!v"
BACKTRACK_HISTORY_KEY = "!b"
CHANGE_DIRECTORY_ALIAS = "!n"
RECORD_AUDIO_ALIAS = "!r"
VOICE_OUTPUT_ALIAS = "!o"
HELP_ALL_ALIAS = "[ALL]"
EXPORT_ALL_JSON_ALIAS = "[ALL JSON]"
SKIP_SEND_TEXT = "!."

# aliases that don't require parameters by default
PARAMETER_LESS_ALIASES = [
    CLEAR_HISTORY_TEXT,
    EXIT_STRING_KEY,
    LOAD_MESSAGE_CONTENT,
    LOAD_MESSAGE_CONTENT_ADVANCED,
    RUN_ANSWER_FEATURE,
    RUN_QUICK_SEARCH_FEATURE,
    TEXT_EDITOR_INPUT_MODE,
    SWITCH_MODEL_TEXT,
    SWITCH_PLATFORM_TEXT,
    USE_CODE_DUMP,
    EXPORT_FILES_IN_OUTPUT_KEY,
    ENABLE_OR_DISABLE_AUTO_SD,
    RUN_EDITOR_ALIAS,
    BACKTRACK_HISTORY_KEY,
    CHANGE_DIRECTORY_ALIAS,
    RECORD_AUDIO_ALIAS,
    VOICE_OUTPUT_ALIAS,
    SKIP_SEND_TEXT,
    HELP_PRINT_OPTIONS_KEY,
]

# last updated on 4-10-2024
CHA_DEFAULT_MODEL = "gpt-4.1"
CHA_DEFAULT_IMAGE_MODEL = "gpt-4o"
CHA_DEBUG_MODE = False
CHA_STREAMING_ERROR_LIMIT = 5
CHA_CURRENT_PLATFORM_NAME = "openai"

# local config variables
CHA_DEFAULT_SHOW_PRINT_TITLE = True
CHA_LOCAL_SAVE_ALL_CHA_CHATS = False
CHA_SHOW_VISITED_DIRECTORIES_ON_EXIT = True

# shell command security config, block only very dangerous commands
BLOCKED_SHELL_COMMANDS = [
    "sudo",
    "su",
    # "rm",
    # "rmdir",
    "dd",
    "mkfs",
    "fdisk",
    "format",
    "shutdown",
    "reboot",
    "halt",
    "poweroff",
    "init",
    "kill",
    "killall",
    "pkill",
    "passwd",
    "chpasswd",
    "userdel",
    "groupdel",
    "deluser",
    "delgroup",
    "iptables",
    "ufw",
    "firewall-cmd",
    "pfctl",
    "del",
    "deltree",
    "rd",
    "erase",
]

# answer feature config
DEFAULT_SEARCH_BIG_MODEL = "gpt-4.1"
DEFAULT_SEARCH_SMALL_MODEL = "gpt-4.1-mini"
DEFAULT_SEARCH_FRESHNESS_STATE = "none"
DEFAULT_SEARCH_MAX_TOKEN_LIMIT = 1_000_000
DEFAULT_SEARCH_TIME_DELAY_SECONDS = 1
DEFAULT_SEARCH_RESULT_COUNT = 5
DEFAULT_GEN_SEARCH_QUERY_COUNT = 5
CHA_SEAR_XNG_BASE_URL = "http://localhost:8080"
CHA_USE_SEAR_XNG = False
CHA_SEAR_XNG_TIMEOUT = 30

# other random configs
OPENAI_MODELS_TO_KEEP = ["gpt", "o0", "o1", "o2", "o3", "o4", "o5", "o6", "o7"]
OPENAI_IGNORE_DATED_MODEL_NAMES = False
BY_PASS_SLOW_MODEL_DETECTION = False
OPENAI_MODELS_TO_IGNORE = [
    "instruct",
    "realtime",
    "audio",
    "tts",
    "image",
    "transcribe",
]

# terminal/console config
SUPPORTED_TERMINAL_IDES = ["vim", "nvim", "vi", "nano", "hx", "pico", "micro", "emacs"]
PREFERRED_TERMINAL_IDE = "vi"
MOVE_CURSOR_ONE_LINE = "\033[F"
HIDE_CURSOR = "\033[?25l"
SHOW_CURSOR = "\033[?25h"
CLEAR_LINE = "\033[K"
TERMINAL_THEME_CODES = {
    "reset": "\033[0m",
    "colors": {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
        "black": "\033[30m",
    },
    "styles": {"bold": "\033[1m", "underline": "\033[4m"},
    "backgrounds": {
        "black": "\033[40m",
        "red": "\033[41m",
        "green": "\033[42m",
        "yellow": "\033[43m",
        "blue": "\033[44m",
        "magenta": "\033[45m",
        "cyan": "\033[46m",
        "white": "\033[47m",
    },
}

# external, custom, 3rd party tools if defined by the user externally
EXTERNAL_TOOLS = []

# http request configs
REQUEST_DEFAULT_TIMEOUT_SECONDS = 10
REQUEST_DEFAULT_RETRY_COUNT = 1
REQUEST_BACKOFF_FACTOR = 0.1
REQUEST_DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# codedump variables
NOTHING_SELECTED_TAG = "[NOTHING]"
EXIT_SELECTION_TAG = "[EXIT]"
FILES_TO_IGNORE = [
    ".DS_Store",
    ".env",
    ".env.local",
    ".env",
    ".env.local",
    ".env.development",
    ".env.production",
    ".env.test",
]
DIRS_TO_IGNORE = [
    # version control
    ".git/",
    ".hg/",
    ".svn/",
    "CVS/",
    # python
    "__pycache__/",
    ".venv/",
    "venv/",
    "env/",
    ".env/",
    "*.egg-info/",
    ".pytest_cache/",
    ".mypy_cache/",
    ".ruff_cache/",
    "htmlcov/",
    # nodejs
    "node_modules/",
    ".npm/",
    ".yarn/",
    # java/jvm, rust
    "target/",
    ".gradle/",
    # php, go, ruby
    "vendor/",
    # .net
    "obj/",
    ".vs/",
    # ide(s)
    ".idea/",
    ".vscode/",
    ".cursor/",
    # general build/output/temporary
    "build/",
    "dist/",
    "out/",
    "output/",
    "bin/",
    "logs/",
    "log/",
    "tmp/",
    "temp/",
    "coverage/",
    ".coverage/",
    ".cache/",
]
BINARY_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".bmp",
    ".tiff",
    ".ico",
    ".pdf",
    ".zip",
    ".tar",
    ".gz",
    ".svg",
    ".mp4",
    ".mp3",
    ".wav",
    ".ogg",
    ".mov",
    ".exe",
    ".dll",
    ".so",
    ".dylib",
    ".pyc",
    ".pkl",
    ".pickle",
    ".lock",
    ".woff",
    ".woff2",
    ".ttf",
    ".ds_store",
    ".env",
    ".env.local",
    ".env.development",
    ".env.production",
    ".env.test",
}


"""
Updated: March 2, 2025
Source: https://pypi.org/project/openai-whisper/
*--------*--------*--------*-------*------------*
| Model  | Params | VRAM   | Speed | Error Rate |
|--------|--------|--------|-------|------------|
| tiny   | 39M    | ~1 GB  | ~10x  | ~23.6%     |
| base   | 74M    | ~1 GB  | ~7x   | ~16.5%     |
| small  | 244M   | ~2 GB  | ~4x   | ~9.8%      |
| medium | 769M   | ~5 GB  | ~2x   | ~8.9%      |
| large  | 1,550M | ~10 GB | 1x    | ~7.9%      |
| turbo  | 809M   | ~6 GB  | ~8x   | ~7.7%      |
*--------*--------*--------*-------*------------*
"""
DEFAULT_WHISPER_MODEL_NAME = "tiny"

# set to "local" to use local whisper instead of openai api
TEXT_TO_SPEECH_MODEL = "whisper-1"

# support file formats
SUPPORTED_IMG_FORMATS = [".jpg", ".jpeg", ".png"]
SUPPORTED_PDF_FORMATS = [".pdf"]
SUPPORTED_DOC_FORMATS = [".doc", ".docx"]
SUPPORTED_SPREAD_SHEET_FORMATS = [".xls", ".xlsx"]
SUPPORTED_AUDIO_FORMATS = [
    ".mp3",
    ".mp4",
    ".wav",
    ".m4a",
    ".flac",
    ".ogg",
    ".webm",
]
SUPPORTED_VIDEO_FORMATS = [
    ".mp4",
    ".avi",
    ".mov",
    ".mkv",
    ".webm",
    ".flv",
    ".wmv",
    ".mpeg",
    ".mpg",
    ".m4v",
    ".ogv",
    ".3gp",
    ".3g2",
    ".asf",
    ".vob",
    ".rm",
    ".m2v",
    ".ts",
    ".mxf",
    ".f4v",
    ".divx",
    ".qt",
    ".amv",
    ".nsv",
    ".roq",
    ".svi",
    ".mod",
]

# last updated on 3-11-2025
THIRD_PARTY_PLATFORMS = {
    "groq": {
        "models": {
            "url": "https://api.groq.com/openai/v1/models",
            "headers": {
                "Authorization": f"Bearer {os.environ.get('GROQ_API_KEY')}",
                "Content-Type": "application/json",
            },
            "json_name_path": "data.id",
        },
        "base_url": "https://api.groq.com/openai/v1",
        "env_name": "GROQ_API_KEY",
        "docs": "https://console.groq.com/docs/overview",
    },
    "deepseek": {
        "models": {
            "url": "https://api.deepseek.com/models",
            "headers": {
                "Accept": "application/json",
                "Authorization": f"Bearer {os.environ.get('DEEP_SEEK_API_KEY')}",
            },
            "json_name_path": "data.id",
        },
        "base_url": "https://api.deepseek.com",
        "env_name": "DEEP_SEEK_API_KEY",
        "docs": "https://api-docs.deepseek.com/",
    },
    "together_ai": {
        "models": {
            "url": "https://api.together.xyz/v1/models",
            "headers": {
                "accept": "application/json",
                "authorization": f"Bearer {os.environ.get('TOGETHER_API_KEY')}",
            },
            "json_name_path": "id",
        },
        "base_url": "https://api.together.xyz/v1",
        "env_name": "TOGETHER_API_KEY",
        "docs": "https://docs.together.ai/docs/introduction",
    },
    "google": {
        "models": {
            "url": f"https://generativelanguage.googleapis.com/v1beta/models?key={os.environ.get('GEMINI_API_KEY')}",
            "headers": {},
            "json_name_path": "models.name",
        },
        "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/",
        "env_name": "GEMINI_API_KEY",
        "docs": "https://ai.google.dev/gemini-api/docs",
    },
    "ollama": {
        "models": {
            "url": "http://localhost:11434/api/tags",
            "headers": {},
            "json_name_path": "models.name",
        },
        "base_url": "http://localhost:11434/v1",
        "env_name": "ollama",
        "docs": "https://github.com/ollama/ollama/blob/main/docs/api.md",
    },
    "xai": {
        "models": {
            "url": "https://api.x.ai/v1/models",
            "headers": {
                "accept": "application/json",
                "authorization": f"Bearer {os.environ.get('XAI_API_KEY')}",
            },
            "json_name_path": "data.id",
        },
        "base_url": "https://api.x.ai/v1",
        "env_name": "XAI_API_KEY",
        "docs": "https://docs.x.ai/docs/overview",
    },
    "anthropic": {
        "models": {
            "url": "https://api.anthropic.com/v1/models",
            "headers": {
                "x-api-key": f"{os.environ.get('ANTHROPIC_API_KEY')}",
                "anthropic-version": "2023-06-01",
            },
            "json_name_path": "data.id",
        },
        "base_url": "https://api.anthropic.com/v1/",
        "env_name": "ANTHROPIC_API_KEY",
        "docs": "https://docs.anthropic.com/",
    },
}

# urls that contain video data that can be scrapped using cha's scraper
VALID_VIDEO_ROOT_URL_DOMAINS_FOR_SCRAPING = [
    "https://www.youtube.com",
    "https://youtube.com",
    "https://www.vimeo.com",
    "https://vimeo.com",
    "https://www.twitch.tv",
    "https://twitch.tv",
    "https://www.dailymotion.com",
    "https://dailymotion.com",
    "https://www.dropout.tv",
    "https://dropout.tv",
    "https://www.linkedin.com",
    "https://linkedin.com",
    "https://www.twitter.com",
    "https://twitter.com",
    "https://x.com",
    "https://www.cbsnews.com",
    "https://cbsnews.com",
    "https://www.cnn.com",
    "https://cnn.com",
    "https://www.cnbc.com",
    "https://cnbc.com",
    "https://www.abc.com.au",
    "https://abc.com.au",
    "https://www.bbc.co.uk",
    "https://bbc.co.uk",
    "https://www.cartoonnetwork.com",
    "https://cartoonnetwork.com",
    "https://www.canalplus.fr",
    "https://canalplus.fr",
    "https://www.arte.tv",
    "https://arte.tv",
    "https://www.cbc.ca",
    "https://cbc.ca",
    "https://www.3sat.de",
    "https://3sat.de",
    "https://www.ard.de",
    "https://ard.de",
]

"""
ascii, text based, terminal animations for loading animations
- https://stackoverflow.com/questions/2685435/cooler-ascii-spinners
- https://raw.githubusercontent.com/sindresorhus/cli-spinners/master/spinners.json
"""
LOADING_ANIMATIONS = {
    "basic": ["|", "/", "-", "\\"],
    "star": ["✶", "✸", "✹", "✺", "✹", "✷"],
    "vertical_bar": [
        "▉",
        "▊",
        "▋",
        "▌",
        "▍",
        "▎",
        "▏",
        "▎",
        "▍",
        "▌",
        "▋",
        "▊",
        "▉",
    ],
    "dots": ["▖", "▘", "▝", "▗"],
    "rectangles": ["◰", "◳", "◲", "◱"],
    "circles": ["◴", "◷", "◶", "◵"],
    "halfcircles": ["◐", "◓", "◑", "◒"],
    "braille": [
        "⣾",
        "⣽",
        "⣻",
        "⢿",
        "⡿",
        "⣟",
        "⣯",
        "⣷",
        "⠁",
        "⠂",
        "⠄",
        "⡀",
        "⢀",
        "⠠",
        "⠐",
        "⠈",
    ],
}

# last updated on March 29, 2025
FILETYPE_TO_EXTENSION = {
    "python": ".py",
    "py": ".py",
    "bash": ".sh",
    "sh": ".sh",
    "shell": ".sh",
    "zsh": ".zsh",
    "fish": ".fish",
    "powershell": ".ps1",
    "ps1": ".ps1",
    "bat": ".bat",
    "cmd": ".cmd",
    "javascript": ".js",
    "js": ".js",
    "typescript": ".ts",
    "ts": ".ts",
    "coffee": ".coffee",
    "vue": ".vue",
    "jsx": ".jsx",
    "tsx": ".tsx",
    "java": ".java",
    "c": ".c",
    "h": ".h",
    "hpp": ".hpp",
    "c++": ".cpp",
    "cpp": ".cpp",
    "cxx": ".cpp",
    "cc": ".cpp",
    "cs": ".cs",  # C#
    "go": ".go",
    "golang": ".go",
    "php": ".php",
    "rb": ".rb",  # Ruby
    "ruby": ".rb",
    "swift": ".swift",
    "kotlin": ".kt",
    "kt": ".kt",
    "rs": ".rs",  # Rust
    "rust": ".rs",
    "dart": ".dart",
    "r": ".r",
    "m": ".m",  # MATLAB/Objective-C
    "matlab": ".m",
    "mm": ".mm",  # Objective-C++
    "scala": ".scala",
    "lua": ".lua",
    "perl": ".pl",
    "pl": ".pl",
    "pm": ".pm",
    "tcl": ".tcl",
    "groovy": ".groovy",
    "gradle": ".gradle",
    "clojure": ".clj",
    "clj": ".clj",
    "cljs": ".cljs",
    "cljc": ".cljc",
    "fsharp": ".fs",
    "fs": ".fs",
    "elixir": ".ex",
    "ex": ".ex",
    "exs": ".exs",
    "asp": ".asp",
    "aspx": ".aspx",
    "jsp": ".jsp",
    "sas": ".sas",
    "d": ".d",  # D language
    "pas": ".pas",  # Pascal
    "pp": ".pp",  # Free Pascal
    "asm": ".asm",  # Assembly
    "s": ".s",
    "v": ".v",  # Verilog
    "sv": ".sv",  # SystemVerilog
    "vhd": ".vhd",
    "vhdl": ".vhdl",
    "cl": ".cl",  # OpenCL
    "html": ".html",
    "htm": ".htm",
    "css": ".css",
    "sass": ".sass",
    "scss": ".scss",
    "xml": ".xml",
    "svg": ".svg",
    "svgz": ".svgz",
    "yaml": ".yaml",
    "yml": ".yml",
    "toml": ".toml",
    "ini": ".ini",
    "cfg": ".cfg",
    "conf": ".conf",
    "json": ".json",
    "json5": ".json5",
    "jsonc": ".jsonc",
    "sql": ".sql",
    "tsql": ".sql",
    "pgsql": ".sql",
    "db2": ".sql",
    "csv": ".csv",
    "tsv": ".tsv",
    "proto": ".proto",
    "proto3": ".proto",
    "ipynb": ".ipynb",
    "md": ".md",
    "markdown": ".md",
    "rst": ".rst",
    "org": ".org",
    "latex": ".tex",
    "tex": ".tex",
    "rmd": ".Rmd",
    "rmarkdown": ".Rmd",
    "rproj": ".Rproj",
    "properties": ".properties",
    "inf": ".inf",
    "plist": ".plist",
    "txt": ".txt",
    "text": ".txt",
    "plaintext": ".txt",
    "rtf": ".rtf",
    "doc": ".doc",
    "docx": ".docx",
    "odt": ".odt",
    "ppt": ".ppt",
    "pptx": ".pptx",
    "pdf": ".pdf",
    "xls": ".xls",
    "xlsx": ".xlsx",
    "ods": ".ods",
    "rtfd": ".rtfd",
    "man": ".man",
    "makefile": ".makefile",
    "dockerfile": ".dockerfile",
    "docker-compose": ".yml",
    "gitignore": ".gitignore",
    "gitattributes": ".gitattributes",
    "editorconfig": ".editorconfig",
    "eslint": ".eslintrc.js",
    "eslintjson": ".eslintrc.json",
    "npmrc": ".npmrc",
    "babelrc": ".babelrc",
    "prettierrc": ".prettierrc",
    "gradlew": ".gradlew",
    "env": ".env",
    "nvmrc": ".nvmrc",
    "npmignore": ".npmignore",
    "dockerignore": ".dockerignore",
    "clang-format": ".clang-format",
    "clang-tidy": ".clang-tidy",
    "desktop": ".desktop",
    "service": ".service",
    "socket": ".socket",
    "timer": ".timer",
    "target": ".target",
    "jpg": ".jpg",
    "jpeg": ".jpeg",
    "png": ".png",
    "gif": ".gif",
    "bmp": ".bmp",
    "webp": ".webp",
    "ico": ".ico",
    "tiff": ".tiff",
    "tga": ".tga",
    "psd": ".psd",
    "xcf": ".xcf",
    "exr": ".exr",
    "hdr": ".hdr",
    "mp4": ".mp4",
    "mkv": ".mkv",
    "mov": ".mov",
    "avi": ".avi",
    "mpg": ".mpg",
    "mpeg": ".mpeg",
    "flv": ".flv",
    "f4v": ".f4v",
    "swf": ".swf",
    "mp3": ".mp3",
    "wav": ".wav",
    "flac": ".flac",
    "ogg": ".ogg",
    "wma": ".wma",
    "ape": ".ape",
    "aiff": ".aiff",
    "au": ".au",
    "caf": ".caf",
    "mid": ".mid",
    "midi": ".midi",
    "xm": ".xm",
    "it": ".it",
    "s3m": ".s3m",
    "mod": ".mod",
    "zip": ".zip",
    "7z": ".7z",
    "gz": ".gz",
    "xz": ".xz",
    "lz": ".lz",
    "lzma": ".lzma",
    "lzo": ".lzo",
    "lzop": ".lzop",
    "cpio": ".cpio",
    "z": ".z",
    "tar": ".tar",
    "tgz": ".tgz",
    "bz2": ".bz2",
    "rar": ".rar",
    "ps": ".ps",
    "eps": ".eps",
    "ai": ".ai",
}

NORMALIZED_LANGUAGE_MAPPING = {
    "AFRIKAANS": {"espeak_code": "af", "say_voice_name": None},
    "AMHARIC": {"espeak_code": "am", "say_voice_name": None},
    "ARAGONESE": {"espeak_code": "an", "say_voice_name": None},
    "ARABIC": {"espeak_code": "ar", "say_voice_name": "Majed"},
    "ASSAMESE": {"espeak_code": "as", "say_voice_name": None},
    "AZERBAIJANI": {"espeak_code": "az", "say_voice_name": None},
    "BELARUSIAN": {"espeak_code": "be", "say_voice_name": None},
    "BULGARIAN": {"espeak_code": "bg", "say_voice_name": "Daria"},
    "BENGALI": {"espeak_code": "bn", "say_voice_name": None},
    "BOSNIAN": {"espeak_code": "bs", "say_voice_name": None},
    "CATALAN": {"espeak_code": "ca", "say_voice_name": "Montse"},
    "CHINESE": {"espeak_code": "cmn", "say_voice_name": None},
    "CZECH": {"espeak_code": "cs", "say_voice_name": "Zuzana"},
    "WELSH": {"espeak_code": "cy", "say_voice_name": None},
    "DANISH": {"espeak_code": "da", "say_voice_name": "Sara"},
    "GERMAN": {"espeak_code": "de", "say_voice_name": "Shelley (German (Germany))"},
    "GREEK": {"espeak_code": "el", "say_voice_name": "Melina"},
    "ENGLISH": {"espeak_code": "en", "say_voice_name": "Karen"},
    "ESPERANTO": {"espeak_code": "eo", "say_voice_name": None},
    "SPANISH": {"espeak_code": "es", "say_voice_name": "Shelley (Spanish (Spain))"},
    "ESTONIAN": {"espeak_code": "et", "say_voice_name": None},
    "BASQUE": {"espeak_code": "eu", "say_voice_name": None},
    "PERSIAN": {"espeak_code": "fa", "say_voice_name": None},
    "FINNISH": {"espeak_code": "fi", "say_voice_name": "Shelley (Finnish (Finland))"},
    "FRENCH": {"espeak_code": "fr", "say_voice_name": "Thomas"},
    "IRISH": {"espeak_code": "ga", "say_voice_name": None},
    "SCOTTISH": {"espeak_code": "gd", "say_voice_name": None},
    "GUJARATI": {"espeak_code": "gu", "say_voice_name": None},
    "HEBREW": {"espeak_code": "he", "say_voice_name": "Carmit"},
    "HINDI": {"espeak_code": "hi", "say_voice_name": "Lekha"},
    "CROATIAN": {"espeak_code": "hr", "say_voice_name": "Lana"},
    "HUNGARIAN": {"espeak_code": "hu", "say_voice_name": "T\u00fcnde"},
    "ARMENIAN": {"espeak_code": "hy", "say_voice_name": None},
    "INDONESIAN": {"espeak_code": "id", "say_voice_name": "Damayanti"},
    "ICELANDIC": {"espeak_code": "is", "say_voice_name": None},
    "ITALIAN": {"espeak_code": "it", "say_voice_name": "Shelley (Italian (Italy))"},
    "JAPANESE": {"espeak_code": "ja", "say_voice_name": "Kyoko"},
    "GEORGIAN": {"espeak_code": "ka", "say_voice_name": None},
    "KANNADA": {"espeak_code": "kn", "say_voice_name": None},
    "KOREAN": {"espeak_code": "ko", "say_voice_name": "Yuna"},
    "KURDISH": {"espeak_code": "ku", "say_voice_name": None},
    "LATIN": {"espeak_code": "la", "say_voice_name": None},
    "LITHUANIAN": {"espeak_code": "lt", "say_voice_name": None},
    "LATVIAN": {"espeak_code": "lv", "say_voice_name": None},
    "MACEDONIAN": {"espeak_code": "mk", "say_voice_name": None},
    "MALAYALAM": {"espeak_code": "ml", "say_voice_name": None},
    "MARATHI": {"espeak_code": "mr", "say_voice_name": None},
    "MALAY": {"espeak_code": "ms", "say_voice_name": "Amira"},
    "MALTESE": {"espeak_code": "mt", "say_voice_name": None},
    "NORWEGIAN": {"espeak_code": "nb", "say_voice_name": "Nora"},
    "NEPALI": {"espeak_code": "ne", "say_voice_name": None},
    "DUTCH": {"espeak_code": "nl", "say_voice_name": "Xander"},
    "PUNJABI": {"espeak_code": "pa", "say_voice_name": None},
    "POLISH": {"espeak_code": "pl", "say_voice_name": "Zosia"},
    "PORTUGUESE": {"espeak_code": "pt", "say_voice_name": "Joana"},
    "ROMANIAN": {"espeak_code": "ro", "say_voice_name": "Ioana"},
    "RUSSIAN": {"espeak_code": "ru", "say_voice_name": "Milena"},
    "SINHALA": {"espeak_code": "si", "say_voice_name": None},
    "SLOVAK": {"espeak_code": "sk", "say_voice_name": "Laura"},
    "SLOVENIAN": {"espeak_code": "sl", "say_voice_name": None},
    "ALBANIAN": {"espeak_code": "sq", "say_voice_name": None},
    "SERBIAN": {"espeak_code": "sr", "say_voice_name": None},
    "SWEDISH": {"espeak_code": "sv", "say_voice_name": "Alva"},
    "SWAHILI": {"espeak_code": "sw", "say_voice_name": None},
    "TAMIL": {"espeak_code": "ta", "say_voice_name": None},
    "TELUGU": {"espeak_code": "te", "say_voice_name": None},
    "THAI": {"espeak_code": "th", "say_voice_name": "Kanya"},
    "TURKISH": {"espeak_code": "tr", "say_voice_name": "Yelda"},
    "UKRAINIAN": {"espeak_code": "uk", "say_voice_name": "Lesya"},
    "URDU": {"espeak_code": "ur", "say_voice_name": None},
    "VIETNAMESE": {"espeak_code": "vi", "say_voice_name": "Linh"},
}

# NOTE: do NOT modify the code below because it allows the loading of custom configs if provided!

TOOL_MOST_HAVE_VARIABLES = {
    "name": {"type": str, "required": True},
    "description": {"type": str, "required": True},
    "alias": {"type": str, "required": True},
    "include_history": {"type": [bool, int], "required": False, "default": False},
    "timeout_sec": {"type": int, "required": False, "default": 15},
    "pipe_input": {"type": bool, "required": False, "default": False},
    "pipe_output": {"type": bool, "required": False, "default": True},
    "show_loading_animation": {"type": bool, "required": False, "default": True},
}

LOCAL_CHA_CONFIG_DIR = os.path.join(str(Path.home()), ".cha/")
LOCAL_CHA_CONFIG_HISTORY_DIR = os.path.join(LOCAL_CHA_CONFIG_DIR, "history/")
LOCAL_CHA_CONFIG_TOOLS_DIR = os.path.join(LOCAL_CHA_CONFIG_DIR, "tools/")
LOCAL_CHA_CONFIG_FILE = os.path.join(LOCAL_CHA_CONFIG_DIR, "config.py")

_external_config_loaded = False


def _load_external_config():
    global _external_config_loaded
    if _external_config_loaded:
        return

    CUSTOM_CONFIG_PATH = os.environ.get("CHA_PYTHON_CUSTOM_CONFIG_PATH")
    OVERRIGHT_CONFIG = None
    if CUSTOM_CONFIG_PATH and os.path.exists(CUSTOM_CONFIG_PATH):
        OVERRIGHT_CONFIG = CUSTOM_CONFIG_PATH
    elif LOCAL_CHA_CONFIG_FILE and os.path.exists(LOCAL_CHA_CONFIG_FILE):
        OVERRIGHT_CONFIG = LOCAL_CHA_CONFIG_FILE

    if OVERRIGHT_CONFIG:
        spec = importlib.util.spec_from_file_location(
            "external_config", OVERRIGHT_CONFIG
        )
        external_config = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(external_config)

        for key, value in external_config.__dict__.items():
            if key.isupper():
                globals()[key] = value

    _external_config_loaded = True


def get_external_tools_execute():
    _load_external_config()

    if len(globals().get("EXTERNAL_TOOLS", [])) > 0:
        return local.get_tools()
    return []


CUSTOM_CONFIG_PATH = os.environ.get("CHA_PYTHON_CUSTOM_CONFIG_PATH")
OVERRIGHT_CONFIG = None
if CUSTOM_CONFIG_PATH and os.path.exists(CUSTOM_CONFIG_PATH):
    OVERRIGHT_CONFIG = CUSTOM_CONFIG_PATH
elif LOCAL_CHA_CONFIG_FILE and os.path.exists(LOCAL_CHA_CONFIG_FILE):
    OVERRIGHT_CONFIG = LOCAL_CHA_CONFIG_FILE

if OVERRIGHT_CONFIG != None:
    spec = importlib.util.spec_from_file_location("external_config", OVERRIGHT_CONFIG)
    external_config = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(external_config)

    for key, value in external_config.__dict__.items():
        if key.isupper() and key != "EXTERNAL_TOOLS":
            globals()[key] = value

EXTERNAL_TOOLS_EXECUTE = []
