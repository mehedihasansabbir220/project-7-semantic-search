/**
 * LoadingState Component
 *
 * Shows skeleton loaders while search results are being fetched.
 * Provides better UX than plain loading message.
 */

export function LoadingState() {
  return (
    <div className="space-y-4">
      {/* Show 3 skeleton cards */}
      {[0, 1, 2].map((i) => (
        <div
          key={i}
          className="p-6 border border-gray-200 rounded-lg bg-white"
        >
          {/* Skeleton header */}
          <div className="flex items-start justify-between mb-3">
            <div className="flex items-center gap-3 flex-1">
              <div className="w-8 h-8 rounded-full bg-gray-200 animate-pulse" />
              <div className="h-6 bg-gray-200 rounded w-1/3 animate-pulse" />
            </div>
            <div className="h-6 bg-gray-200 rounded w-20 animate-pulse" />
          </div>

          {/* Skeleton label */}
          <div className="h-4 bg-gray-200 rounded w-24 mb-3 animate-pulse" />

          {/* Skeleton text */}
          <div className="space-y-2 mb-4">
            <div className="h-4 bg-gray-200 rounded w-full animate-pulse" />
            <div className="h-4 bg-gray-200 rounded w-5/6 animate-pulse" />
            <div className="h-4 bg-gray-200 rounded w-4/5 animate-pulse" />
          </div>

          {/* Skeleton footer */}
          <div className="flex items-center justify-between pt-4 border-t border-gray-100">
            <div className="h-4 bg-gray-200 rounded w-1/4 animate-pulse" />
            <div className="h-6 bg-gray-200 rounded w-20 animate-pulse" />
          </div>
        </div>
      ))}
    </div>
  );
}
