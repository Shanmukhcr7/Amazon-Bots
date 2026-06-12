'use client';

import { useEffect, useState } from 'react';
import DealCard from '@/components/DealCard';
import { fetchDeals } from '@/lib/api';

export default function Home() {
  const [deals, setDeals] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('PENDING');

  const loadDeals = async () => {
    setLoading(true);
    try {
      const data = await fetchDeals(filter === 'ALL' ? undefined : filter);
      setDeals(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDeals();
  }, [filter]);

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row justify-between items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold mb-2">Deal Discovery Engine</h1>
          <p className="text-slate-400">Review AI-analyzed product deals before publishing.</p>
        </div>
        <div className="flex gap-2 p-1 bg-slate-800 rounded-lg border border-slate-700">
          {['ALL', 'PENDING', 'APPROVED', 'REJECTED'].map((f) => (
            <button
              key={f}
              onClick={() => setFilter(f)}
              className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                filter === f 
                  ? 'bg-blue-600 text-white shadow-lg' 
                  : 'text-slate-400 hover:text-white hover:bg-slate-700'
              }`}
            >
              {f}
            </button>
          ))}
        </div>
      </div>

      {loading ? (
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
        </div>
      ) : deals.length === 0 ? (
        <div className="text-center py-20 bg-slate-800/30 rounded-2xl border border-slate-800 border-dashed">
          <p className="text-slate-400">No {filter !== 'ALL' ? filter.toLowerCase() : ''} deals found.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
          {deals.map((deal: any) => (
            <DealCard key={deal.id} deal={deal} onUpdate={loadDeals} />
          ))}
        </div>
      )}
    </div>
  );
}
