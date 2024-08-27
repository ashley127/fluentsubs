import React from "react";
import { FlipWords } from "../components/flip-words.tsx";
import '../App.css'
import { MacbookScroll } from "../components/macbook-scroll.tsx";
import Button from '@mui/material/Button';
import { StickyScroll } from "../components/sticky-scroll-reveal.tsx";
import SendIcon from '@mui/icons-material/Send';


export default function Landing() {
  const words = ["anime", "movies", "shows", "videos"];

  const content = [
    {
      title: "Collaborative Editing",
      description:
        "Work together in real time with your team, clients, and stakeholders. Collaborate on documents, share ideas, and make decisions quickly. With our platform, you can streamline your workflow and increase productivity.",
      content: (
        <div className="h-full w-full bg-[linear-gradient(to_bottom_right,var(--cyan-500),var(--emerald-500))] flex items-center justify-center text-white">
          Collaborative Editing
        </div>
      ),
    },
    {
      title: "Real time changes",
      description:
        "See changes as they happen. With our platform, you can track every modification in real time. No more confusion about the latest version of your project. Say goodbye to the chaos of version control and embrace the simplicity of real-time updates.",
      content: (
        <div className="h-full w-full  flex items-center justify-center text-white">
          <img
            src="/linear.webp"
            width={300}
            height={300}
            className="h-full w-full object-cover"
            alt="linear board demo"
          />
        </div>
      ),
    },
    {
      title: "Version control",
      description:
        "Experience real-time updates and never stress about version control again. Our platform ensures that you're always working on the most recent version of your project, eliminating the need for constant manual updates. Stay in the loop, keep your team aligned, and maintain the flow of your work without any interruptions.",
      content: (
        <div className="h-full w-full bg-[linear-gradient(to_bottom_right,var(--orange-500),var(--yellow-500))] flex items-center justify-center text-white">
          Version control
        </div>
      ),
    },
    {
      title: "Running out of content",
      description:
        "Experience real-time updates and never stress about version control again. Our platform ensures that you're always working on the most recent version of your project, eliminating the need for constant manual updates. Stay in the loop, keep your team aligned, and maintain the flow of your work without any interruptions.",
      content: (
        <div className="h-full w-full bg-[linear-gradient(to_bottom_right,var(--cyan-500),var(--emerald-500))] flex items-center justify-center text-white">
          Running out of content
        </div>
      ),
    },
  ];



  return (
    <body className="bg-[#0B0B0F] h-full">
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
      </div>
      <h1 className = "text-4xl font-bold text-white mb-6 ">How it works</h1>
      <div className="overflow-hidden">
        <StickyScroll content={content} />
      </div>
      <br/>
      <div className="flex justify-center w-full">
        <Button variant="contained" endIcon={<SendIcon />} href="upload">
          Get started
        </Button>
      </div>
    </body>
  );
}

