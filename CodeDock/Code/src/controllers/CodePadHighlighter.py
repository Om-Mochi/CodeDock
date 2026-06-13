from PyQt6.QtWidgets import QApplication, QTextEdit, QMainWindow,QStyledItemDelegate,QLabel
from PyQt6.QtGui import QColor, QSyntaxHighlighter, QTextCharFormat, QFont,QStandardItemModel, QStandardItem,QTextDocument
from PyQt6.QtCore import QRegularExpression,Qt
import sys
import re

#from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor
#from PyQt5.QtCore import QRegularExpression
HEX_COLOR_RE = re.compile(r"#([0-9a-fA-F]{6})")

class IndentationHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)
        self.indent_format = QTextCharFormat()
        self.indent_format.setBackground(QColor(12,127,155, 100))  # Red with transparency

    def highlightBlock(self, text):
        # Match leading spaces (tabs or spaces)
        match = QRegularExpression(r"^(\s+)").match(text)
        if match.hasMatch():
            indent_length = len(match.captured(1))  # Get number of leading spaces
            self.setFormat(0, indent_length, self.indent_format)  # Apply red background


class CppHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)
        self.html_color_code = True
        self.i=0
        self.colors = {
            "language":".cpp",
            "keyword": "#597669",           # red-ish for keywords
            "type": "#82AAFF",             # blue for built-in types
            "class": "#82AAFF",            # blue for class names
            "function": "#89DDFF",         # light blue for function calls
            "def_func": "#C3E88D",         # green for function definitions
            "string": "#40974e",           # dark green for strings
            "comment": "#C3E88D",          # green for comments
            "number": "#C792EA",           # purple for numbers
            "constants": "#FFCB6B",        # yellow for constants/macros
            "brackets": "#8c518e",         # magenta for brackets
            "preprocessor": "#FFCB6B",     # yellow for preprocessor directives
            "namespace": "#82AAFF",        # blue for namespaces
            "method": "#FF5370",           # red-ish for methods (.something or ->something)
            "operator": "#333333",         # dark for operators
            "other": "#8fa0b0",           # default text color
        }
        self.setColors()
        

    def htmlColorCodeTagColorEnable(self, flag: bool = True):
        self.html_color_code = flag

    
    def setColors(self):
        # C++ Keywords
        self.keywords = [
            "auto", "break", "case", "catch", "class", "const", "continue", "default",
            "delete", "do", "else", "enum", "explicit", "extern", "false", "for",
            "friend", "goto", "if", "inline", "namespace", "new", "operator", "private",
            "protected", "public", "return", "sizeof", "static", "struct", "switch",
            "template", "this", "throw", "true", "try", "typedef", "typename", "union",
            "using", "virtual", "void", "volatile", "while", "constexpr", "decltype",
            "noexcept", "nullptr", "override", "final", "static_assert", "thread_local"
        ]
        
        # C++ Built-in types
        self.types = [
            "bool", "char", "char16_t", "char32_t", "double", "float", "int", "long",
            "short", "signed", "unsigned", "wchar_t", "size_t", "ptrdiff_t", "nullptr_t",
            "int8_t", "int16_t", "int32_t", "int64_t", "uint8_t", "uint16_t", "uint32_t",
            "uint64_t", "string", "vector", "map", "set", "list", "queue", "stack",
            "pair", "tuple", "shared_ptr", "unique_ptr", "weak_ptr"
        ]

        # Keyword format
        self.keyword_format = QTextCharFormat()
        self.keyword_format.setForeground(QColor(self.colors["keyword"]))
        self.keyword_patterns = [QRegularExpression(rf"\b{kw}\b") for kw in self.keywords]

        # Type format
        self.type_format = QTextCharFormat()
        self.type_format.setForeground(QColor(self.colors["type"]))
        #self.type_format.setForeground(QColor("Red"))
        
        self.type_patterns = [QRegularExpression(rf"\b{tp}\b") for tp in self.types]

        # Comments (single line // and multi-line /* */)
        self.comment_format = QTextCharFormat()
        self.comment_format.setForeground(QColor(self.colors["comment"]))
        self.single_comment_pattern = QRegularExpression(r"//.*")
        self.multi_comment_start = QRegularExpression(r"/\*")
        self.multi_comment_end = QRegularExpression(r"\*/")

        # Strings (double and single quotes, including escaped quotes)
        self.string_format = QTextCharFormat()
        self.string_format.setForeground(QColor(self.colors["string"]))
        self.string_pattern = QRegularExpression(r'"[^"\\]*(\\.[^"\\]*)*"|\'[^\'\\]*(\\.[^\'\\]*)*\'')

        # Character literals
        self.char_format = QTextCharFormat()
        self.char_format.setForeground(QColor(self.colors["string"]))
        self.char_pattern = QRegularExpression(r"'\\?.'")

        # Numbers (integers, floats, hex, binary)
        self.number_format = QTextCharFormat()
        self.number_format.setForeground(QColor(self.colors["number"]))
        self.number_pattern = QRegularExpression(r"\b(0x[0-9a-fA-F]+|0b[01]+|\d+(\.\d+)?([eE][+-]?\d+)?[fFlL]?)\b")

        # Constants and macros (all caps words)
        self.constant_format = QTextCharFormat()
        self.constant_format.setForeground(QColor(self.colors["constants"]))
        self.constant_pattern = QRegularExpression(r"\b[A-Z_][A-Z0-9_]*\b")

        # Brackets and parentheses
        self.bracket_format = QTextCharFormat()
        self.bracket_format.setForeground(QColor(self.colors["brackets"]))
        self.bracket_pattern = QRegularExpression(r"[\(\)\{\}\[\]]")

        # Preprocessor directives
        self.preprocessor_format = QTextCharFormat()
        self.preprocessor_format.setForeground(QColor(self.colors["preprocessor"]))
        self.preprocessor_pattern = QRegularExpression(r"#\w+")

        # Namespace usage (std::, etc.)
        self.namespace_format = QTextCharFormat()
        self.namespace_format.setForeground(QColor(self.colors["namespace"]))
        self.namespace_pattern = QRegularExpression(r"\b\w+(?=::)")

        # Function calls (word followed by opening parenthesis)
        self.function_format = QTextCharFormat()
        self.function_format.setForeground(QColor(self.colors["function"]))
        self.function_pattern = QRegularExpression(
            r"\b(?!if|for|while|switch|catch|sizeof|static_assert|decltype|noexcept)\w+(?=\s*\()"
        )

        # Class names (after 'class' keyword)
        self.class_name_format = QTextCharFormat()
        self.class_name_format.setForeground(QColor(self.colors["class"]))
        self.class_name_pattern = QRegularExpression(r"\bclass\s+(\w+)")

        # Function definitions (after return type and before parentheses)
        self.def_func_format = QTextCharFormat()
        self.def_func_format.setForeground(QColor(self.colors["def_func"]))
        # This pattern looks for function definitions (simplified)
        self.def_func_pattern = QRegularExpression(r"^\s*(?:\w+\s+)*?(\w+)\s*\([^)]*\)\s*[{;]")

        # Method calls (dot notation and arrow notation)
        self.method_format = QTextCharFormat()
        self.method_format.setForeground(QColor(self.colors["method"]))
        self.method_pattern = QRegularExpression(r"(?<=\.)\w+|(?<=->)\w+")

        # Operators
        self.operator_format = QTextCharFormat()
        self.operator_format.setForeground(QColor(self.colors["operator"]))
        self.operator_pattern = QRegularExpression(r"[=+\-*/%<>&|^~!,;:]|<<|>>|<=|>=|==|!=|&&|\|\||->|\+\+|--|::")

        # 'this' keyword (similar to 'self' in Python)
        self.this_format = QTextCharFormat()
        self.this_format.setForeground(QColor(self.colors["constants"]))
        self.this_pattern = QRegularExpression(r"\bthis\b")

    def applyFormat(self, text, pattern, fmt):
        iterator = pattern.globalMatch(text)
        while iterator.hasNext():
            match = iterator.next()
            self.setFormat(match.capturedStart(), match.capturedLength(), fmt)

    def highlightBlock(self, text):
        # Set default format
        default_format = QTextCharFormat()
        default_format.setForeground(QColor(self.colors['other']))
        self.setFormat(0, len(text), default_format)

        # Handle multi-line comments
        self.setCurrentBlockState(0)
        start_index = 0
        if self.previousBlockState() != 1:
            start_match = self.multi_comment_start.match(text)
            start_index = start_match.capturedStart() if start_match.hasMatch() else -1

        while start_index >= 0:
            end_match = self.multi_comment_end.match(text, start_index)
            if end_match.hasMatch():
                comment_length = end_match.capturedEnd() - start_index
                self.setFormat(start_index, comment_length, self.comment_format)
                start_match = self.multi_comment_start.match(text, end_match.capturedEnd())
                start_index = start_match.capturedStart() if start_match.hasMatch() else -1
            else:
                self.setCurrentBlockState(1)
                self.setFormat(start_index, len(text) - start_index, self.comment_format)
                break

        # Apply other formats (order matters for precedence)
        
        # Keywords
        for pattern in self.keyword_patterns:

            self.applyFormat(text, pattern, self.keyword_format)
        
        # Types
        for pattern in self.type_patterns:
            self.applyFormat(text, pattern, self.type_format)
        
        # Constants/Macros
        self.applyFormat(text, self.constant_pattern, self.constant_format)
        
        # Brackets
        self.applyFormat(text, self.bracket_pattern, self.bracket_format)
        
        # Namespace
        self.applyFormat(text, self.namespace_pattern, self.namespace_format)
        
        # Function calls
        self.applyFormat(text, self.function_pattern, self.function_format)
        
        # Method calls
        self.applyFormat(text, self.method_pattern, self.method_format)
        
        # 'this' keyword
        self.applyFormat(text, self.this_pattern, self.this_format)
        
        # Preprocessor directives
        self.applyFormat(text, self.preprocessor_pattern, self.preprocessor_format)
        
        # Numbers
        self.applyFormat(text, self.number_pattern, self.number_format)
        
        # Operators
        self.applyFormat(text, self.operator_pattern, self.operator_format)

        # Class names (capture group 1)
        iterator = self.class_name_pattern.globalMatch(text)
        while iterator.hasNext():
            match = iterator.next()
            name_start = match.capturedStart(1)
            name_len = len(match.captured(1))
            self.setFormat(name_start, name_len, self.class_name_format)

        # Function definitions (capture group 1)
        iterator = self.def_func_pattern.globalMatch(text)
        while iterator.hasNext():
            match = iterator.next()
            name_start = match.capturedStart(1)
            name_len = len(match.captured(1))
            self.setFormat(name_start, name_len, self.def_func_format)

        # Apply strings and comments last to override other formatting
        self.applyFormat(text, self.string_pattern, self.string_format)
        self.applyFormat(text, self.char_pattern, self.char_format)
        self.applyFormat(text, self.single_comment_pattern, self.comment_format)

        # Handle hex color codes if enabled
        if self.html_color_code:
            hex_color_pattern = QRegularExpression(r"#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})")
            iterator = hex_color_pattern.globalMatch(text)
            while iterator.hasNext():
                match = iterator.next()
                hex_code = match.captured(1)
                start = match.capturedStart()
                if QColor(f"#{hex_code}").isValid():
                    fmt = QTextCharFormat()
                    fmt.setForeground(QColor(f"#{hex_code}"))
                    self.setFormat(start, 1, fmt)  # only highlight '#'

class RustHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)
        self.html_color_code = True
        self.colors = {
            "language": ".rs",
            "keyword": "#597669",           # red-ish for keywords
            "type": "#82AAFF",             # blue for built-in types
            "struct": "#82AAFF",           # blue for struct/enum names
            "function": "#89DDFF",         # light blue for function calls
            "def_func": "#C3E88D",         # green for function definitions
            "string": "#40974e",           # dark green for strings
            "comment": "#C3E88D",          # green for comments
            "number": "#C792EA",           # purple for numbers
            "constants": "#FFCB6B",        # yellow for constants/macros
            "brackets": "#8c518e",         # magenta for brackets
            "macro": "#FFCB6B",            # yellow for macros
            "module": "#82AAFF",           # blue for modules
            "method": "#FF5370",           # red-ish for methods (.something)
            "operator": "#333333",         # dark for operators
            "lifetime": "#C792EA",         # purple for lifetimes
            "attribute": "#FFCB6B",        # yellow for attributes
            "other": "#8fa0b0",            # default text color
        }
        self.setColors()

    def htmlColorCodeTagColorEnable(self, flag: bool = True):
        self.html_color_code = flag

    def setColors(self):
        # Rust Keywords
        self.keywords = [
            "as", "async", "await", "break", "const", "continue", "crate", "dyn",
            "else", "enum", "extern", "false", "fn", "for", "if", "impl", "in",
            "let", "loop", "match", "mod", "move", "mut", "pub", "ref", "return",
            "self", "Self", "static", "struct", "super", "trait", "true", "type",
            "union", "unsafe", "use", "where", "while", "abstract", "become",
            "box", "do", "final", "macro", "override", "priv", "typeof", "unsized",
            "virtual", "yield", "try"
        ]
        
        # Rust Built-in types
        self.types = [
            "bool", "char", "str", "i8", "i16", "i32", "i64", "i128", "isize",
            "u8", "u16", "u32", "u64", "u128", "usize", "f32", "f64",
            "String", "Vec", "HashMap", "HashSet", "BTreeMap", "BTreeSet",
            "Option", "Result", "Box", "Rc", "Arc", "Cell", "RefCell",
            "Mutex", "RwLock", "Path", "PathBuf", "OsString", "CString"
        ]

        # Keyword format
        self.keyword_format = QTextCharFormat()
        self.keyword_format.setForeground(QColor(self.colors["keyword"]))
        self.keyword_patterns = [QRegularExpression(rf"\b{kw}\b") for kw in self.keywords]

        # Type format
        self.type_format = QTextCharFormat()
        self.type_format.setForeground(QColor(self.colors["type"]))
        self.type_patterns = [QRegularExpression(rf"\b{tp}\b") for tp in self.types]

        # Comments (single line // and multi-line /* */)
        self.comment_format = QTextCharFormat()
        self.comment_format.setForeground(QColor(self.colors["comment"]))
        self.single_comment_pattern = QRegularExpression(r"//.*")
        self.multi_comment_start = QRegularExpression(r"/\*")
        self.multi_comment_end = QRegularExpression(r"\*/")
        self.doc_comment_pattern = QRegularExpression(r"///.*")

        # Strings (double quotes, raw strings, byte strings)
        self.string_format = QTextCharFormat()
        self.string_format.setForeground(QColor(self.colors["string"]))
        # Regular strings and raw strings
        self.string_pattern = QRegularExpression(r'"[^"\\]*(\\.[^"\\]*)*"|r#*".*?"#*')
        # Byte strings
        self.byte_string_pattern = QRegularExpression(r'b"[^"\\]*(\\.[^"\\]*)*"|br#*".*?"#*')

        # Character literals
        self.char_format = QTextCharFormat()
        self.char_format.setForeground(QColor(self.colors["string"]))
        self.char_pattern = QRegularExpression(r"'([^'\\]|\\.)'")

        # Numbers (integers, floats, with suffixes)
        self.number_format = QTextCharFormat()
        self.number_format.setForeground(QColor(self.colors["number"]))
        self.number_pattern = QRegularExpression(r"\b(0x[0-9a-fA-F_]+|0b[01_]+|0o[0-7_]+|\d[\d_]*(\.\d[\d_]*)?([eE][+-]?\d+)?)[fi]?(8|16|32|64|128|size)?\b")

        # Constants and SCREAMING_SNAKE_CASE
        self.constant_format = QTextCharFormat()
        self.constant_format.setForeground(QColor(self.colors["constants"]))
        self.constant_pattern = QRegularExpression(r"\b[A-Z_][A-Z0-9_]*\b")

        # Brackets and parentheses
        self.bracket_format = QTextCharFormat()
        self.bracket_format.setForeground(QColor(self.colors["brackets"]))
        self.bracket_pattern = QRegularExpression(r"[\(\)\{\}\[\]]")

        # Macros (ending with !)
        self.macro_format = QTextCharFormat()
        self.macro_format.setForeground(QColor(self.colors["macro"]))
        self.macro_pattern = QRegularExpression(r"\b\w+!")

        # Attributes (#[...] and #![...])
        self.attribute_format = QTextCharFormat()
        self.attribute_format.setForeground(QColor(self.colors["attribute"]))
        self.attribute_pattern = QRegularExpression(r"#!?\[[^\]]*\]")

        # Lifetimes ('a, 'static, etc.)
        self.lifetime_format = QTextCharFormat()
        self.lifetime_format.setForeground(QColor(self.colors["lifetime"]))
        self.lifetime_pattern = QRegularExpression(r"'\w+\b")
       
        # Module paths (crate::, super::, self::)
        self.module_format = QTextCharFormat()
        self.module_format.setForeground(QColor(self.colors["module"]))
        self.module_pattern = QRegularExpression(r"\b\w+(?=::)")

        # Function calls (word followed by opening parenthesis, excluding keywords)
        self.function_format = QTextCharFormat()
        self.function_format.setForeground(QColor(self.colors["function"]))
        excluded_keywords = "|".join(["if", "for", "while", "match", "loop"])
        self.function_pattern = QRegularExpression(
            rf"\b(?!{excluded_keywords})\w+(?=\s*\()"
        )

        # Struct/Enum names (after 'struct', 'enum', 'trait' keywords)
        self.struct_name_format = QTextCharFormat()
        self.struct_name_format.setForeground(QColor(self.colors["struct"]))
        self.struct_name_pattern = QRegularExpression(r"\b(?:struct|enum|trait|impl)\s+(\w+)")

        # Function definitions (fn keyword followed by name)
        self.def_func_format = QTextCharFormat()
        self.def_func_format.setForeground(QColor(self.colors["def_func"]))
        self.def_func_pattern = QRegularExpression(r"\bfn\s+(\w+)")

        # Method calls (dot notation)
        self.method_format = QTextCharFormat()
        self.method_format.setForeground(QColor(self.colors["method"]))
        self.method_pattern = QRegularExpression(r"(?<=\.)\w+")

        # Operators (Rust-specific)
        self.operator_format = QTextCharFormat()
        self.operator_format.setForeground(QColor(self.colors["operator"]))
        self.operator_pattern = QRegularExpression(r"[=+\-*/%<>&|^~!,;:]|<<|>>|<=|>=|==|!=|&&|\|\||->|\+\+|--|::|\.\.=?|\?|@")

    def applyFormat(self, text, pattern, fmt):
        iterator = pattern.globalMatch(text)
        while iterator.hasNext():
            match = iterator.next()
            self.setFormat(match.capturedStart(), match.capturedLength(), fmt)

    def highlightBlock(self, text):
        # Set default format
        default_format = QTextCharFormat()
        default_format.setForeground(QColor(self.colors['other']))
        self.setFormat(0, len(text), default_format)

        # Handle multi-line comments
        self.setCurrentBlockState(0)
        start_index = 0
        if self.previousBlockState() != 1:
            start_match = self.multi_comment_start.match(text)
            start_index = start_match.capturedStart() if start_match.hasMatch() else -1

        while start_index >= 0:
            end_match = self.multi_comment_end.match(text, start_index)
            if end_match.hasMatch():
                comment_length = end_match.capturedEnd() - start_index
                self.setFormat(start_index, comment_length, self.comment_format)
                start_match = self.multi_comment_start.match(text, end_match.capturedEnd())
                start_index = start_match.capturedStart() if start_match.hasMatch() else -1
            else:
                self.setCurrentBlockState(1)
                self.setFormat(start_index, len(text) - start_index, self.comment_format)
                break

        # Apply other formats (order matters for precedence)
        
        # Keywords
        for pattern in self.keyword_patterns:
            self.applyFormat(text, pattern, self.keyword_format)
        
        # Types
        for pattern in self.type_patterns:
            self.applyFormat(text, pattern, self.type_format)
        
        # Attributes
        self.applyFormat(text, self.attribute_pattern, self.attribute_format)
        
        # Macros
        self.applyFormat(text, self.macro_pattern, self.macro_format)
        
        # Constants
        self.applyFormat(text, self.constant_pattern, self.constant_format)
        
        # Brackets
        self.applyFormat(text, self.bracket_pattern, self.bracket_format)
        
        # Lifetimes
        self.applyFormat(text, self.lifetime_pattern, self.lifetime_format)
        
        # Module paths
        self.applyFormat(text, self.module_pattern, self.module_format)
        
        # Function calls
        self.applyFormat(text, self.function_pattern, self.function_format)
        
        # Method calls
        self.applyFormat(text, self.method_pattern, self.method_format)
        
        # Operators
        self.applyFormat(text, self.operator_pattern, self.operator_format)
        
        # Numbers
        self.applyFormat(text, self.number_pattern, self.number_format)
        

        # Struct/Enum/Trait names (capture group 1)
        iterator = self.struct_name_pattern.globalMatch(text)
        while iterator.hasNext():
            match = iterator.next()
            name_start = match.capturedStart(1)
            name_len = len(match.captured(1))
            self.setFormat(name_start, name_len, self.struct_name_format)

        # Function definitions (capture group 1)
        iterator = self.def_func_pattern.globalMatch(text)
        while iterator.hasNext():
            match = iterator.next()
            name_start = match.capturedStart(1)
            name_len = len(match.captured(1))
            self.setFormat(name_start, name_len, self.def_func_format)

        # Apply strings and comments last to override other formatting
        self.applyFormat(text, self.string_pattern, self.string_format)
        self.applyFormat(text, self.byte_string_pattern, self.string_format)
        self.applyFormat(text, self.char_pattern, self.char_format)
        self.applyFormat(text, self.single_comment_pattern, self.comment_format)
        self.applyFormat(text, self.doc_comment_pattern, self.comment_format)

        # Handle hex color codes if enabled
        if self.html_color_code:
            hex_color_pattern = QRegularExpression(r"#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})")
            iterator = hex_color_pattern.globalMatch(text)
            while iterator.hasNext():
                match = iterator.next()
                hex_code = match.captured(1)
                start = match.capturedStart()
                if QColor(f"#{hex_code}").isValid():
                    fmt = QTextCharFormat()
                    fmt.setForeground(QColor(f"#{hex_code}"))
                    self.setFormat(start, 1, fmt)  # only highlight '#'
                    
class PythonHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)
        self.html_color_code=True
        self.colors = {
            "language":".py",
            "keyword": "#597669",     # red-ish for keywords
            "class": "#82AAFF",       # blue for class names
            "function": "#89DDFF",    # light blue for function calls
            "def_func": "#C3E88D",    # green for function definitions
            "string": "#40974e",      # dark green for strings
            "comment": "#C3E88D",     # green for comments
            "number": "#C792EA",      # purple for numbers
            "constants": "#FFCB6B",    # yellow for True, False, None
            "brackets": "#8c518e",    # magenta for brackets
            "self": "#FFCB6B",        # yellow for 'self'
            "object": "#82AAFF",      # blue for object attributes
            "method": "#FF5370",      # red-ish for methods (.something)
            "method_call": "#FF5370", # red-ish for method calls
            "other": "#8fa0b0",
            "operator":'#333333',
        }
        self.setColors()
        
    def htmlColorCodeTagColorEnable(self,flag:bool=True):
        self.html_color_code=flag

    def setColors(self):
        # Format for keywords
        self.keywords = [
            "def", "class", "return", "import", "from", "if", "else", "elif", "for", "while",
            "break", "continue", "try", "except", "with", "as", "lambda"
        ]
        self.keyword_format = QTextCharFormat()
        self.keyword_format.setForeground(QColor(self.colors["keyword"]))
        self.keyword_patterns = [QRegularExpression(rf"\b{kw}\b") for kw in self.keywords]

        self.comment_format = QTextCharFormat()
        self.comment_format.setForeground(QColor(self.colors["comment"]))
        self.comment_pattern = QRegularExpression(r"#.*")

        self.string_format = QTextCharFormat()
        self.string_format.setForeground(QColor(self.colors["string"]))
        self.string_pattern = QRegularExpression(r'"[^"\\]*(\\.[^"\\]*)*"|\'[^\']*\'')

        self.number_format = QTextCharFormat()
        self.number_format.setForeground(QColor(self.colors["number"]))
        self.number_pattern = QRegularExpression(r"\b\d+(\.\d+)?\b")

        self.constant_format = QTextCharFormat()
        self.constant_format.setForeground(QColor(self.colors["constants"]))
        self.constant_pattern = QRegularExpression(r"\b(True|False|None)\b")

        self.bracket_format = QTextCharFormat()
        self.bracket_format.setForeground(QColor(self.colors["brackets"]))
        self.bracket_pattern = QRegularExpression(r"[\(\)\{\}\[\]]")

        self.self_format = QTextCharFormat()
        self.self_format.setForeground(QColor(self.colors["self"]))
        self.self_pattern = QRegularExpression(r"\bself\b")

        self.object_format = QTextCharFormat()
        self.object_format.setForeground(QColor(self.colors["object"]))
        self.object_pattern = QRegularExpression(r"\b\w+(?=\.)")

        self.method_format = QTextCharFormat()
        self.method_format.setForeground(QColor(self.colors["method"]))
        self.method_pattern = QRegularExpression(r"\.\w+")

        self.function_format = QTextCharFormat()
        self.function_format.setForeground(QColor(self.colors["function"]))
        self.function_pattern = QRegularExpression(
            r"(?<!def\s)(?<!class\s)\b(?!return|if|else|elif|for|while|break|continue|try|except|with|as|lambda)\w+(?=\s*\()"
        )

        self.class_name_format = QTextCharFormat()
        self.class_name_format.setForeground(QColor(self.colors["class"]))
        self.class_name_pattern = QRegularExpression(r"\bclass\s+(\w+)")

        self.def_func_format = QTextCharFormat()
        self.def_func_format.setForeground(QColor(self.colors["def_func"]))
        self.def_func_pattern = QRegularExpression(r"\bdef\s+(\w+)")

        self.method_call_format = QTextCharFormat()
        self.method_call_format.setForeground(QColor(self.colors["method_call"]))
        self.method_call_pattern = QRegularExpression(r"(?<=\.)\w+(?=\s*\()")

        self.operator_format = QTextCharFormat()
        self.operator_format.setForeground(QColor(self.colors["operator"]))

        # Pattern for common operators (excluding brackets)
        self.operator_pattern = QRegularExpression(r"[=+\-*/%<>&|^~,:\.]")


    def applyFormat(self, text, pattern, fmt):
        
        iterator = pattern.globalMatch(text)
        while iterator.hasNext():
            match = iterator.next()
            self.setFormat(match.capturedStart(), match.capturedLength(), fmt)

    def highlightBlock(self, text):
        default_format = QTextCharFormat()
        default_format.setForeground(QColor(self.colors['other']))  # default color for non-highlighted text
        self.setFormat(0, len(text), default_format)
        for pattern in self.keyword_patterns:
            iterator = pattern.globalMatch(text)
            while iterator.hasNext():
                match = iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), self.keyword_format)
        
        self.applyFormat(text, self.number_pattern, self.number_format)
        self.applyFormat(text, self.constant_pattern, self.constant_format)
        self.applyFormat(text, self.bracket_pattern, self.bracket_format)
        self.applyFormat(text, self.object_pattern, self.object_format)
        self.applyFormat(text, self.method_pattern, self.method_format)
        self.applyFormat(text, self.function_pattern, self.function_format)
        self.applyFormat(text, self.method_call_pattern, self.method_call_format)
        self.applyFormat(text, self.self_pattern, self.self_format)
        self.applyFormat(text, self.operator_pattern, self.operator_format)
        self.applyFormat(text, self.operator_pattern, self.operator_format)

        self.applyFormat(text, self.string_pattern, self.string_format)
        self.applyFormat(text, self.comment_pattern, self.comment_format)

        # Highlight class names (e.g., Test in class Test:)
        iterator = self.class_name_pattern.globalMatch(text)
        while iterator.hasNext():
            match = iterator.next()
            name_start = match.capturedStart(1)
            name_len = len(match.captured(1))
            self.setFormat(name_start, name_len, self.class_name_format)

        # Highlight function names (e.g., my_func in def my_func())
        iterator = self.def_func_pattern.globalMatch(text)
        while iterator.hasNext():
            match = iterator.next()
            name_start = match.capturedStart(1)
            name_len = len(match.captured(1))
            self.setFormat(name_start, name_len, self.def_func_format)

        if self.html_color_code==True:
                
            for match in HEX_COLOR_RE.finditer(text):
                hex_code = match.group(1)
                start = match.start()
                if QColor(f"#{hex_code}").isValid():
                    fmt = QTextCharFormat()
                    fmt.setForeground(QColor(f"#{hex_code}"))
                    self.setFormat(start, 1, fmt)  # only highlight '#'


class HTMLDelegate(QStyledItemDelegate):
    def __init__(self,parent,font_size):
        super().__init__(parent)
        self.font_size=font_size
    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)

        option.font.setPointSize(self.font_size)
    def paint(self, painter, option, index):
        # Render the text with HTML formatting
        """option.rect.setTop(option.rect.top() + 10)  # Add top spacing
        option.rect.setBottom(option.rect.bottom() - 10)  # Add bottom spacing
        """
        
        painter.save()
        text = index.data(Qt.ItemDataRole.DisplayRole)
        if text:
            # Use the QTextDocument for rendering HTML
            from PyQt6.QtGui import QTextDocument
            doc = QTextDocument()
            doc.setHtml(text)
            # Draw the HTML-rendered content
            painter.translate(option.rect.topLeft())
            doc.drawContents(painter)
        painter.restore()

    def sizeHint(self, option, index):
        from PyQt6.QtGui import QTextDocument
        text = index.data(Qt.ItemDataRole.DisplayRole)
        doc = QTextDocument()
        doc.setHtml(text)
        return doc.size().toSize()



class SignatureHighlighter(PythonHighlighter):
    def __init__(self, document):
        super().__init__(document)
        self.active_param = None
        self
        self.param_format = QTextCharFormat()
        self.param_format.setForeground(QColor("#FFD064"))
        self.param_format.setFontWeight(QFont.Weight.Bold)

    def set_active_param(self, param_name):
        self.active_param = param_name
        self.rehighlight()

    def highlightBlock(self, text):
        # 1. Call base class for Python highlighting
        super().highlightBlock(text)

        # 2. Add parameter highlighting logic
        if not self.active_param:
            return

        pattern = QRegularExpression(
            rf'\b{QRegularExpression.escape(self.active_param)}(\s*:\s*\w+)?\b'
        )
        match_iter = pattern.globalMatch(text)
        while match_iter.hasNext():
            match = match_iter.next()
            self.setFormat(
                match.capturedStart(),
                match.capturedLength(),
                self.param_format
        )
if __name__ == "__main__":
    class MainWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Syntax Highlighter Test")
            
            # Set up the text editor
            self.textedit_for_code_editor = QLabel()
            self.textedit_for_code_editor.setText("# Sample Python Code\n\ndef example():\n    x = 42\n    print('Hello, world!')\n")
            self.setCentralWidget(self.textedit_for_code_editor)
            
            # Set up syntax highlighting
            self.highlighter = PythonHighlighter(self.textedit_for_code_editor.document())
            
            
  
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
