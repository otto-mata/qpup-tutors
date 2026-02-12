// app/dashboard/page.tsx
"use client";

import { useAuth } from "../context/AuthContext";
import { useRouter } from "next/navigation";
import {
  Dispatch,
  FormEvent,
  SetStateAction,
  useEffect,
  useReducer,
  useState,
} from "react";

interface Question {
  ID: number;
  Question: string;
  Answer: string;
  Author: string;
}

const jsonIsQuestionArray = (data: any): data is Question[] => {
  if (!(data instanceof Array)) return false;
  return data.every((val, idx, arr) => {
    return (
      val instanceof Object &&
      Object.hasOwn(val, "ID") &&
      Object.hasOwn(val, "Question") &&
      Object.hasOwn(val, "Answer") &&
      Object.hasOwn(val, "Author")
    );
  });
};

const fetchQuestions = async (): Promise<Question[]> => {
  const response = await fetch("http://localhost:3000/api/question", {
    method: "GET",
    credentials: "include",
    headers: { "Content-Type": "application/json" },
  });
  if (!response.ok) return [];
  const data = await response.json();
  if (!jsonIsQuestionArray(data)) return [];
  return data;
};

export default function Dashboard() {
  const { user, loading, logout } = useAuth();
  const router = useRouter();
  const [questions, setQuestions] = useState<Question[]>([]);
  const [isLoading, setLoading] = useState<boolean>(false);

  fetchQuestions().then(setQuestions);
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

  setInterval(async () => {
    setLoading(true);
    setQuestions(await fetchQuestions());
    setLoading(false);
  }, 60000);
  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const formData = new FormData(event.currentTarget);
    const question = formData.get("question");
    const answer = formData.get("answer");

    const response = await fetch("http://localhost:3000/api/question", {
      method: "POST",
      credentials: "include",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question, answer }),
    });

    if (response.ok) {
      const { success } = await response.json();
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

        <div className="mt-8 rounded-lg bg-gray-900 p-6 shadow ">
          <div className="flex items-center space-x-4">
            <form
              action=""
              onSubmit={handleSubmit}
              className="flex items-center align-middle justify-center space-x-4"
            >
              <input
                type="text"
                name="question"
                id="question"
                placeholder="Question"
                className="border rounded-md h-9 px-4 py-2 "
              />
              <input
                type="text"
                name="answer"
                id="answer"
                placeholder="Answer"
                className="border rounded-md h-9 px-4 py-2 "
              />
              <input
                type="submit"
                value="Submit"
                className="uppercase inline-flex items-center justify-center gap-2 whitespace-nowrap text-sm font-medium transition-all disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg:not([class*='size-'])]:size-4 shrink-0 [&_svg]:shrink-0 outline-none focus-visible:border-ring focus-visible:ring-ring/50 focus-visible:ring-[3px] aria-invalid:ring-destructive/40 aria-invalid:border-destructive shadow-xs hover:text-accent-foreground h-9 px-4 py-2 has-[>svg]:px-3 relative rounded-md cursor-pointer border text-foreground border-white/20 bg-white/10 hover:bg-white/15"
              />
            </form>
          </div>
        </div>
        <div>
          {isLoading ? (
            <span>Loading...</span>
          ) : (
            <ul>
              {questions.map((e) => {
                return <li key={e.ID}>{e.Question}</li>;
              })}
            </ul>
          )}
        </div>
      </div>
    </div>
  );
}
