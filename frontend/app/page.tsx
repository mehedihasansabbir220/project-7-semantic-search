'use client';

/**
 * Home Page Component
 *
 * Main semantic search interface combining:
 * - Search form
 * - Results display
 * - Loading states
 * - Error handling
 * - Empty states
 *
 * STATE MANAGEMENT:
 * - query: Current search query
 * - results: Search results from API
 * - isLoading: Loading state during search
 * - error: Error message if search fails
 * - apiAvailable: Whether backend is reachable
 */

import { useState, useEffect } from 'react';
import { Header } from '@/components/Header';
import { SearchForm } from '@/components/SearchForm';
import { SearchResult } from '@/components/SearchResult';
import { LoadingState } from '@/components/LoadingState';
import { EmptyState } from '@/components/EmptyState';
import { search, checkHealth } from '@/lib/api';
import type { SearchResponse } from '@/types';

export default function Home() {
  // State management
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SearchResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | undefined>();
  const [apiAvailable, setApiAvailable] = useState<boolean | undefined>();

  // Check API health on mount
  useEffect(() => {
    const checkAPI = async () => {
      try {
        await checkHealth();
        setApiAvailable(true);
      } catch {
        setApiAvailable(false);
      }
    };

    checkAPI();
  }, []);

  /**
   * Handle search form submission
   *
   * PROCESS:
   * 1. Clear previous errors
   * 2. Set loading state
   * 3. Call search API
   * 4. Update results or error
   * 5. Clear loading state
   */
  const handleSearch = async (searchQuery: string) => {
    setError(undefined);
    setQuery(searchQuery);
    setIsLoading(true);

    try {
      const data = await search(searchQuery, 5);
      setResults(data);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Search failed';
      setError(errorMessage);
      setResults(null);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <Header apiStatus={apiAvailable} />

      {/* Main content */}
      <main className="max-w-4xl mx-auto px-4 sm:px-6 py-8 sm:py-12">
        {/* Search form section */}
        <div className="bg-white rounded-lg shadow-sm p-6 sm:p-8 mb-8">
          <SearchForm
            onSearch={handleSearch}
            isLoading={isLoading}
            error={error}
          />
        </div>

        {/* Results section */}
        <div>
          {/* API Unavailable */}
          {apiAvailable === false && (
            <div className="bg-white rounded-lg shadow-sm p-8">
              <EmptyState apiUnavailable={true} />
            </div>
          )}

          {/* Loading state */}
          {isLoading && (
            <div className="bg-white rounded-lg shadow-sm p-6 sm:p-8">
              <LoadingState />
            </div>
          )}

          {/* Results found */}
          {!isLoading && results && results.total_results > 0 && (
            <div className="space-y-4">
              {/* Results header */}
              <div className="flex items-center justify-between">
                <h2 className="text-lg font-semibold text-gray-900">
                  Found {results.total_results} result{results.total_results !== 1 ? 's' : ''}
                </h2>
                <p className="text-sm text-gray-500">
                  Ranked by relevance
                </p>
              </div>

              {/* Results list */}
              <div className="space-y-4">
                {results.results.map((result, index) => (
                  <SearchResult
                    key={result.chunk_id}
                    result={result}
                    index={index}
                  />
                ))}
              </div>
            </div>
          )}

          {/* No results or empty state */}
          {!isLoading && (!results || results.total_results === 0) && (
            <div className="bg-white rounded-lg shadow-sm p-8">
              <EmptyState query={query} />
            </div>
          )}
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-gray-200 bg-white mt-12 sm:mt-16">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 py-6 sm:py-8">
          <p className="text-center text-sm text-gray-600">
            Built with Next.js, FastAPI, and AI embeddings
          </p>
          <p className="text-center text-xs text-gray-500 mt-2">
            Backend: {process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}
          </p>
        </div>
      </footer>
    </div>
  );
}
