import React from "react";
import { FlipWords } from "../components/flip-words.tsx";
import '../App.css'
import { MacbookScroll } from "../components/macbook-scroll.tsx";
import Button from '@mui/material/Button';
import { StickyScroll } from "../components/sticky-scroll-reveal.tsx";
import SendIcon from '@mui/icons-material/Send';
import { AuroraBackground } from "../components/aurora-background.tsx";
import { motion } from 'framer-motion';

export default function Landing() {


  return (
    <body className="bg-[#0B0B0F] h-full">
      <nav className = "fixed top-0 left-0 w-full  text-white shadow-lg z-10 " style={{ backgroundColor: 'rgba(0, 0, 0, 0.6)' }}>
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

      <AuroraBackground>
      <motion.div
        initial={{ opacity: 0.0, y: 40 }}
        whileInView={{ opacity: 1, y: 0 }}
        transition={{
          delay: 0.3,
          duration: 0.8,
          ease: "easeInOut",
        }}
        className="relative flex flex-col gap-4 items-center justify-center px-4"
      >
        <div className="text-3xl md:text-7xl font-bold text-white text-center">
          Create subtitles in an instant.
        </div>
        <div className="font-extralight text-base md:text-4xl text-neutral-200 py-4">
          No kidding.
        </div>
        <a href="upload">
          <button className="bg-white rounded-full w-fit text-black px-4 py-2">
            Start now
          </button>
        </a>
      </motion.div>
    </AuroraBackground>
    </body>
  );
}

