import apiClient from './apiClient';

export interface FormSchemaDTO {
  id?: string;
  name: string;
  description?: string;
  schemaDefinition: Record<string, any>;
  createdById?: string;
  createdAt?: string;
  updatedAt?: string;
}

export interface FormSubmissionDTO {
  id?: string;
  schemaId: string;
  data: Record<string, any>;
  submittedById?: string;
  createdAt?: string;
  updatedAt?: string;
}

export interface PageResponse<T> {
  content: T[];
  pageable: any;
  totalElements: number;
  totalPages: number;
}

export const formService = {
  // Form Schemas
  createSchema: (schema: FormSchemaDTO): Promise<FormSchemaDTO> => {
    return apiClient.post('/forms/schemas', schema);
  },
  
  getAllSchemas: (page = 0, size = 20): Promise<PageResponse<FormSchemaDTO>> => {
    return apiClient.get(`/forms/schemas?page=${page}&size=${size}`);
  },
  
  getSchemaById: (id: string): Promise<FormSchemaDTO> => {
    return apiClient.get(`/forms/schemas/${id}`);
  },

  // Form Submissions
  submitForm: (submission: FormSubmissionDTO): Promise<FormSubmissionDTO> => {
    return apiClient.post('/forms/submissions', submission);
  },
  
  getAllSubmissions: (page = 0, size = 20): Promise<PageResponse<FormSubmissionDTO>> => {
    return apiClient.get(`/forms/submissions?page=${page}&size=${size}`);
  }
};
