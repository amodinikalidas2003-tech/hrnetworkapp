import apiClient from './apiClient';

export interface FileArchiveDTO {
  id?: string;
  originalFileName: string;
  contentType: string;
  size: number;
  uploadedById: string;
  createdAt: string;
}

export const fileService = {
  uploadFile: (file: File, uploaderId: string): Promise<FileArchiveDTO> => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('uploaderId', uploaderId);

    // Override Content-Type for multipart/form-data. Axios will auto-set boundary.
    return apiClient.post('/files/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  }
};
