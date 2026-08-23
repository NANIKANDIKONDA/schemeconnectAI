import React from 'react';
import { UserCircle } from 'lucide-react';

const ProfilePanel = ({ profile }) => {
  if (!profile || Object.keys(profile).length === 0) {
    return (
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 text-center">
        <UserCircle className="w-12 h-12 text-gray-300 mx-auto mb-3" />
        <p className="text-sm text-gray-500">Your profile is empty. Describe your situation to get started.</p>
      </div>
    );
  }

  // Filter out internal fields starting with underscore
  const displayFields = Object.entries(profile).filter(([k, v]) => !k.startsWith('_') && v !== null && v !== undefined && v !== '');

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
      <div className="bg-gray-50 px-4 py-3 border-b border-gray-200 flex items-center space-x-2">
        <UserCircle className="w-5 h-5 text-gray-500" />
        <h2 className="text-sm font-semibold text-gray-700 uppercase tracking-wider">Citizen Profile</h2>
      </div>
      <div className="p-4">
        {displayFields.length === 0 ? (
          <p className="text-sm text-gray-500 italic">No details extracted yet.</p>
        ) : (
          <dl className="grid grid-cols-1 gap-x-4 gap-y-4 sm:grid-cols-2">
            {displayFields.map(([key, value]) => (
              <div key={key} className="sm:col-span-1">
                <dt className="text-xs font-medium text-gray-500 capitalize">{key.replace(/_/g, ' ')}</dt>
                <dd className="mt-1 text-sm text-gray-900 font-medium">
                  {Array.isArray(value) ? value.join(', ') : String(value)}
                </dd>
              </div>
            ))}
          </dl>
        )}
      </div>
    </div>
  );
};

export default ProfilePanel;
