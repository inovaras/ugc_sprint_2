import pytest
from httpx import AsyncClient


class TestRatingsAPI:
    endpoint_template = "api/v1/ratings/movie/{movie_id}/"

    @pytest.mark.asyncio
    async def test_get_ratings(self, make_get_request, mongo_client, load_test_data):
        """
        Проверяет получение списка оценок по ID фильма.
        """
        movie_id = "4a82f1d4-8e94-4e4e-8d0c-845f4a25b733"  # UUID фильма из фикстуры
        endpoint = self.endpoint_template.format(movie_id=movie_id)

        response = await make_get_request(endpoint)
        
        # Проверка статуса ответа
        assert response.status_code == 200, f"Статус ответа должен быть 200, пришёл {response.status_code}"

        # Проверка содержимого ответа
        response_json = response.json()
        assert isinstance(response_json, list), "Ответ должен быть списком"
        assert len(response_json) > 0, "Список оценок не должен быть пустым"

        # Проверка структуры данных
        rating = response_json[0]
        assert "user_id" in rating, "Оценка должна содержать 'user_id'"
        assert "movie_id" in rating, "Оценка должна содержать 'movie_id'"
        assert "rating" in rating, "Оценка должна содержать 'rating'"
        assert "timestamp" in rating, "Оценка должна содержать 'timestamp'"

        # Проверка соответствия ID фильма в ответе
        assert all(r["movie_id"] == movie_id for r in response_json), "Все оценки должны принадлежать фильму"

    @pytest.mark.asyncio
    async def test_get_ratings_with_pagination(self, make_get_request, mongo_client, load_test_data):
        """
        Проверяет работу пагинации при получении списка оценок
        """

        movie_id = "4a82f1d4-8e94-4e4e-8d0c-845f4a25b733"
        params = {"limit": 1, "offset": 2}
        response = await make_get_request(self.endpoint_template.format(movie_id=movie_id), params=params)
        
        assert response.status_code == 200, "Статус ответа должен быть 200"
        response_json = response.json()

        assert isinstance(response_json, list), "Ответ должен быть списком"
        assert len(response_json) <= 2, "Количество элементов не должно превышать размер страницы"