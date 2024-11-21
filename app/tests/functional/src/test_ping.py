import pytest
from httpx import AsyncClient


class TestPingAPI:
    endpoint_template = "api/v1/ping"

    @pytest.mark.asyncio
    async def test_get_ratings(self, make_get_request):
        """
        Проверяет получение
        """
        endpoint = f"{self.endpoint_template}/"

        response = await make_get_request(endpoint)
        
        # Проверка статуса ответа
        assert response.status_code == 200, f"Статус ответа должен быть 200, пришёл {response.status_code}"
        assert response.json() == {"status": "ok", "message": "Server is up and running."}

    @pytest.mark.asyncio
    async def test_health_check_success(self, make_get_request):
        """Тестирует эндпоинт для проверки состояния MongoDB"""
        endpoint = f"{self.endpoint_template}/mongo"
        response = await make_get_request(endpoint)

        assert response.status_code == 200, f"Статус ответа должен быть 200, пришёл {response.status_code}"
        assert response.json() == {"status": "ok", "message": "All systems operational"}