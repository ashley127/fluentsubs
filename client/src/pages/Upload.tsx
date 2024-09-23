import React, { useState } from 'react';
import { FileUpload } from '../components/file-upload.tsx';
import axios from 'axios';

function Upload() {
    const [files, setFiles] = useState<File[]>([]);
    const [fileIds, setFileIds] = useState<string[]>([]);

    const handleFileUpload = async (files: File[]) => {
        setFiles(files);
    
        const formData = new FormData();
        files.forEach((file) => formData.append('file', file));
    
        try {
            const response = await axios.post('http://127.0.0.1:5000/upload', formData, {
                headers: { 'Content-Type': 'multipart/form-data' },
            });
    
            console.log('Upload response:', response.data); // Log the response
    
            // Check if `file_id` is present
            const uploadedFileId = response.data.file_id;
            if (uploadedFileId) {
                setFileIds([uploadedFileId]); // Store it as an array with one element
            } else {
                console.error('Unexpected file_ids format:', response.data);
            }
        } catch (error) {
            console.error('Error uploading files:', error);
        }
    };
    

    const handleSubmit = async () => {
        console.log('Submit button clicked');
        console.log('File IDs:', fileIds);
    
        if (fileIds.length === 0) {
            console.log('No file IDs available.');
            return;
        }
    
        try {
            const response = await axios.post('http://127.0.0.1:5000/process-video', { file_ids: fileIds , withCredentials: true });
            console.log('Processing response:', response.data);
        } catch (error) {
            console.error('Error processing video:', error);
        }
    };

    return (
        <>
            <div className='fixed flex flex-col inset-0 bg-black items-center justify-center'>
                <div className="w-full max-w-4xl min-h-96 border border-dashed bg-black border-neutral-800 rounded-lg">
                    <FileUpload onChange={handleFileUpload} />
                </div>

                <button 
                    className="px-4 py-2 rounded-md border border-neutral-300 bg-neutral-100 text-neutral-500 text-sm hover:-translate-y-1 transform transition duration-200 hover:shadow-md"
                    onClick={handleSubmit}
                    disabled={fileIds.length === 0}
                >
                    Submit
                </button>
            </div>
        </>
    );
}

export default Upload;
