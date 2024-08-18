import React from "react";
import { FlipWords } from "../components/flip-words.tsx";
import '../App.css'
import { MacbookScroll } from "../components/macbook-scroll.tsx";

export default function Landing() {
  const words = ["anime", "movies", "shows", "videos"];

  return (
    <div className = "bg-black min-h-screen ">
      <nav className = "fixed top-0 left-0 w-full bg-black text-white shadow-lg z-10 border-b border-gray-600">
        <div class="container mx-auto flex justify-between items-center p-4">
          <div class="text-lg font-semibold">
            FluentSubs
          </div>
          <div class="flex space-x-4">
            <button class="text-white">Log in</button>
            <button class="bg-gray-700 text-white px-4 py-2 rounded">Sign up</button>
          </div>
        </div>
      </nav>
      <div className="overflow-hidden bg-[#0B0B0F] w-full">
      <MacbookScroll
        title={
          <span>
            Create subtitles in an instant <br /> No kidding.
          </span>
        }
        src={"https://assets-prd.ignimgs.com/2021/09/02/demon-slayer-moment-1-1630545040097.jpg"}
        showGradient={false}
      />
    </div>

    </div>
  );
}

