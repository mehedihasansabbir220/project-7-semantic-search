/**
 * SearchResult Component
 *
 * Displays a single search result with:
 * - Document filename
 * - Similarity score (0.0 to 1.0)
 * - Text snippet preview
 * - Relevance badge
 */

import type { SearchResult as SearchResultType } from '@/types';

interface SearchResultProps {
  result: SearchResultType;
  index: number;
}

export function SearchResult({ result, index }: SearchResultProps) {
  // Convert score (0.0-1.0) to percentage
  const scorePercentage = Math.round(result.score * 100);

  // Determine color based on score
  const getScoreColor = (score: number) => {
    if (score >= 0.85) return 'bg-green-100 text-green-800 border-green-200';
    if (score >= 0.70) return 'bg-blue-100 text-blue-800 border-blue-200';
    return 'bg-gray-100 text-gray-800 border-gray-200';
  };

  const getScoreLabel = (score: number) => {
    if (score >= 0.85) return 'Very Relevant';
    if (score >= 0.70) return 'Relevant';
    return 'Somewhat Relevant';
  };

  return (
    <div
      className="animate-fade-in p-6 border border-gray-200 rounded-lg hover:border-primary-500 hover:shadow-lg transition-smooth bg-white"
      style={{ animationDelay: `${index * 50}ms` }}
    >
      {/* Header with rank and score */}
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center gap-3">
          <span className="flex items-center justify-center w-8 h-8 rounded-full bg-primary-100 text-primary-700 font-semibold text-sm">
            {index + 1}
          </span>
          <h3 className="text-lg font-semibold text-gray-900">
            {result.filename}
          </h3>
        </div>

        {/* Score badge */}
        <div className={`px-3 py-1 rounded-full text-sm font-medium border ${getScoreColor(result.score)}`}>
          {scorePercentage}%
        </div>
      </div>

      {/* Relevance label */}
      <div className="mb-3">
        <span className="text-xs font-medium text-gray-500 uppercase tracking-wide">
          {getScoreLabel(result.score)}
        </span>
      </div>

      {/* Text snippet */}
      <p className="text-gray-700 leading-relaxed mb-4 text-sm">
        {result.text}
      </p>

      {/* Metadata */}
      <div className="flex items-center justify-between pt-4 border-t border-gray-100">
        <div className="text-xs text-gray-500">
          <span className="font-medium">ID:</span> {result.chunk_id}
        </div>
        <div className="text-xs px-2 py-1 rounded bg-gray-50 text-gray-600">
          {result.document_id}
        </div>
      </div>
    </div>
  );
}
