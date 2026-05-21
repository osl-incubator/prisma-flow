"""Exceptions raised by prisma-flow."""


class PrismaFlowError(Exception):
    """Base exception for prisma-flow errors."""


class TemplateNotSupportedError(PrismaFlowError):
    """Raised when a requested PRISMA template is not implemented."""


class OptionalDependencyError(PrismaFlowError):
    """Raised when an optional export backend is not installed."""


class PrismaValidationError(PrismaFlowError):
    """Raised when a flow has validation errors."""
