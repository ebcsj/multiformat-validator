from .common import check_brackets, make_result


def validate_go(content: str) -> dict:
    return make_result(check_brackets(
        content.split("\n"), prefix="Go",
        comment_prefixes=("//", "/*"), skip_star=True,
    ))
