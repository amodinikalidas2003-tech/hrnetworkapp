import apiClient from './apiClient';

export interface AssessmentScoreDTO {
  id?: string;
  evaluatedUserId: string;
  evaluatorUserId: string;
  submissionId?: string;
  dimensionScores: Record<string, number>;
  totalScore?: number;
  createdAt?: string;
}

export const assessmentService = {
  createScore: (score: AssessmentScoreDTO): Promise<AssessmentScoreDTO> => {
    return apiClient.post('/assessments', score);
  },
  
  getScoresForUser: (userId: string): Promise<AssessmentScoreDTO[]> => {
    return apiClient.get(`/assessments/users/${userId}`);
  }
};
