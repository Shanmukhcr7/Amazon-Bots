import Link from 'next/link';

export default function Navbar() {
  return (
    <nav className="bg-slate-900 border-b border-slate-800 p-4 sticky top-0 z-50">
      <div className="container mx-auto flex justify-between items-center">
        <Link href="/" className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-emerald-400">
          Affiliate Deal Discovery
        </Link>
        <div className="flex gap-4">
          <Link href="/" className="hover:text-blue-400 transition-colors">Deals</Link>
          <Link href="/products" className="hover:text-emerald-400 transition-colors">Products</Link>
        </div>
      </div>
    </nav>
  );
}
