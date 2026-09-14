/**
 * SearchForm Component
 *
 * Handles user input for semantic search queries.
 * Features:
 * - Text input field
 * - Submit button with loading state
 * - Example queries for guidance
 * - Error boundary
 */

'use client';

import { FormEvent, useState } from 'react';

interface SearchFormProps {
  onSearch: (query: string) => Promise<void>;
  isLoading: boolean;
  error?: string;
}

const EXAMPLE_QUERIES = [
  'machine learning algorithms',
  'deep neural networks',
  'natural language processing',
  'transformer models',
  'embeddings and vectors',
];

export function SearchForm({ onSearch, isLoading, error }: SearchFormProps) {
  const [query, setQuery] = useState('');

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (query.trim()) {
      await onSearch(query);
    }
  };

  const handleExampleClick = (example: string) => {
    setQuery(example);
  };

  return (
    <div className="w-full">
      {/* Main search form */}
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="space-y-2">
          <div className="relative">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search by meaning, not keywords..."
              disabled={isLoading}
              className="w-full px-4 py-3 text-lg border-2 border-gray-200 rounded-lg focus:border-primary-500 focus:outline-none disabled:bg-gray-50 disabled:cursor-not-allowed transition-smooth"
              autoFocus
            />
            {query && (
              <button
                type="button"
                onClick={() => setQuery('')}
                className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
              >
                ✕
              </button>
            )}
          </div>

          {/* Error message */}
          {error && (
            <div className="px-3 py-2 rounded bg-red-50 border border-red-200">
              <p className="text-sm text-red-700">{error}</p>
            </div>
          )}
        </div>

        {/* Search button */}
        <button
          type="submit"
          disabled={isLoading || !query.trim()}
          className="w-full px-6 py-3 rounded-lg font-semibold text-white bg-gradient-to-r from-primary-500 to-primary-700 hover:from-primary-600 hover:to-primary-800 disabled:opacity-50 disabled:cursor-not-allowed transition-smooth flex items-center justify-center gap-2"
        >
          {isLoading ? (
            <>
              <div className="animate-spin w-5 h-5 border-2 border-white border-t-transparent rounded-full" />
              Searching...
            </>
          ) : (
            <>
              🔍 Search
            </>
          )}
        </button>
      </form>

      {/* Example queries */}
      <div className="mt-6 pt-6 border-t border-gray-200">
        <p className="text-sm text-gray-600 font-medium mb-3">Try these examples:</p>
        <div className="flex flex-wrap gap-2">
          {EXAMPLE_QUERIES.map((example) => (
            <button
              key={example}
              onClick={() => handleExampleClick(example)}
              type="button"
              className="px-3 py-1.5 rounded-full text-sm bg-gray-100 text-gray-700 hover:bg-primary-50 hover:text-primary-700 transition-smooth border border-gray-200 hover:border-primary-200"
            >
              {example}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
