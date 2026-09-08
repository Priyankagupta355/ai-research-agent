def calculate(expression: str) -> str:
    """
    Calculate a mathematical expression.
    """

    try:
        result = eval(expression)
        return str(result)

    except Exception as e:
        return f"Error: {str(e)}"