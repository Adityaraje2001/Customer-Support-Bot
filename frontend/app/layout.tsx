import "./globals.css";

export const metadata = {
  title: "AI Customer Support Agent",
  description: "Minimal UI for AI Customer Support Agent",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
