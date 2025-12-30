"""
Domain Exceptions
"""

class DomainException(Exception):
    """도메인 레이어 기본 예외"""
    pass

class AIAnalysisError(DomainException):
    """AI 분석 수행 중 발생한 예외"""
    pass
