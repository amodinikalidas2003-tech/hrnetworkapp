import apiClient from './apiClient';

export interface HrDashboardStatsDTO {
  totalUsers: number;
  totalDepartments: number;
  totalFormsCreated: number;
  totalFormSubmissions: number;
  submissionsByForm: Record<string, number>;
  averageOverallScore: number;
}

export const dashboardService = {
  getGlobalStats: (): Promise<HrDashboardStatsDTO> => {
    return apiClient.get('/dashboard/stats');
  }
};
