import React from 'react';

function StatisticsHeader({ viewType, setViewType }) {
  return (
    <header className="pt-6 pb-2 px-6">
      <h1 className="text-xl font-bold text-center text-gray-900 tracking-tight">
        InnerNote
      </h1>

      <div className="flex gap-2 mt-4 border-b border-orange-100/50">
        <button
          onClick={() => setViewType('daily')}
          className={`pb-2 px-3 text-sm transition-all ${
            viewType === 'daily'
              ? 'font-bold border-b-2 border-red-400 text-red-500'
              : 'font-medium text-gray-400 hover:text-gray-600'
          }`}
        >
          일별
        </button>

        <button
          onClick={() => setViewType('weekly')}
          className={`pb-2 px-3 text-sm transition-all ${
            viewType === 'weekly'
              ? 'font-bold border-b-2 border-red-400 text-red-500'
              : 'font-medium text-gray-400 hover:text-gray-600'
          }`}
        >
          주별
        </button>

        <button
          onClick={() => setViewType('monthly')}
          className={`pb-2 px-3 text-sm transition-all ${
            viewType === 'monthly'
              ? 'font-bold border-b-2 border-red-400 text-red-500'
              : 'font-medium text-gray-400 hover:text-gray-600'
          }`}
        >
          월별
        </button>
      </div>
    </header>
  );
}

export default StatisticsHeader;