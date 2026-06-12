const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

export async function fetchDeals(status?: str) {
  const url = new URL(`${API_URL}/deals`);
  if (status) {
    url.searchParams.append('status', status);
  }
  
  const res = await fetch(url.toString(), { cache: 'no-store' });
  if (!res.ok) {
    throw new Error('Failed to fetch deals');
  }
  return res.json();
}

export async function updateDealStatus(id: string, status: string) {
  const res = await fetch(`${API_URL}/deals/${id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ status }),
  });
  
  if (!res.ok) {
    throw new Error('Failed to update deal status');
  }
  return res.json();
}

export async function fetchProducts() {
  const res = await fetch(`${API_URL}/products`, { cache: 'no-store' });
  if (!res.ok) {
    throw new Error('Failed to fetch products');
  }
  return res.json();
}
