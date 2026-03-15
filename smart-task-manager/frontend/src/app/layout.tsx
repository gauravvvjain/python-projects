import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import "./calendar.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Smart Task Manager",
  description: "AI-powered auto-updating task manager synced with Google Calendar",
  manifest: "/manifest.json",
  themeColor: "#020617",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>
        {children}
      </body>
    </html>
  );
}
