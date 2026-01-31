// app/dashboard/page.tsx
"use client";

import { useAuth } from "../context/AuthContext";
import { useRouter } from "next/navigation";
import { FormEvent, useEffect } from "react";

export default function Dashboard() {
  const { user, loading, logout } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading && !user) {
      router.push("/");
    }
  }, [user, loading, router]);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (!user) {
    return null;
  }

  const handleLogout = async () => {
    await logout();
    router.push("/");
  };
  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const formData = new FormData(event.currentTarget);
    const question = formData.get("question");
    const answer = formData.get("answer");

    const response = await fetch("http://localhost:3000/api/auth/login", {
      method: "POST",
      credentials: "include",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question, answer }),
    });

    if (response.ok) {
    } else {
      // Handle errors
    }
  }
  return (
    <div className="min-h-screen p-8">
      <div className="mx-auto max-w-4xl">
        <div className="flex items-center justify-between">
          <h1 className="text-3xl font-bold">Dashboard</h1>
          <button
            onClick={handleLogout}
            className="uppercase inline-flex items-center justify-center gap-2 whitespace-nowrap text-sm font-medium transition-all disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg:not([class*='size-'])]:size-4 shrink-0 [&_svg]:shrink-0 outline-none focus-visible:border-ring focus-visible:ring-ring/50 focus-visible:ring-[3px] aria-invalid:ring-destructive/40 aria-invalid:border-destructive shadow-xs hover:text-accent-foreground h-9 px-4 py-2 has-[>svg]:px-3 relative rounded-md cursor-pointer border text-foreground border-white/20 bg-white/10 hover:bg-white/15"
          >
            Logout
          </button>
        </div>

        <div className="mt-8 rounded-lg bg-white p-6 shadow">
          <div className="flex items-center space-x-4">
            <form action=""></form>
          </div>
        </div>
      </div>
    </div>
  );
}
