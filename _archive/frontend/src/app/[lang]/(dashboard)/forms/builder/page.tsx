'use client'

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { formService } from '@/services/formService';

type FieldType = 'text' | 'number' | 'date' | 'select' | 'checkbox';

interface FormField {
  id: string;
  name: string;
  label: string;
  type: FieldType;
  required: boolean;
  options?: string[]; // for select type
}

export default function FormBuilder() {
  const router = useRouter();
  const [formName, setFormName] = useState('');
  const [description, setDescription] = useState('');
  const [fields, setFields] = useState<FormField[]>([]);

  const addField = (type: FieldType) => {
    const newField: FormField = {
      id: `field_${Date.now()}`,
      name: `field_${Date.now()}`,
      label: 'New Field',
      type,
      required: false,
    };
    setFields([...fields, newField]);
  };

  const updateField = (id: string, updates: Partial<FormField>) => {
    setFields(fields.map(f => (f.id === id ? { ...f, ...updates } : f)));
  };

  const removeField = (id: string) => {
    setFields(fields.filter(f => f.id !== id));
  };

  const saveForm = async () => {
    try {
      // Build schema definition mapping
      const schemaDefinition = fields.reduce((acc, field) => {
        acc[field.name] = {
          label: field.label,
          type: field.type,
          required: field.required,
          ...(field.options && { options: field.options })
        };
        return acc;
      }, {} as Record<string, any>);

      await formService.createSchema({
        name: formName,
        description,
        schemaDefinition,
        // Mock createdById for now until Auth is integrated
        createdById: '00000000-0000-0000-0000-000000000000'
      });

      router.push('/forms');
    } catch (error) {
      console.error('Failed to save form schema:', error);
      alert('Failed to save form. Check console for details.');
    }
  };

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold mb-6">Form Builder (No-Code)</h1>

      <div className="bg-white shadow rounded p-6 mb-6">
        <div className="mb-4">
          <label className="block text-sm font-medium mb-1">Form Name</label>
          <input 
            type="text" 
            value={formName}
            onChange={(e) => setFormName(e.target.value)}
            className="w-full border rounded p-2"
            placeholder="e.g., Performance Review 2026"
          />
        </div>
        <div className="mb-4">
          <label className="block text-sm font-medium mb-1">Description</label>
          <textarea 
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="w-full border rounded p-2"
            placeholder="Optional description"
          />
        </div>
      </div>

      <div className="bg-white shadow rounded p-6 mb-6">
        <h2 className="text-xl font-semibold mb-4">Fields</h2>
        
        {fields.map((field, index) => (
          <div key={field.id} className="border p-4 rounded mb-4 flex gap-4 items-start bg-gray-50">
            <div className="flex-grow grid grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-medium mb-1">Label</label>
                <input 
                  type="text" 
                  value={field.label}
                  onChange={(e) => updateField(field.id, { label: e.target.value })}
                  className="w-full border rounded p-2 text-sm"
                />
              </div>
              <div>
                <label className="block text-xs font-medium mb-1">Key Name (API)</label>
                <input 
                  type="text" 
                  value={field.name}
                  onChange={(e) => updateField(field.id, { name: e.target.value })}
                  className="w-full border rounded p-2 text-sm"
                />
              </div>
              <div className="flex items-center mt-6">
                <input 
                  type="checkbox" 
                  checked={field.required}
                  onChange={(e) => updateField(field.id, { required: e.target.checked })}
                  className="mr-2"
                />
                <label className="text-sm">Required Field</label>
              </div>
            </div>
            <button 
              onClick={() => removeField(field.id)}
              className="text-red-500 hover:text-red-700 font-bold"
            >
              &times; Remove
            </button>
          </div>
        ))}

        <div className="flex gap-2 mt-4">
          <button onClick={() => addField('text')} className="bg-gray-200 px-3 py-1 rounded text-sm hover:bg-gray-300">+ Text</button>
          <button onClick={() => addField('number')} className="bg-gray-200 px-3 py-1 rounded text-sm hover:bg-gray-300">+ Number</button>
          <button onClick={() => addField('date')} className="bg-gray-200 px-3 py-1 rounded text-sm hover:bg-gray-300">+ Date</button>
          <button onClick={() => addField('checkbox')} className="bg-gray-200 px-3 py-1 rounded text-sm hover:bg-gray-300">+ Checkbox</button>
        </div>
      </div>

      <div className="flex justify-end">
        <button 
          onClick={saveForm}
          disabled={!formName}
          className="bg-primary text-white px-6 py-2 rounded shadow hover:bg-primary-dark disabled:opacity-50"
        >
          Save Form Schema
        </button>
      </div>
    </div>
  );
}
