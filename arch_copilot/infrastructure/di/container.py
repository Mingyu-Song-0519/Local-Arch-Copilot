"""
Dependency Injection Container
"""

from typing import Any, Callable, Dict, TypeVar

T = TypeVar("T")


class Container:
    """간단한 의존성 주입 컨테이너"""

    def __init__(self) -> None:
        self._singletons: Dict[type, Any] = {}
        self._factories: Dict[type, Callable[[], Any]] = {}

    def register_singleton(self, interface: type[T], instance: T) -> None:
        """싱글톤 인스턴스 등록"""
        self._singletons[interface] = instance

    def register_factory(self, interface: type[T], factory: Callable[[], T]) -> None:
        """팩토리 함수 등록 (Lazy Singleton)"""
        self._factories[interface] = factory

    def resolve(self, interface: type[T]) -> T:
        """의존성 해결"""
        # 1. 이미 생성된 싱글톤이 있으면 반환
        if interface in self._singletons:
            return self._singletons[interface]

        # 2. 팩토리가 있으면 생성 후 싱글톤으로 등록하고 반환
        if interface in self._factories:
            instance = self._factories[interface]()
            self._singletons[interface] = instance
            return instance

        raise ValueError(f"No binding found for {interface}")


# 전역 컨테이너 인스턴스
_container = Container()


def get_container() -> Container:
    """전역 컨테이너 반환"""
    return _container
