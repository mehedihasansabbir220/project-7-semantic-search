/**
 * EmptyState Component
 *
 * Shows when:
 * - No search has been performed yet
 * - Search returned no results
 * - API is not available
 */

interface EmptyStateProps {
  query?: string;
  apiUnavailable?: boolean;
}

export function EmptyState({ query, apiUnavailable }: EmptyStateProps) {
  if (apiUnavailable) {
    return (
      <div className="text-center py-12">
        <div className="text-4xl mb-3">⚠️</div>
        <h3 className="text-xl font-semibold text-gray-900 mb-2">API Unavailable</h3>
        <p className="text-gray-600 mb-4">
          Unable to connect to the search API. Please make sure the backend is running:
        </p>
        <pre className="bg-gray-100 p-4 rounded text-left inline-block text-sm text-gray-700 mb-4">
          cd backend{'\n'}
          uvicorn main:app --reload
        </pre>
      </div>
    );
  }

  if (query) {
    return (
      <div className="text-center py-12">
        <div className="text-4xl mb-3">🔍</div>
        <h3 className="text-xl font-semibold text-gray-900 mb-2">No Results Found</h3>
        <p className="text-gray-600">
          No documents matched your query: <span className="font-medium">"{query}"</span>
        </p>
        <p className="text-gray-500 text-sm mt-2">
          Try a different query or search for a related topic
        </p>
      </div>
    );
  }

  return (
    <div className="text-center py-12">
      <div className="text-5xl mb-4">✨</div>
      <h2 className="text-2xl font-bold text-gray-900 mb-2">Semantic Search</h2>
      <p className="text-gray-600 mb-6 max-w-md">
        Find documents by <span className="font-semibold">meaning</span>, not just keywords.
      </p>

      {/* Features list */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-8 max-w-2xl mx-auto">
        <div className="p-4 rounded-lg bg-blue-50 border border-blue-100">
          <div className="text-2xl mb-2">🧠</div>
          <p className="text-sm text-gray-700">
            <span className="font-semibold">AI-Powered</span> Understands meaning
          </p>
        </div>
        <div className="p-4 rounded-lg bg-green-50 border border-green-100">
          <div className="text-2xl mb-2">⚡</div>
          <p className="text-sm text-gray-700">
            <span className="font-semibold">Instant</span> Results in milliseconds
          </p>
        </div>
        <div className="p-4 rounded-lg bg-purple-50 border border-purple-100">
          <div className="text-2xl mb-2">📚</div>
          <p className="text-sm text-gray-700">
            <span className="font-semibold">Local</span> Runs completely on your machine
          </p>
        </div>
      </div>

      {/* Instructions */}
      <div className="mt-8 p-4 rounded-lg bg-gray-50 border border-gray-200">
        <p className="text-sm text-gray-600">
          👆 Start by entering your search query above to get started
        </p>
      </div>
    </div>
  );
}
