'use client'

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { formService, FormSchemaDTO } from '@/services/formService';
import { useQuery } from '@tanstack/react-query';

export default function FormRenderer({ params }: { params: { id: string } }) {
  const router = useRouter();
  const [formData, setFormData] = useState<Record<string, any>>({});

  const { data: schema, isLoading, error } = useQuery({
    queryKey: ['formSchema', params.id],
    queryFn: () => formService.getSchemaById(params.id)
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await formService.submitForm({
        schemaId: params.id,
        data: formData,
        submittedById: '00000000-0000-0000-0000-000000000000' // Mock user ID
      });
      alert('Form submitted successfully!');
      router.push('/forms');
    } catch (err) {
      console.error('Submission failed', err);
      alert('Failed to submit form.');
    }
  };

  const handleInputChange = (key: string, value: any) => {
    setFormData(prev => ({ ...prev, [key]: value }));
  };

  if (isLoading) return <div className="p-6">Loading form...</div>;
  if (error || !schema) return <div className="p-6 text-red-500">Failed to load form.</div>;

  return (
    <div className="p-6 max-w-3xl mx-auto bg-white shadow rounded mt-6">
      <h1 className="text-2xl font-bold mb-2">{schema.name}</h1>
      {schema.description && <p className="text-gray-600 mb-6">{schema.description}</p>}

      <form onSubmit={handleSubmit} className="space-y-6">
        {Object.entries(schema.schemaDefinition).map(([key, field]: [string, any]) => (
          <div key={key} className="flex flex-col">
            <label className="text-sm font-medium mb-1">
              {field.label} {field.required && <span className="text-red-500">*</span>}
            </label>
            
            {field.type === 'text' && (
              <input
                type="text"
                required={field.required}
                className="border rounded p-2"
                onChange={(e) => handleInputChange(key, e.target.value)}
              />
            )}
            
            {field.type === 'number' && (
              <input
                type="number"
                required={field.required}
                className="border rounded p-2"
                onChange={(e) => handleInputChange(key, Number(e.target.value))}
              />
            )}

            {field.type === 'date' && (
              <input
                type="date"
                required={field.required}
                className="border rounded p-2"
                onChange={(e) => handleInputChange(key, e.target.value)}
              />
            )}

            {field.type === 'checkbox' && (
              <div className="flex items-center">
                <input
                  type="checkbox"
                  required={field.required}
                  className="mr-2 h-4 w-4"
                  onChange={(e) => handleInputChange(key, e.target.checked)}
                />
                <span className="text-sm">Yes</span>
              </div>
            )}
          </div>
        ))}

        <div className="pt-4 border-t">
          <button 
            type="submit"
            className="w-full bg-primary text-white py-2 rounded shadow hover:bg-primary-dark transition"
          >
            Submit
          </button>
        </div>
      </form>
    </div>
  );
}
