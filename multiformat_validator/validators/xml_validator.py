import xml.sax
import xml.sax.handler

from .common import ValidationError, make_result


class _SafeXMLHandler(xml.sax.ContentHandler):
    """仅用于语法结构检查的 SAX Handler，不加载任何外部实体"""
    pass


def validate_xml(content: str) -> dict:
    errors: list[ValidationError] = []
    try:
        parser = xml.sax.make_parser()
        parser.setFeature(xml.sax.handler.feature_external_ges, False)
        parser.setFeature(xml.sax.handler.feature_external_pes, False)
        parser.setContentHandler(_SafeXMLHandler())
        parser.parseString(content)
    except xml.sax.SAXParseException as e:
        errors.append(ValidationError(
            type="XMLSyntaxError", line=e.getLineNumber(), col=e.getColumnNumber(),
            message=e.getMessage(),
            fix="Check XML syntax: ensure all tags are properly closed and nested.",
        ))
    except Exception as e:
        errors.append(ValidationError(
            type="XMLSyntaxError", line=0, col=0,
            message=str(e),
            fix="Check XML syntax: ensure all tags are properly closed and nested.",
        ))
    return make_result(errors)
