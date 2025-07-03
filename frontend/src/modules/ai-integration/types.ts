export interface AIEnhancementRequest {
  content: string;
  enhancementType: 'general' | 'seo' | 'accessibility' | 'marketing';
}

export interface AIEnhancementResponse {
  enhancedContent: string;
  originalContent: string;
  enhancementType: string;
}

export interface MetaTagsRequest {
  content: string;
}

export interface MetaTagsResponse {
  title: string;
  description: string;
  keywords: string;
}

export interface ImprovementSuggestion {
  suggestions: string[];
}

export interface AICapabilities {
  enhancementTypes: Array<{
    id: string;
    name: string;
    description: string;
  }>;
  features: string[];
}
