import React from 'react';
import EligibilityBadge from './EligibilityBadge';
import { ExternalLink, CheckCircle2, XCircle, AlertCircle } from 'lucide-react';

const SchemeCard = ({ scheme }) => {
  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden mb-4 hover:shadow-md transition-shadow">
      <div className="p-5 border-b border-gray-100 bg-gray-50 flex justify-between items-start">
        <div>
          <div className="flex items-center space-x-2 mb-1">
            <span className="text-xs font-semibold text-blue-600 uppercase tracking-wider">{scheme.category}</span>
            <span className="text-gray-300">•</span>
            <span className="text-xs font-medium text-gray-500">Relevance: {scheme.relevance.replace(/_/g, ' ')}</span>
          </div>
          <h3 className="text-lg font-bold text-gray-900">{scheme.name}</h3>
        </div>
        <EligibilityBadge status={scheme.eligibility_status} />
      </div>

      <div className="p-5 space-y-4">
        {scheme.missing_information && scheme.missing_information.length > 0 && (
          <div className="flex items-start space-x-2 text-sm text-yellow-700 bg-yellow-50 p-3 rounded-md">
            <AlertCircle className="w-5 h-5 flex-shrink-0 text-yellow-500 mt-0.5" />
            <div>
              <span className="font-semibold block mb-1">Missing Information:</span>
              <ul className="list-disc list-inside">
                {scheme.missing_information.map((info, idx) => (
                  <li key={idx}>{info}</li>
                ))}
              </ul>
            </div>
          </div>
        )}

        {scheme.failed_conditions && scheme.failed_conditions.length > 0 && (
          <div className="flex items-start space-x-2 text-sm text-red-700 bg-red-50 p-3 rounded-md">
            <XCircle className="w-5 h-5 flex-shrink-0 text-red-500 mt-0.5" />
            <div>
              <span className="font-semibold block mb-1">Failed Conditions:</span>
              <ul className="list-disc list-inside">
                {scheme.failed_conditions.map((cond, idx) => (
                  <li key={idx}>{cond}</li>
                ))}
              </ul>
            </div>
          </div>
        )}

        {scheme.success_reasons && scheme.success_reasons.length > 0 && (
          <div className="flex items-start space-x-2 text-sm text-green-700 bg-green-50 p-3 rounded-md">
            <CheckCircle2 className="w-5 h-5 flex-shrink-0 text-green-500 mt-0.5" />
            <div>
              <span className="font-semibold block mb-1">Why you match:</span>
              <ul className="list-disc list-inside">
                {scheme.success_reasons.map((reason, idx) => (
                  <li key={idx}>{reason}</li>
                ))}
              </ul>
            </div>
          </div>
        )}

        {scheme.benefits && scheme.benefits.length > 0 && (
          <div>
            <h4 className="text-sm font-semibold text-gray-900 mb-2">Benefits</h4>
            <ul className="space-y-1">
              {scheme.benefits.map((benefit, idx) => (
                <li key={idx} className="flex items-start space-x-2 text-sm text-gray-600">
                  <CheckCircle2 className="w-4 h-4 text-green-500 mt-0.5 flex-shrink-0" />
                  <span>{benefit}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2 border-t border-gray-100">
          {scheme.documents_required && scheme.documents_required.length > 0 && (
            <div>
              <h4 className="text-sm font-semibold text-gray-900 mb-1">Required Documents</h4>
              <p className="text-sm text-gray-600">{scheme.documents_required.join(', ')}</p>
            </div>
          )}
          {scheme.how_to_apply && (
            <div>
              <h4 className="text-sm font-semibold text-gray-900 mb-1">How to Apply</h4>
              <p className="text-sm text-gray-600">{scheme.how_to_apply}</p>
            </div>
          )}
        </div>
      </div>

      {scheme.official_url && (
        <div className="px-5 py-3 bg-gray-50 border-t border-gray-100">
          <a
            href={scheme.official_url.startsWith('http') ? scheme.official_url : `https://${scheme.official_url}`}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center space-x-1 text-sm font-medium text-blue-600 hover:text-blue-800"
          >
            <span>Official Source</span>
            <ExternalLink className="w-4 h-4" />
          </a>
        </div>
      )}
    </div>
  );
};

export default SchemeCard;
