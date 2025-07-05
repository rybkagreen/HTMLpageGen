from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.modules.ai_integration.service import AIService

router = APIRouter()


class ChatMessage(BaseModel):
    role: str  # 'user' | 'assistant' | 'system'
    content: str
    timestamp: Optional[str] = None


class ChatRequest(BaseModel):
    message: str
    conversation_history: Optional[List[ChatMessage]] = []


class ChatResponse(BaseModel):
    content: str
    reasoning: Optional[str] = None
    generated_code: Optional[Dict[str, Any]] = None


@router.post("/generate", response_model=ChatResponse)
async def generate_chat_response(
    request: ChatRequest,
    ai_service: AIService = Depends(),
):
    """
    Generate chat response using AI with context awareness
    """
    try:
        # Определяем намерение пользователя
        intention = await ai_service.analyze_intention(request.message)

        # Строим контекст из истории разговора
        context = _build_context(request.conversation_history)

        # Генерируем ответ в зависимости от намерения
        if intention.get("type") == "code_generation":
            # Пользователь хочет сгенерировать код
            result = await _generate_code_response(request.message, context, ai_service)
        elif intention.get("type") == "code_improvement":
            # Пользователь хочет улучшить существующий код
            result = await _improve_code_response(request.message, context, ai_service)
        else:
            # Обычный разговор или консультация
            result = await _generate_conversational_response(
                request.message, context, ai_service
            )

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def _generate_code_response(
    message: str, context: str, ai_service: AIService
) -> ChatResponse:
    """Генерация кода на основе запроса пользователя"""

    # Промпт для генерации кода
    system_prompt = f"""
    Вы - эксперт веб-разработчик и ментор. Ваша задача - создать качественный HTML код на основе описания пользователя.
    
    Контекст разговора: {context}
    
    Требования:
    1. Создайте современный, семантичный HTML код
    2. Используйте встроенные CSS стили для красивого дизайна
    3. Код должен быть адаптивным (responsive)
    4. Добавьте комментарии для объяснения ключевых частей
    5. Следуйте лучшим практикам веб-разработки
    
    Запрос пользователя: {message}
    
    Ответьте в формате JSON:
    {{
        "explanation": "Объяснение того, что вы создали",
        "reasoning": "Ваши рассуждения и подход",
        "html_code": "Сгенерированный HTML код",
        "features": ["список ключевых особенностей"],
        "suggestions": ["предложения по улучшению"]
    }}
    """

    # Получаем ответ от AI
    ai_response = await ai_service.chat_completion(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message},
        ]
    )

    try:
        import json

        parsed_response = json.loads(ai_response)

        # Формируем ответ для пользователя
        content = f"""✨ **Создан HTML код!**

{parsed_response.get('explanation', 'Код создан согласно вашему запросу.')}

**Ключевые особенности:**
{chr(10).join(['• ' + feature for feature in parsed_response.get('features', [])])}

**Рекомендации:**
{chr(10).join(['• ' + suggestion for suggestion in parsed_response.get('suggestions', [])])}
"""

        return ChatResponse(
            content=content,
            reasoning=parsed_response.get("reasoning"),
            generated_code={
                "html": parsed_response.get("html_code", ""),
                "meta": {
                    "features": parsed_response.get("features", []),
                    "suggestions": parsed_response.get("suggestions", []),
                    "generation_type": "chat_based",
                },
            },
        )

    except json.JSONDecodeError:
        # Если AI не ответил в JSON формате, возвращаем как есть
        return ChatResponse(
            content=ai_response,
            reasoning="Базовый ответ без структурированного форматирования",
        )


async def _improve_code_response(
    message: str, context: str, ai_service: AIService
) -> ChatResponse:
    """Улучшение существующего кода"""

    system_prompt = f"""
    Вы - эксперт по оптимизации и улучшению веб-кода. Помогите улучшить код пользователя.
    
    Контекст разговора: {context}
    
    Запрос пользователя: {message}
    
    Проанализируйте код и предложите конкретные улучшения в областях:
    - Производительность
    - Доступность (accessibility)
    - SEO оптимизация
    - Современные практики
    - Безопасность
    """

    ai_response = await ai_service.chat_completion(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message},
        ]
    )

    return ChatResponse(
        content=ai_response, reasoning="Анализ и рекомендации по улучшению кода"
    )


async def _generate_conversational_response(
    message: str, context: str, ai_service: AIService
) -> ChatResponse:
    """Обычный разговорный ответ"""

    system_prompt = f"""
    Вы - дружелюбный и опытный ментор по веб-разработке. Отвечайте полезно и поддерживающе.
    
    Контекст разговора: {context}
    
    Если пользователь задает вопросы о веб-разработке, дайте экспертный совет.
    Если пользователь хочет создать что-то, направьте его к конкретному описанию для генерации кода.
    """

    ai_response = await ai_service.chat_completion(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message},
        ]
    )

    return ChatResponse(content=ai_response, reasoning="Консультационный ответ")


def _build_context(conversation_history: List[ChatMessage]) -> str:
    """Строим контекст из истории разговора"""
    if not conversation_history:
        return "Начало разговора"

    context_parts = []
    for msg in conversation_history[-5:]:  # Последние 5 сообщений
        role = "Пользователь" if msg.role == "user" else "Ассистент"
        context_parts.append(f"{role}: {msg.content[:200]}...")

    return "\n".join(context_parts)


@router.get("/capabilities")
async def get_chat_capabilities():
    """Получить возможности чата"""
    return {
        "features": [
            "Генерация HTML кода по описанию",
            "Улучшение существующего кода",
            "Консультации по веб-разработке",
            "Анализ и рекомендации",
            "Контекстная память в разговоре",
        ],
        "supported_languages": ["Russian", "English"],
        "model": "DeepSeek Chat",
        "reasoning_available": True,
    }
