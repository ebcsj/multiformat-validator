from .common import check_brackets, make_result


def validate_sql(content: str) -> dict:
    return make_result(check_brackets(
        content.split("\n"), prefix="SQL",
        comment_prefixes=("--", "/*"),
        check_parens=True, check_braces=False, check_brackets=False,
    ))
