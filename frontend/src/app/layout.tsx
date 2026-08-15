"use client";
import { cn } from "@/lib/utils";
import { queryClient } from "@/libs/queryClient";
import { QueryClientProvider } from "@tanstack/react-query";
import { Geist } from "next/font/google";
import { Toaster } from "sonner";
import "./globals.css";

const geist = Geist({ subsets: ["latin"], variable: "--font-sans" });

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="en" className={cn("font-sans", geist.variable)}>
      <body className="min-h-full flex flex-col">
        <QueryClientProvider client={queryClient}>
          {children}
        </QueryClientProvider>
        <Toaster />
      </body>
    </html>
  );
}
