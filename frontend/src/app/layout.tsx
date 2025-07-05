import type { Metadata } from 'next';
import { Geist, Geist_Mono } from 'next/font/google';

import Layout from '@/components/layout/Layout';

import './globals.css';

const geistSans = Geist({
  variable: '--font-geist-sans',
  subsets: ['latin'],
});

const geistMono = Geist_Mono({
  variable: '--font-geist-mono',
  subsets: ['latin'],
});

export const metadata: Metadata = {
  title: 'HTMLpageGen - Генератор HTML-страниц с AI',
  description:
    'Создавайте красивые и оптимизированные HTML-страницы с помощью искусственного интеллекта',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang='ru' className='dark'>
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased bg-[#0D1117] text-white`}
      >
        <Layout>{children}</Layout>
      </body>
    </html>
  );
}
