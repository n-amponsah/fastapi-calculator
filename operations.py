import logging

logger = logging.getLogger(__name__)


def add(a: float, b: float) -> float:
    result = a + b
    logger.info(f"ADD: {a} + {b} = {result}")
    return result


def subtract(a: float, b: float) -> float:
    result = a - b
    logger.info(f"SUBTRACT: {a} - {b} = {result}")
    return result


def multiply(a: float, b: float) -> float:
    result = a * b
    logger.info(f"MULTIPLY: {a} * {b} = {result}")
    return result


def divide(a: float, b: float) -> float:
    if b == 0:
        logger.error(f"DIVIDE: division by zero attempted")
        raise ValueError("Cannot divide by zero")
    result = a / b
    logger.info(f"DIVIDE: {a} / {b} = {result}")
    return result


def power(a: float, b: float) -> float:
    result = a ** b
    logger.info(f"POWER: {a} ^ {b} = {result}")
    return result


def modulo(a: float, b: float) -> float:
    if b == 0:
        logger.error(f"MODULO: modulo by zero attempted")
        raise ValueError("Cannot perform modulo by zero")
    result = a % b
    logger.info(f"MODULO: {a} % {b} = {result}")
    return result
