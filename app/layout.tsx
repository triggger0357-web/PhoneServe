import './globals.css'
import { Analytics } from '@vercel/analytics/next'

export const metadata = {
  title: 'Edge Tech Knowledgey',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        {children}
        <Analytics />
      </body>
    </html>
  )
}