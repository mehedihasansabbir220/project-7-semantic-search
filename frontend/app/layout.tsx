import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Semantic Search',
  description: 'AI-powered semantic search engine',
  authors: [{ name: 'Claude' }],
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <head>
        <meta charSet="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <meta name="theme-color" content="#0ea5e9" />
      </head>
      <body>
        {children}
      </body>
    </html>
  );
}
