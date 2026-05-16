import { formService, FormSchemaDTO } from '@/services/formService';
import Link from 'next/link';

export default async function FormsPage() {
  // Fetch forms from backend (Server-side rendering)
  let forms: FormSchemaDTO[] = [];
  try {
    const response = await formService.getAllSchemas(0, 20);
    forms = response.content;
  } catch (error) {
    console.error('Failed to fetch forms:', error);
  }

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Forms Management</h1>
        <Link 
          href="/forms/builder" 
          className="bg-primary text-white px-4 py-2 rounded shadow hover:bg-primary-dark transition"
        >
          Create New Form
        </Link>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {forms.length === 0 ? (
          <p className="text-gray-500">No forms found. Create one to get started!</p>
        ) : (
          forms.map((form) => (
            <div key={form.id} className="bg-surface shadow rounded p-4 border border-border">
              <h2 className="text-xl font-semibold mb-2">{form.name}</h2>
              <p className="text-gray-600 mb-4">{form.description || 'No description provided.'}</p>
              <div className="flex space-x-2">
                <Link href={`/forms/${form.id}`} className="text-primary hover:underline">
                  View Form
                </Link>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
