'use client'

import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { fileService } from '@/services/fileService';

export default function FileArchivePage() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  
  // Hardcoded user ID for demo purposes. This should come from an auth context.
  const [uploaderId, setUploaderId] = useState<string>('00000000-0000-0000-0000-000000000000');

  const uploadMutation = useMutation({
    mutationFn: (data: { file: File, uploaderId: string }) => fileService.uploadFile(data.file, data.uploaderId),
    onSuccess: (data) => {
      alert(`File uploaded successfully! ID: ${data.id}`);
      setSelectedFile(null); // reset form
    },
    onError: (error) => {
      console.error(error);
      alert('Failed to upload file.');
    }
  });

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setSelectedFile(e.target.files[0]);
    }
  };

  const handleUpload = (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedFile) {
      alert('Please select a file first.');
      return;
    }
    uploadMutation.mutate({ file: selectedFile, uploaderId });
  };

  return (
    <div className="p-6 max-w-3xl mx-auto">
      <h1 className="text-2xl font-bold mb-6">File Archive</h1>

      <div className="bg-white shadow rounded p-6">
        <h2 className="text-xl font-semibold mb-4">Upload New Document</h2>
        
        <form onSubmit={handleUpload} className="space-y-4">
          <div className="border-2 border-dashed border-gray-300 rounded-lg p-10 text-center hover:bg-gray-50 transition">
            <input 
              type="file" 
              id="fileInput" 
              className="hidden" 
              onChange={handleFileChange} 
            />
            <label htmlFor="fileInput" className="cursor-pointer">
              <div className="text-primary mb-2">
                <i className="tabler-upload text-3xl"></i>
              </div>
              {selectedFile ? (
                <span className="font-semibold text-gray-800">{selectedFile.name}</span>
              ) : (
                <span className="text-gray-500">Click to browse or drag and drop a file here</span>
              )}
            </label>
          </div>

          <button 
            type="submit" 
            disabled={uploadMutation.isPending || !selectedFile}
            className="w-full bg-primary text-white py-2 rounded shadow hover:bg-primary-dark disabled:opacity-50"
          >
            {uploadMutation.isPending ? 'Uploading...' : 'Upload File'}
          </button>
        </form>
      </div>
    </div>
  );
}
