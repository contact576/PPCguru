import "./globals.css";

export const metadata = {
  title: "GCAD Construction — Ads Performance Dashboard",
  description: "Daily Google Ads + Meta Ads performance for GCAD Construction, by PPC Guru.",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
