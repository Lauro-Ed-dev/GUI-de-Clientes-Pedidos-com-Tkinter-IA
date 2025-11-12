# Simples Event Bus (pub/sub) para desacoplar telas e lógica de atualização

from collections import defaultdict

class EventBus:
    _subscribers = defaultdict(list)

    @classmethod
    def subscribe(cls, event_name: str, callback):
        """Registra uma função callback para um evento."""
        cls._subscribers[event_name].append(callback)

    @classmethod
    def publish(cls, event_name: str, **data):
        """Notifica todos os inscritos do evento."""
        for cb in cls._subscribers.get(event_name, []):
            try:
                cb(data)
            except Exception as e:
                print(f"[EventBus] Erro em callback de '{event_name}': {e}")