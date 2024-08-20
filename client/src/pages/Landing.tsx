import React from "react";
import { FlipWords } from "../components/flip-words.tsx";
import '../App.css'
import { MacbookScroll } from "../components/macbook-scroll.tsx";
import Button from '@mui/material/Button';

export default function Landing() {
  const words = ["anime", "movies", "shows", "videos"];

  return (
    <div >
      <nav className = "fixed top-0 left-0 w-full bg-black text-white shadow-lg z-10 border-b border-gray-600">
        <div className="container mx-auto flex justify-between items-center p-4">
          <div className="text-lg font-semibold">
            FluentSubs
          </div>
          <div className="flex space-x-4">
            <button className="text-white">Log in</button>
            <button className="bg-gray-700 text-white px-4 py-2 rounded">Sign up</button>
          </div>
        </div>
      </nav>
      <div className=" overflow-hidden bg-[#0B0B0F] w-full">
        <MacbookScroll
          title={
            <span>
              Create subtitles in an instant <br /> No kidding.
              </span>
          }
          src={"https://i.ibb.co/55wQ0pR/thumbnail-new.png"}
          showGradient={false}
        /> 
         <div className="flex justify-center items-center mt-[-10px]">
          <Button variant="contained" href="#contained-buttons">
            Get started for free 
          </Button>
         </div>
      </div>
    </div>
  );
}

