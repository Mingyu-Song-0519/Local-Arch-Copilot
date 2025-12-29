"""
DI Container 테스트

의존성 등록, 해결, 싱글톤 동작을 테스트합니다.
"""

from abc import ABC, abstractmethod

import pytest

from arch_copilot.infrastructure.di.container import Container, get_container


class IService(ABC):
    @abstractmethod
    def do_something(self) -> str:
        pass


class ServiceImpl(IService):
    def do_something(self) -> str:
        return "done"


class TestContainer:
    """Dependency Injection Container 테스트"""

    def test_should_register_and_resolve_singleton(self) -> None:
        """싱글톤 등록 및 해결"""
        container = Container()
        instance = ServiceImpl()

        container.register_singleton(IService, instance)
        resolved = container.resolve(IService)

        assert resolved is instance
        assert resolved.do_something() == "done"

    def test_should_register_and_resolve_factory(self) -> None:
        """팩토리 등록 및 해결 (싱글톤으로 관리됨)"""
        container = Container()

        container.register_factory(IService, lambda: ServiceImpl())

        resolvedfv1 = container.resolve(IService)
        resolved2 = container.resolve(IService)

        assert isinstance(resolvedfv1, ServiceImpl)
        assert resolvedfv1 is resolved2  # 컨테이너는 기본적으로 싱글톤으로 관리

    def test_should_raise_error_for_unregistered(self) -> None:
        """등록되지 않은 인터페이스 요청 시 에러"""
        container = Container()

        with pytest.raises(ValueError, match="No binding found"):
            container.resolve(IService)

    def test_should_get_global_container(self) -> None:
        """전역 컨테이너 인스턴스 접근"""
        container1 = get_container()
        container2 = get_container()

        assert container1 is container2
