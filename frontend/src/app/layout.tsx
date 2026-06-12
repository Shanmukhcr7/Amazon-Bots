import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Navbar from "@/components/Navbar";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Affiliate Deal Discovery",
  description: "Monitor and discover genuine product deals.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className={`${inter.className} antialiased bg-slate-900 text-slate-50 min-h-screen flex flex-col`}>
        <Navbar />
        <main className="flex-1 container mx-auto p-4 md:p-8">
          {children}
        </main>
      </body>
    </html>
  );
}
