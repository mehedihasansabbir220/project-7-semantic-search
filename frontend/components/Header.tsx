/**
 * Header Component
 *
 * Application header with logo and description
 */

interface HeaderProps {
  apiStatus?: boolean;
}

export function Header({ apiStatus }: HeaderProps) {
  return (
    <header className="border-b border-gray-200 bg-white">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 py-6 sm:py-8">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h1 className="text-3xl sm:text-4xl font-bold">
              <span className="text-gradient">Semantic Search</span>
            </h1>
            <p className="text-gray-600 mt-2">
              Find documents by meaning, not keywords. Powered by AI embeddings.
            </p>
          </div>

          {/* API Status indicator */}
          {apiStatus !== undefined && (
            <div className="flex items-center gap-2 px-3 py-2 rounded-full text-sm font-medium">
              <div className={`w-2 h-2 rounded-full ${apiStatus ? 'bg-green-500' : 'bg-red-500'}`} />
              <span className={apiStatus ? 'text-green-700' : 'text-red-700'}>
                {apiStatus ? 'Connected' : 'Offline'}
              </span>
            </div>
          )}
        </div>

        {/* Tech stack info */}
        <div className="flex flex-wrap gap-2 text-xs text-gray-500">
          <span className="px-2 py-1 bg-gray-100 rounded">Python Backend</span>
          <span className="px-2 py-1 bg-gray-100 rounded">FastAPI</span>
          <span className="px-2 py-1 bg-gray-100 rounded">Embeddings</span>
          <span className="px-2 py-1 bg-gray-100 rounded">Local</span>
        </div>
      </div>
    </header>
  );
}
