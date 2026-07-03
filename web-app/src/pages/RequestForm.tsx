import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { useNavigate } from 'react-router-dom'
import toast from 'react-hot-toast'
import api from '../api/axios'

const requestSchema = z.object({
  title: z.string().min(1, 'Title is required').max(255),
  description: z.string().optional(),
  department: z.enum(['purchase', 'account', 'hr']),
  requested_by: z.string().min(1, 'Requester name is required'),
  amount: z.number().min(0.01, 'Amount must be greater than 0'),
  quantity: z.number().min(1, 'Quantity must be at least 1'),
  unit: z.string().min(1, 'Unit is required'),
  vendor: z.string().optional(),
  priority: z.enum(['low', 'medium', 'high']),
  notes: z.string().optional(),
})

type RequestFormData = z.infer<typeof requestSchema>

const RequestForm = () => {
  const navigate = useNavigate()
  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm<RequestFormData>({
    resolver: zodResolver(requestSchema),
    defaultValues: {
      priority: 'medium',
      department: 'purchase',
    }
  })

  const onSubmit = async (data: RequestFormData) => {
    try {
      await api.post('/purchase-requests/', data)
      toast.success('Request created successfully!')
      navigate('/')
    } catch (error) {
      toast.error('Failed to create request. Please try again.')
    }
  }

  return (
    <div className="max-w-3xl mx-auto">
      <div className="card p-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-6">New Purchase Request</h1>
        
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="label-field">Title *</label>
              <input
                {...register('title')}
                className="input-field"
                placeholder="Enter request title"
              />
              {errors.title && (
                <p className="text-red-500 text-sm mt-1">{errors.title.message}</p>
              )}
            </div>
            
            <div>
              <label className="label-field">Department *</label>
              <select {...register('department')} className="input-field">
                <option value="purchase">Purchase</option>
                <option value="account">Account</option>
                <option value="hr">HR</option>
              </select>
            </div>
            
            <div>
              <label className="label-field">Requested By *</label>
              <input
                {...register('requested_by')}
                className="input-field"
                placeholder="Your name"
              />
              {errors.requested_by && (
                <p className="text-red-500 text-sm mt-1">{errors.requested_by.message}</p>
              )}
            </div>
            
            <div>
              <label className="label-field">Amount ($) *</label>
              <input
                type="number"
                step="0.01"
                {...register('amount', { valueAsNumber: true })}
                className="input-field"
                placeholder="0.00"
              />
              {errors.amount && (
                <p className="text-red-500 text-sm mt-1">{errors.amount.message}</p>
              )}
            </div>
            
            <div>
              <label className="label-field">Quantity *</label>
              <input
                type="number"
                {...register('quantity', { valueAsNumber: true })}
                className="input-field"
                placeholder="1"
              />
              {errors.quantity && (
                <p className="text-red-500 text-sm mt-1">{errors.quantity.message}</p>
              )}
            </div>
            
            <div>
              <label className="label-field">Unit *</label>
              <input
                {...register('unit')}
                className="input-field"
                placeholder="e.g., pieces, kg, hours"
              />
              {errors.unit && (
                <p className="text-red-500 text-sm mt-1">{errors.unit.message}</p>
              )}
            </div>
            
            <div>
              <label className="label-field">Vendor</label>
              <input
                {...register('vendor')}
                className="input-field"
                placeholder="Vendor name"
              />
            </div>
            
            <div>
              <label className="label-field">Priority</label>
              <select {...register('priority')} className="input-field">
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
              </select>
            </div>
          </div>
          
          <div>
            <label className="label-field">Description</label>
            <textarea
              {...register('description')}
              className="input-field"
              rows={3}
              placeholder="Detailed description of the request"
            />
          </div>
          
          <div>
            <label className="label-field">Additional Notes</label>
            <textarea
              {...register('notes')}
              className="input-field"
              rows={2}
              placeholder="Any additional information"
            />
          </div>
          
          <div className="flex items-center space-x-4">
            <button
              type="submit"
              disabled={isSubmitting}
              className="btn-primary flex-1"
            >
              {isSubmitting ? 'Creating...' : 'Create Request'}
            </button>
            <button
              type="button"
              onClick={() => navigate('/')}
              className="btn-secondary flex-1"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default RequestForm
