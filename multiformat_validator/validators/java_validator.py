from .common import check_brackets, make_result


def validate_java(content: str) -> dict:
    return make_result(check_brackets(
        content.split("\n"), prefix="Java",
        comment_prefixes=("//", "/*"), skip_star=True,
    ))
