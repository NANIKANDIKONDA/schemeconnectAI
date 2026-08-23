import React from 'react';
import clsx from 'clsx';

const EligibilityBadge = ({ status }) => {
  const getBadgeStyles = () => {
    switch (status?.toUpperCase()) {
      case 'LIKELY_ELIGIBLE':
      case 'ELIGIBLE':
        return 'bg-green-100 text-green-800 border-green-200';
      case 'POSSIBLY_ELIGIBLE':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'MORE_INFORMATION_REQUIRED':
        return 'bg-blue-100 text-blue-800 border-blue-200';
      case 'NOT_ELIGIBLE':
        return 'bg-red-100 text-red-800 border-red-200';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getLabel = () => {
    return status?.replace(/_/g, ' ') || 'UNKNOWN';
  };

  return (
    <span className={clsx("inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border", getBadgeStyles())}>
      {getLabel()}
    </span>
  );
};

export default EligibilityBadge;
