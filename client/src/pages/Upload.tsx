import React from 'react'
import { FileUpload } from '../components/file-upload.tsx'
import { useState } from "react";

function Upload() {
    const [files, setFiles] = useState<File[]>([]);
    const handleFileUpload = (files: File[]) => {
        setFiles(files);
        console.log(files);
    };
  return (
    <div className='fixed inset-0 bg-black flex items-center justify-center'>
      <div className="w-full max-w-4xl min-h-96 border border-dashed bg-black border-neutral-800 rounded-lg">
      <FileUpload onChange={handleFileUpload} />
      </div>
    </div>
  )
}

export default Upload