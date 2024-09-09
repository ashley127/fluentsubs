import React from "react";
import axios from "axios";

interface FileSubmitProps {
    fileIds: string[];
}

export function FileSubmit({ fileIds }: FileSubmitProps) {

    const handleSubmit = async () => {
        try {
            // Make a POST request to process-video endpoint
            const response = await axios.post('/process-video', { fileIds });
            console.log("Processing complete:", response.data);
        } catch (error) {
            console.error("Error processing files:", error);
        }
    };

    return (
        <button 
            className="mt-[20px] p-[2px] relative"
            onClick={handleSubmit}
        >
            <div className="absolute inset-0 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-lg" />
            <div className="px-8 py-2 bg-black rounded-[6px] relative group transition duration-200 text-white hover:bg-transparent">
                Submit
            </div>
        </button>
    );
}
