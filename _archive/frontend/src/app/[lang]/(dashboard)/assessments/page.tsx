'use client'

import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { orgService } from '@/services/orgService';
import { assessmentService } from '@/services/assessmentService';

export default function AssessmentsPage() {
  const [selectedUserId, setSelectedUserId] = useState<string>('');

  const { data: usersData, isLoading: usersLoading } = useQuery({
    queryKey: ['users'],
    queryFn: () => orgService.getAllUsers(0, 100)
  });

  const { data: scores, isLoading: scoresLoading } = useQuery({
    queryKey: ['assessments', selectedUserId],
    queryFn: () => assessmentService.getScoresForUser(selectedUserId),
    enabled: !!selectedUserId
  });

  const users = usersData?.content || [];

  return (
    <div className="p-6 max-w-5xl mx-auto">
      <h1 className="text-2xl font-bold mb-6">Employee Assessments & Scoring</h1>

      <div className="bg-white shadow rounded p-6 mb-6">
        <label className="block text-sm font-medium mb-2">Select Employee to View Scores</label>
        <select 
          className="w-full border rounded p-2"
          value={selectedUserId}
          onChange={(e) => setSelectedUserId(e.target.value)}
        >
          <option value="">-- Select an employee --</option>
          {users.map((u: any) => (
            <option key={u.id} value={u.id}>{u.username} ({u.email})</option>
          ))}
        </select>
      </div>

      {selectedUserId && (
        <div className="bg-white shadow rounded p-6">
          <h2 className="text-xl font-semibold mb-4">Assessment Results</h2>
          
          {scoresLoading ? (
            <p>Loading scores...</p>
          ) : !scores || scores.length === 0 ? (
            <p className="text-gray-500">No assessments found for this user.</p>
          ) : (
            <div className="space-y-6">
              {scores.map((score: any) => (
                <div key={score.id} className="border p-4 rounded bg-gray-50">
                  <div className="flex justify-between items-center mb-4">
                    <span className="font-bold text-lg">Total Score: {score.totalScore.toFixed(1)}</span>
                    <span className="text-sm text-gray-500">Date: {new Date(score.createdAt).toLocaleDateString()}</span>
                  </div>
                  
                  <h4 className="text-sm font-semibold mb-2 text-gray-700">Dimension Scores:</h4>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    {Object.entries(score.dimensionScores).map(([dim, val]) => (
                      <div key={dim} className="bg-white p-2 rounded shadow-sm border text-center">
                        <div className="text-xs text-gray-500 uppercase">{dim}</div>
                        <div className="font-semibold text-lg">{Number(val)}</div>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
