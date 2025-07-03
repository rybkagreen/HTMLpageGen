import { 
  AIEnhancementRequest, 
  AIEnhancementResponse, 
  MetaTagsRequest, 
  MetaTagsResponse,
  ImprovementSuggestion,
  AICapabilities 
} from './types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export class AIService {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  async enhanceContent(request: AIEnhancementRequest): Promise<AIEnhancementResponse> {
    const response = await fetch(`${this.baseUrl}/api/v1/ai/enhance-content`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        content: request.content,
        enhancement_type: request.enhancementType
      })
    });

    if (!response.ok) {
      throw new Error(`AI enhancement failed: ${response.statusText}`);
    }

    const data = await response.json();
    return {
      enhancedContent: data.enhanced_content,
      originalContent: data.original_content,
      enhancementType: data.enhancement_type
    };
  }

  async generateMetaTags(request: MetaTagsRequest): Promise<MetaTagsResponse> {
    const response = await fetch(`${this.baseUrl}/api/v1/ai/generate-meta-tags`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request)
    });

    if (!response.ok) {
      throw new Error(`Meta tags generation failed: ${response.statusText}`);
    }

    return await response.json();
  }

  async suggestImprovements(html: string): Promise<ImprovementSuggestion> {
    const response = await fetch(`${this.baseUrl}/api/v1/ai/suggest-improvements`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ html })
    });

    if (!response.ok) {
      throw new Error(`Improvement suggestions failed: ${response.statusText}`);
    }

    return await response.json();
  }

  async getCapabilities(): Promise<AICapabilities> {
    const response = await fetch(`${this.baseUrl}/api/v1/ai/capabilities`);

    if (!response.ok) {
      throw new Error(`Failed to get AI capabilities: ${response.statusText}`);
    }

    return await response.json();
  }
}

export const aiService = new AIService();
