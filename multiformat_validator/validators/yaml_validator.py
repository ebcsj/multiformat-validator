from .common import ValidationError, make_result


def validate_yaml(content: str) -> dict:
    errors: list[ValidationError] = []

    try:
        import yaml
    except ImportError:
        errors.append(ValidationError(
            type="YAMLMissingDependency", line=0, col=0,
            message="PyYAML not installed. Run: pip install pyyaml",
            fix="Install pyyaml package: pip install pyyaml",
        ))
        return make_result(errors)

    try:
        yaml.safe_load(content)
    except yaml.YAMLError as e:
        line = col = 0
        if hasattr(e, "problem_mark") and e.problem_mark:
            line = e.problem_mark.line + 1
            col = e.problem_mark.column + 1
        errors.append(ValidationError(
            type="YAMLSyntaxError", line=line, col=col,
            message=str(e.problem) if hasattr(e, "problem") else str(e),
            fix="Check YAML syntax: ensure proper indentation and structure.",
        ))

    return make_result(errors)
