"""
Domain Layer - 비즈니스 로직의 핵심

Clean Architecture의 가장 안쪽 계층으로, 외부 의존성이 없어야 합니다.
- entities: 도메인 엔티티 (ProjectStructure, FileNode 등)
- repositories: 리포지토리 인터페이스 (추상 클래스)
- services: 도메인 서비스 (비즈니스 규칙)
- config: 설정 인터페이스
"""
