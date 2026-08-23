import React from 'react';
import { HelpCircle } from 'lucide-react';

const MissingInfoCard = ({ fields }) => {
  if (!fields || fields.length === 0) return null;

  return (
    <div className="bg-blue-50 rounded-lg border border-blue-100 p-4 mb-4">
      <div className="flex items-start space-x-3">
        <HelpCircle className="w-5 h-5 text-blue-500 flex-shrink-0 mt-0.5" />
        <div>
          <h4 className="text-sm font-semibold text-blue-800">Additional information needed</h4>
          <p className="text-sm text-blue-600 mt-1">
            Please provide:
          </p>
          <ul className="list-disc list-inside mt-2 text-sm text-blue-700 font-medium">
            {fields.map(field => (
              <li key={field} className="capitalize">{field.replace(/_/g, ' ')}</li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};

export default MissingInfoCard;
