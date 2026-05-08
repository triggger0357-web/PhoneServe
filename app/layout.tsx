import './globals.css'

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
      <body>{children}</body>
    </html>
  )
}