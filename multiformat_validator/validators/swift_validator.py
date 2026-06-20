from .common import check_brackets, make_result


def validate_swift(content: str) -> dict:
    return make_result(check_brackets(
        content.split("\n"), prefix="Swift",
        comment_prefixes=("//", "/*"), skip_star=True,
    ))
