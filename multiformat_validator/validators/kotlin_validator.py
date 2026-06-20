from .common import check_brackets, make_result


def validate_kotlin(content: str) -> dict:
    return make_result(check_brackets(
        content.split("\n"), prefix="Kotlin",
        comment_prefixes=("//", "/*"), skip_star=True,
    ))
