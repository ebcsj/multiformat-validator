from .common import check_brackets, make_result


def validate_javascript(content: str) -> dict:
    return make_result(check_brackets(
        content.split("\n"), prefix="JS",
        comment_prefixes=("//", "/*"), skip_star=False,
    ))
