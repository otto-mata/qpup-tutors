"use client";

import { SmallLogo42 } from "./components/Small42";

export default function Home() {
  const handleLogin = () => {
    window.location.href = "http://localhost:3000/auth/forty_two";
  };
  return (
    <div className="flex flex-col bg-background text-white h-full min-h-screen">
      <div className="flex-1 flex flex-col justify-center items-center p-4 sm:p-6 lg:p-8 overflow-y-auto z-99">
        <div className="w-full max-w-md p-6 sm:p-8">
          <button
            onClick={handleLogin}
            className="uppercase inline-flex items-center justify-center gap-2 whitespace-nowrap text-sm font-medium transition-all disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg:not([class*='size-'])]:size-4 shrink-0 [&_svg]:shrink-0 outline-none focus-visible:border-ring focus-visible:ring-ring/50 focus-visible:ring-[3px] aria-invalid:ring-destructive/40 aria-invalid:border-destructive shadow-xs hover:text-accent-foreground h-9 px-4 py-2 has-[>svg]:px-3 relative w-full rounded-md cursor-pointer border text-foreground border-white/20 bg-white/10 hover:bg-white/15"
          >
            <SmallLogo42 />
            Continue with intra
          </button>
        </div>
      </div>
    </div>
  );
}
