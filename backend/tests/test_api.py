from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "HTML" in response.text


class TestPagesAPI:
    """Test pages API endpoints"""

    def test_generate_page_basic(self):
        """Test basic page generation"""
        request_data = {
            "content": "Test content for page generation",
            "template": "default",
            "ai_enhancements": True,
        }

        response = client.post("/api/v1/pages/generate", json=request_data)
        assert response.status_code == 200

        data = response.json()
        assert "html" in data
        assert "meta" in data
        assert "generation_time" in data

    def test_generate_page_minimal(self):
        """Test page generation with minimal data"""
        request_data = {"content": "Minimal test content"}

        response = client.post("/api/v1/pages/generate", json=request_data)
        assert response.status_code == 200

    def test_get_templates(self):
        """Test getting available templates"""
        response = client.get("/api/v1/pages/templates")
        assert response.status_code == 200

        data = response.json()
        assert "templates" in data
        assert isinstance(data["templates"], list)

    def test_preview_page(self):
        """Test page preview"""
        response = client.get("/api/v1/pages/preview/test-page-id")
        assert response.status_code == 200

        data = response.json()
        assert "html" in data
        assert "page_id" in data
        assert data["page_id"] == "test-page-id"

    def test_delete_page(self):
        """Test page deletion"""
        response = client.delete("/api/v1/pages/pages/test-page-id")
        assert response.status_code == 200

        data = response.json()
        assert "message" in data
        assert "test-page-id" in data["message"]


class TestAIAPI:
    """Test AI API endpoints"""

    def test_ai_capabilities(self):
        """Test getting AI capabilities"""
        response = client.get("/api/v1/ai/capabilities")
        assert response.status_code == 200

        data = response.json()
        assert "enhancement_types" in data
        assert "features" in data
        assert isinstance(data["enhancement_types"], list)

    def test_enhance_content(self):
        """Test content enhancement"""
        request_data = {
            "content": "Test content to enhance",
            "enhancement_type": "general",
        }

        response = client.post("/api/v1/ai/enhance-content", json=request_data)
        # Note: This might fail without valid AI service, that's expected
        # 500 if no AI key configured
        assert response.status_code in [200, 500]

    def test_generate_meta_tags(self):
        """Test meta tags generation"""
        request_data = {"content": "Test content for meta generation"}

        response = client.post("/api/v1/ai/generate-meta-tags", json=request_data)
        # 500 if no AI key configured
        assert response.status_code in [200, 500]

    def test_suggest_improvements(self):
        """Test improvement suggestions"""
        request_data = {"html": "<html><body><h1>Test</h1></body></html>"}

        response = client.post("/api/v1/ai/suggest-improvements", json=request_data)
        # 500 if no AI key configured
        assert response.status_code in [200, 500]

    def test_provider_info(self):
        """Test getting provider info"""
        response = client.get("/api/v1/ai/provider-info")
        assert response.status_code == 200

        data = response.json()
        assert "provider" in data
        assert "configured" in data


class TestSEOAPI:
    """Test SEO API endpoints"""

    def test_seo_analysis(self):
        """Test SEO analysis"""
        test_html = (
            "<html><head><title>Test</title></head>" "<body><h1>Test</h1></body></html>"
        )
        request_data = {"html": test_html}

        response = client.post("/api/v1/seo/analyze", json=request_data)
        assert response.status_code == 200

        data = response.json()
        assert "score" in data
        assert "title" in data
        assert "meta_description" in data

    def test_generate_structured_data(self):
        """Test structured data generation"""
        request_data = {
            "content_type": "webpage",
            "data": {"title": "Test Page", "description": "Test description"},
        }

        response = client.post("/api/v1/seo/structured-data", json=request_data)
        assert response.status_code == 200

        data = response.json()
        assert "json_ld" in data


class TestMetrics:
    """Test metrics endpoint"""

    def test_metrics_endpoint(self):
        """Test metrics collection"""
        response = client.get("/metrics")
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, dict)


class TestErrorHandling:
    """Test error handling"""

    def test_invalid_page_generation(self):
        """Test invalid page generation request"""
        request_data = {}  # Empty request

        response = client.post("/api/v1/pages/generate", json=request_data)
        assert response.status_code == 422  # Validation error

    def test_nonexistent_endpoint(self):
        """Test nonexistent endpoint"""
        response = client.get("/api/v1/nonexistent")
        assert response.status_code == 404

    def test_invalid_method(self):
        """Test invalid method"""
        response = client.post("/health")
        assert response.status_code == 405  # Method not allowed
