from .common import check_brackets, make_result


def validate_rust(content: str) -> dict:
    return make_result(check_brackets(
        content.split("\n"), prefix="Rust",
        comment_prefixes=("//", "/*"), skip_star=True,
    ))
