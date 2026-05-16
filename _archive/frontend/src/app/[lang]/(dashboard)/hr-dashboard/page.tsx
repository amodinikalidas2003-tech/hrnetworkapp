'use client'

import { useQuery } from '@tanstack/react-query';
import { dashboardService } from '@/services/dashboardService';

export default function HrDashboardPage() {
  const { data: stats, isLoading, error } = useQuery({
    queryKey: ['dashboardStats'],
    queryFn: () => dashboardService.getGlobalStats()
  });

  if (isLoading) return <div className="p-6">Loading dashboard data...</div>;
  if (error || !stats) return <div className="p-6 text-red-500">Failed to load dashboard data. Ensure backend is running.</div>;

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">HR Analytics Dashboard</h1>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="bg-white shadow rounded p-6 border-l-4 border-primary">
          <h3 className="text-gray-500 text-sm font-semibold uppercase">Total Users</h3>
          <p className="text-3xl font-bold mt-2">{stats.totalUsers}</p>
        </div>
        
        <div className="bg-white shadow rounded p-6 border-l-4 border-success">
          <h3 className="text-gray-500 text-sm font-semibold uppercase">Departments</h3>
          <p className="text-3xl font-bold mt-2">{stats.totalDepartments}</p>
        </div>

        <div className="bg-white shadow rounded p-6 border-l-4 border-info">
          <h3 className="text-gray-500 text-sm font-semibold uppercase">Dynamic Forms</h3>
          <p className="text-3xl font-bold mt-2">{stats.totalFormsCreated}</p>
        </div>

        <div className="bg-white shadow rounded p-6 border-l-4 border-warning">
          <h3 className="text-gray-500 text-sm font-semibold uppercase">Avg Overall Score</h3>
          <p className="text-3xl font-bold mt-2">{stats.averageOverallScore.toFixed(1)} / 100</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Submissions Stats */}
        <div className="bg-white shadow rounded p-6">
          <h2 className="text-xl font-semibold mb-4">Total Submissions: {stats.totalFormSubmissions}</h2>
          <div className="space-y-4">
            {Object.entries(stats.submissionsByForm || {}).map(([formName, count]) => (
              <div key={formName} className="flex justify-between items-center border-b pb-2">
                <span className="text-gray-700">{formName}</span>
                <span className="font-semibold bg-gray-100 px-3 py-1 rounded">{Number(count)}</span>
              </div>
            ))}
            {Object.keys(stats.submissionsByForm || {}).length === 0 && (
              <p className="text-gray-500 text-sm">No form submissions data available yet.</p>
            )}
          </div>
        </div>

        {/* Quick Actions / Getting Started */}
        <div className="bg-white shadow rounded p-6">
          <h2 className="text-xl font-semibold mb-4">Quick Actions</h2>
          <ul className="space-y-3">
            <li>
              <a href="/forms/builder" className="text-primary hover:underline flex items-center">
                <i className="tabler-plus mr-2" /> Create New Assessment Form
              </a>
            </li>
            <li>
              <a href="/organization" className="text-primary hover:underline flex items-center">
                <i className="tabler-sitemap mr-2" /> Manage Org Structure
              </a>
            </li>
            <li>
              <a href="/forms" className="text-primary hover:underline flex items-center">
                <i className="tabler-list mr-2" /> View Existing Forms
              </a>
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
}
