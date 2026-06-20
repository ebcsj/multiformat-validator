from .json_validator import validate_json
from .py_validator import validate_python
from .html_validator import validate_html
from .xml_validator import validate_xml
from .batcmd_validator import validate_bat
from .css_validator import validate_css
from .js_validator import validate_javascript
from .yaml_validator import validate_yaml
from .md_validator import validate_markdown
from .sql_validator import validate_sql
from .php_validator import validate_php
from .ini_validator import validate_ini
from .java_validator import validate_java
from .cs_validator import validate_csharp
from .go_validator import validate_go
from .ts_validator import validate_typescript
from .ruby_validator import validate_ruby
from .rust_validator import validate_rust
from .kotlin_validator import validate_kotlin
from .swift_validator import validate_swift
from .perl_validator import validate_perl
from .lua_validator import validate_lua
from .scala_validator import validate_scala

VALIDATORS = {
    ".json": validate_json, ".ipynb": validate_json, ".jsonl": validate_json, ".topojson": validate_json, ".geojson": validate_json,
    ".py": validate_python, ".pyw": validate_python, ".pyi": validate_python, ".pyx": validate_python,
    ".html": validate_html, ".htm": validate_html, ".xhtml": validate_html, ".phtml": validate_html, ".jsp": validate_html, ".asp": validate_html, ".aspx": validate_html,
    ".xml": validate_xml, ".xsd": validate_xml, ".rss": validate_xml, ".svg": validate_xml, ".plist": validate_xml, ".config": validate_xml, ".wsdl": validate_xml,
    ".bat": validate_bat, ".cmd": validate_bat, ".nt": validate_bat,
    ".php": validate_php, ".php3": validate_php, ".php4": validate_php, ".php5": validate_php, ".phps": validate_php,
    ".css": validate_css, ".wxss": validate_css,
    ".md": validate_markdown, ".markdown": validate_markdown, ".mdown": validate_markdown, ".mdwn": validate_markdown, ".mkd": validate_markdown, ".mkdn": validate_markdown,
    ".ini": validate_ini, ".properties": validate_ini, ".conf": validate_ini, ".cfg": validate_ini, ".prefs": validate_ini, ".inf": validate_ini,
    ".js": validate_javascript, ".jsx": validate_javascript,
    ".ts": validate_typescript, ".tsx": validate_typescript,
    ".java": validate_java,
    ".cs": validate_csharp,
    ".go": validate_go,
    ".rb": validate_ruby,
    ".rs": validate_rust,
    ".kt": validate_kotlin,
    ".swift": validate_swift,
    ".pl": validate_perl, ".pm": validate_perl,
    ".lua": validate_lua,
    ".scala": validate_scala,
    ".yml": validate_yaml, ".yaml": validate_yaml,
    ".sql": validate_sql,
}
