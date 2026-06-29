import "./globals.css";
import type { ReactNode } from "react";

export const metadata = {
  title: "CEO 데일리 브리핑 — 리더 검토",
  description: "오전 9시 리더 보고가 CEO에게 전달되기 전, 사람이 검토하는 휴먼인더루프 화면.",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
