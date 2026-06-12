'use client';
import { useState } from 'react';
import { updateDealStatus } from '@/lib/api';

export default function DealCard({ deal, onUpdate }: { deal: any, onUpdate: () => void }) {
  const [loading, setLoading] = useState(false);

  const handleStatusChange = async (status: string) => {
    setLoading(true);
    try {
      await updateDealStatus(deal.id, status);
      onUpdate();
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status: string) => {
    switch(status) {
      case 'APPROVED': return 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30';
      case 'REJECTED': return 'bg-red-500/20 text-red-400 border-red-500/30';
      case 'PUBLISHED': return 'bg-blue-500/20 text-blue-400 border-blue-500/30';
      default: return 'bg-amber-500/20 text-amber-400 border-amber-500/30';
    }
  };

  return (
    <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-xl p-6 hover:shadow-lg hover:shadow-blue-500/10 transition-all duration-300">
      <div className="flex justify-between items-start mb-4">
        <div>
          <h3 className="text-xl font-semibold mb-1">{deal.product?.name || 'Unknown Product'}</h3>
          <span className={`px-3 py-1 rounded-full text-xs border ${getStatusColor(deal.status)}`}>
            {deal.status}
          </span>
        </div>
        <div className="bg-blue-500/10 border border-blue-500/20 rounded-lg p-2 text-center min-w-[80px]">
          <div className="text-xs text-blue-400 uppercase tracking-wider">Score</div>
          <div className="text-2xl font-bold text-white">{deal.deal_score.toFixed(0)}</div>
        </div>
      </div>
      
      {deal.ai_summary && (
        <div className="mb-4 bg-slate-900/50 p-4 rounded-lg border border-slate-700/50">
          <h4 className="text-sm text-slate-400 mb-2 font-medium">AI Analysis</h4>
          <p className="text-sm text-slate-300 leading-relaxed">{deal.ai_summary}</p>
        </div>
      )}

      <div className="grid grid-cols-2 gap-4 mb-6">
        {deal.pros && deal.pros.length > 0 && (
          <div>
            <h4 className="text-xs text-emerald-400 uppercase tracking-wider mb-2">Pros</h4>
            <ul className="text-sm text-slate-300 space-y-1">
              {deal.pros.map((pro: string, i: number) => <li key={i}>✓ {pro}</li>)}
            </ul>
          </div>
        )}
        {deal.cons && deal.cons.length > 0 && (
          <div>
            <h4 className="text-xs text-red-400 uppercase tracking-wider mb-2">Cons</h4>
            <ul className="text-sm text-slate-300 space-y-1">
              {deal.cons.map((con: string, i: number) => <li key={i}>✗ {con}</li>)}
            </ul>
          </div>
        )}
      </div>

      <div className="flex gap-2 pt-4 border-t border-slate-700 mt-auto">
        {deal.status === 'PENDING' && (
          <>
            <button 
              onClick={() => handleStatusChange('APPROVED')}
              disabled={loading}
              className="flex-1 bg-emerald-500 hover:bg-emerald-600 text-white py-2 rounded-lg transition-colors font-medium text-sm"
            >
              Approve & Publish
            </button>
            <button 
              onClick={() => handleStatusChange('REJECTED')}
              disabled={loading}
              className="flex-1 bg-slate-700 hover:bg-slate-600 text-white py-2 rounded-lg transition-colors font-medium text-sm border border-slate-600"
            >
              Reject
            </button>
          </>
        )}
      </div>
    </div>
  );
}
