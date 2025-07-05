export interface SEOAnalysisRequest {
  html: string;
}

export interface SEOAnalysisResponse {
  score: number;
  title: {
    exists: boolean;
    length: number;
    text: string;
    issues: string[];
  };
  meta_description: {
    exists: boolean;
    length: number;
    text: string;
    issues: string[];
  };
  headings: {
    structure: Record<string, string[]>;
    h1_count: number;
    total_headings: number;
    issues: string[];
  };
  images: {
    total: number;
    missing_alt: number;
    empty_alt: number;
    issues: string[];
  };
  links: {
    total: number;
    internal: number;
    external: number;
    issues: string[];
  };
  content: {
    word_count: number;
    character_count: number;
    issues: string[];
  };
  issues: string[];
  recommendations: string[];
}

export interface StructuredDataRequest {
  content_type: 'article' | 'webpage';
  data: Record<string, unknown>;
}

export interface StructuredDataResponse {
  json_ld: string;
}

export interface SEOBestPractices {
  title: {
    min_length: number;
    max_length: number;
    recommendations: string[];
  };
  meta_description: {
    min_length: number;
    max_length: number;
    recommendations: string[];
  };
  meta_keywords: {
    status: string;
    note: string;
  };
}
