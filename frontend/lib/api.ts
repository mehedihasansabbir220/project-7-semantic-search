/**
 * API utilities for communicating with the semantic search backend.
 *
 * WHY SEPARATE API LOGIC?
 * - Centralized API configuration
 * - Easy to change backend URL
 * - Consistent error handling
 * - Reusable across components
 * - Easy to mock for testing
 */

import type { SearchResponse, HealthResponse, ApiError } from '@/types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

/**
 * Search for semantic matches.
 *
 * @param query - Search query text
 * @param topK - Number of results to return (default: 5)
 * @returns Search results with similarity scores
 * @throws Error if request fails
 */
export async function search(query: string, topK: number = 5): Promise<SearchResponse> {
  try {
    const response = await fetch(`${API_URL}/search`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query,
        top_k: topK,
      }),
    });

    if (!response.ok) {
      const error: ApiError = await response.json();
      throw new Error(error.detail || error.error || 'Search failed');
    }

    const data: SearchResponse = await response.json();
    return data;
  } catch (error) {
    if (error instanceof Error) {
      throw error;
    }
    throw new Error('Failed to search');
  }
}

/**
 * Check if the API is healthy and ready.
 *
 * @returns Health status
 * @throws Error if request fails
 */
export async function checkHealth(): Promise<HealthResponse> {
  try {
    const response = await fetch(`${API_URL}/health`);

    if (!response.ok) {
      throw new Error('API health check failed');
    }

    const data: HealthResponse = await response.json();
    return data;
  } catch (error) {
    if (error instanceof Error) {
      throw error;
    }
    throw new Error('Failed to check API health');
  }
}

/**
 * Get API statistics.
 *
 * @returns Service statistics
 * @throws Error if request fails
 */
export async function getStats(): Promise<any> {
  try {
    const response = await fetch(`${API_URL}/search/stats`);

    if (!response.ok) {
      throw new Error('Failed to get stats');
    }

    return response.json();
  } catch (error) {
    if (error instanceof Error) {
      throw error;
    }
    throw new Error('Failed to get stats');
  }
}
