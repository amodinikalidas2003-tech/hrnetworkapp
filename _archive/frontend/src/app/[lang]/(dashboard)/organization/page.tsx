'use client'

import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { orgService, DepartmentDTO } from '@/services/orgService';

export default function OrganizationPage() {
  const queryClient = useQueryClient();
  const [newDeptName, setNewDeptName] = useState('');
  const [parentId, setParentId] = useState<string | undefined>(undefined);

  const { data: deptsData, isLoading } = useQuery({
    queryKey: ['departments'],
    queryFn: () => orgService.getAllDepartments(0, 100)
  });

  const createDeptMutation = useMutation({
    mutationFn: orgService.createDepartment,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['departments'] });
      setNewDeptName('');
      setParentId(undefined);
    }
  });

  const handleCreate = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newDeptName) return;
    createDeptMutation.mutate({ name: newDeptName, parentId });
  };

  const departments: DepartmentDTO[] = deptsData?.content || [];

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">Organization Structure</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Create Department Form */}
        <div className="bg-white shadow rounded p-6 h-fit">
          <h2 className="text-xl font-semibold mb-4">Add Department / Team</h2>
          <form onSubmit={handleCreate} className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-1">Name</label>
              <input
                type="text"
                value={newDeptName}
                onChange={(e) => setNewDeptName(e.target.value)}
                className="w-full border rounded p-2"
                placeholder="e.g., Engineering, Marketing"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Parent Department (Optional)</label>
              <select
                value={parentId || ''}
                onChange={(e) => setParentId(e.target.value || undefined)}
                className="w-full border rounded p-2"
              >
                <option value="">None (Top Level)</option>
                {departments.map((dept) => (
                  <option key={dept.id} value={dept.id}>{dept.name}</option>
                ))}
              </select>
            </div>
            <button
              type="submit"
              disabled={createDeptMutation.isPending}
              className="bg-primary text-white px-4 py-2 rounded shadow hover:bg-primary-dark w-full"
            >
              {createDeptMutation.isPending ? 'Creating...' : 'Create Department'}
            </button>
          </form>
        </div>

        {/* Departments List */}
        <div className="bg-white shadow rounded p-6">
          <h2 className="text-xl font-semibold mb-4">Current Structure</h2>
          {isLoading ? (
            <p>Loading...</p>
          ) : departments.length === 0 ? (
            <p className="text-gray-500">No departments found.</p>
          ) : (
            <ul className="space-y-2">
              {departments.filter(d => !d.parentId).map(topDept => (
                <li key={topDept.id} className="p-3 border rounded bg-gray-50">
                  <span className="font-semibold">{topDept.name}</span>
                  
                  {/* Render Sub-departments */}
                  <ul className="mt-2 ml-4 space-y-1 border-l-2 border-gray-200 pl-4">
                    {departments.filter(d => d.parentId === topDept.id).map(subDept => (
                      <li key={subDept.id} className="text-sm text-gray-700">
                        ↳ {subDept.name}
                      </li>
                    ))}
                  </ul>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  );
}
