import apiClient from './apiClient';

export interface DepartmentDTO {
  id?: string;
  name: string;
  parentId?: string;
  createdAt?: string;
  updatedAt?: string;
}

export interface UserDTO {
  id?: string;
  username: string;
  email: string;
  role: 'SUPER_ADMIN' | 'ADMIN' | 'MANAGER' | 'USER';
  departmentId?: string;
  createdAt?: string;
  updatedAt?: string;
}

export const orgService = {
  // Departments
  createDepartment: (dept: DepartmentDTO): Promise<DepartmentDTO> => {
    return apiClient.post('/departments', dept);
  },
  
  getAllDepartments: (page = 0, size = 100): Promise<any> => {
    return apiClient.get(`/departments?page=${page}&size=${size}`);
  },

  // Users
  createUser: (user: UserDTO): Promise<UserDTO> => {
    return apiClient.post('/users', user);
  },
  
  getAllUsers: (page = 0, size = 100): Promise<any> => {
    return apiClient.get(`/users?page=${page}&size=${size}`);
  }
};
