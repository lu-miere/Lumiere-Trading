import "../globals.css"; // Import global styles for Tailwind
import React from "react"; // Explicitly import React for type resolution

// Metadata is required for a root layout
export const metadata = {
  title: "Lumiere Trading",
  description: 'Hashid"s Trding Platform',
};

// The root layout component must accept a 'children' prop and return <html> and <body> tags.
export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-gray-50 min-h-screen">
        {/* Children (your page.tsx and other routes) will render here */}
        {children}
      </body>
    </html>
  );
}
