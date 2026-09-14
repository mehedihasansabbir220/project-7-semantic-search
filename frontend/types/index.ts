/**
 * Type definitions for semantic search API
 */

export interface SearchResult {
  chunk_id: string;
  document_id: string;
  score: number;
  text: string;
  filename: string;
}

export interface SearchResponse {
  query: string;
  top_k: number;
  total_results: number;
  results: SearchResult[];
}

export interface HealthResponse {
  status: 'healthy' | 'unhealthy';
  model_loaded: boolean;
  chunks_indexed: number;
}

export interface ApiError {
  error: string;
  detail?: string;
}
