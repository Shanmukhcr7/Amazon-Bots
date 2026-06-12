'use client';

import { useEffect, useState } from 'react';
import { fetchProducts } from '@/lib/api';

export default function ProductsPage() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadProducts = async () => {
      try {
        const data = await fetchProducts();
        setProducts(data);
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    };
    loadProducts();
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold mb-2">Monitored Products</h1>
          <p className="text-slate-400">All products currently being tracked for deals.</p>
        </div>
      </div>

      {loading ? (
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-emerald-500"></div>
        </div>
      ) : products.length === 0 ? (
        <div className="text-center py-20 bg-slate-800/30 rounded-2xl border border-slate-800 border-dashed">
          <p className="text-slate-400">No products monitored yet.</p>
        </div>
      ) : (
        <div className="bg-slate-800/50 rounded-xl border border-slate-700 overflow-hidden">
          <table className="w-full text-left">
            <thead className="bg-slate-900/50 border-b border-slate-700">
              <tr>
                <th className="p-4 font-medium text-slate-300">Product</th>
                <th className="p-4 font-medium text-slate-300">Brand</th>
                <th className="p-4 font-medium text-slate-300">Category</th>
                <th className="p-4 font-medium text-slate-300 text-right">Current Price</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-700/50">
              {products.map((p: any) => {
                const latestPrice = p.price_history && p.price_history.length > 0 
                  ? p.price_history[p.price_history.length - 1].price 
                  : 'N/A';
                
                return (
                  <tr key={p.id} className="hover:bg-slate-700/20 transition-colors">
                    <td className="p-4">
                      <a href={p.url} target="_blank" rel="noreferrer" className="text-blue-400 hover:text-blue-300 font-medium">
                        {p.name}
                      </a>
                    </td>
                    <td className="p-4 text-slate-300">{p.brand}</td>
                    <td className="p-4 text-slate-300">{p.category}</td>
                    <td className="p-4 text-right font-mono text-emerald-400">
                      {latestPrice !== 'N/A' ? `$${latestPrice}` : latestPrice}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
