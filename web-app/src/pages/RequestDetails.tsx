import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { format } from 'date-fns'
import { ArrowLeft, CheckCircle, XCircle } from 'lucide-react'
import api from '../api/axios'
import toast from 'react-hot-toast'

interface RequestDetail {
  id: number
  title: string
  description: string
  department: string
  requested_by: string
  amount: number
  quantity: number
  unit: string
  vendor: string
  priority: string
  status: string
  notes: string
  created_at: string
  approved_by: string
  approved_at: string
  rejection_reason: string
  history: any[]
}

const RequestDetails = () => {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [request, setRequest] = useState<RequestDetail | null>(null)
  const [loading, setLoading] = useState(true)
  const [notes, setNotes] = useState('')
  const [approving, setApproving] = useState(false)

  useEffect(() => {
    fetchRequest()
  }, [id])

  const fetchRequest = async () => {
    try {
      const response = await api.get(`/purchase-requests/${id}`)
      setRequest(response.data)
    } catch (error) {
      toast.error('Failed to load request')
      navigate('/')
    } finally {
      setLoading(false)
    }
  }

  const handleApprove = async () => {
    try {
      setApproving(true)
      await api.post(`/purchase-requests/${id}/approve`, {
        notes: notes,
        approved_by: 'Manager' // In production, get from auth
      })
      toast.success('Request approved!')
      fetchRequest()
      setNotes('')
    } catch (error) {
      toast.error('Failed to approve request')
    } finally {
      setApproving(false)
    }
  }

  const handleReject = async () => {
    const reason = prompt('Please provide a reason for rejection:')
    if (!reason) return
    
    try {
      setApproving(true)
      await api.post(`/purchase-requests/${id}/reject`, {
        reason: reason,
        rejected_by: 'Manager'
      })
      toast.success('Request rejected')
      fetchRequest()
    } catch (error) {
      toast.error('Failed to reject request')
    } finally {
      setApproving(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  if (!request) return null

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <button
        onClick={() => navigate('/')}
        className="flex items-center space-x-2 text-gray-600 hover:text-gray-900 transition-colors duration-200"
      >
        <ArrowLeft className="w-5 h-5" />
        <span>Back to Dashboard</span>
      </button>

      <div className="card p-6">
        <div className="flex justify-between items-start">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">{request.title}</h1>
            <p className="text-gray-500 mt-1">Request #{request.id}</p>
          </div>
          <span className={`px-3 py-1 rounded-full text-sm font-medium ${
            request.status === 'approved' ? 'bg-green-100 text-green-800' :
            request.status === 'rejected' ? 'bg-red-100 text-red-800' :
            'bg-yellow-100 text-yellow-800'
          }`}>
            {request.status}
          </span>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-3 gap-6 mt-6">
          <div>
            <p className="text-sm text-gray-500">Department</p>
            <p className="font-medium capitalize">{request.department}</p>
          </div>
          <div>
            <p className="text-sm text-gray-500">Requested By</p>
            <p className="font-medium">{request.requested_by}</p>
          </div>
          <div>
            <p className="text-sm text-gray-500">Amount</p>
            <p className="font-medium">${request.amount.toFixed(2)}</p>
          </div>
          <div>
            <p className="text-sm text-gray-500">Quantity</p>
            <p className="font-medium">{request.quantity} {request.unit}</p>
          </div>
          <div>
            <p className="text-sm text-gray-500">Priority</p>
            <p className="font-medium capitalize">{request.priority}</p>
          </div>
          <div>
            <p className="text-sm text-gray-500">Date</p>
            <p className="font-medium">{format(new Date(request.created_at), 'MMM d, yyyy')}</p>
          </div>
        </div>

        {request.vendor && (
          <div className="mt-4">
            <p className="text-sm text-gray-500">Vendor</p>
            <p className="font-medium">{request.vendor}</p>
          </div>
        )}

        {request.description && (
          <div className="mt-4">
            <p className="text-sm text-gray-500">Description</p>
            <p className="mt-1">{request.description}</p>
          </div>
        )}

        {request.notes && (
          <div className="mt-4">
            <p className="text-sm text-gray-500">Notes</p>
            <p className="mt-1">{request.notes}</p>
          </div>
        )}

        {request.rejection_reason && (
          <div className="mt-4 p-4 bg-red-50 rounded-md">
            <p className="text-sm font-medium text-red-800">Rejection Reason</p>
            <p className="mt-1 text-red-700">{request.rejection_reason}</p>
          </div>
        )}

        {request.status === 'pending' && (
          <div className="mt-6 border-t pt-6">
            <div className="space-y-4">
              <div>
                <label className="label-field">Notes (Optional)</label>
                <textarea
                  value={notes}
                  onChange={(e) => setNotes(e.target.value)}
                  className="input-field"
                  rows={2}
                  placeholder="Add notes for the approval"
                />
              </div>
              <div className="flex space-x-4">
                <button
                  onClick={handleApprove}
                  disabled={approving}
                  className="btn-primary flex items-center space-x-2 flex-1"
                >
                  <CheckCircle className="w-5 h-5" />
                  <span>Approve</span>
                </button>
                <button
                  onClick={handleReject}
                  disabled={approving}
                  className="btn-secondary flex items-center space-x-2 flex-1"
                >
                  <XCircle className="w-5 h-5" />
                  <span>Reject</span>
                </button>
              </div>
            </div>
          </div>
        )}

        {request.approved_by && (
          <div className="mt-4 p-4 bg-green-50 rounded-md">
            <p className="text-sm text-green-800">
              Approved by {request.approved_by} on {format(new Date(request.approved_at), 'MMM d, yyyy HH:mm')}
            </p>
          </div>
        )}
      </div>

      {/* History */}
      <div className="card p-6">
        <h2 className="text-xl font-semibold mb-4">History</h2>
        <div className="space-y-4">
          {request.history.map((entry) => (
            <div key={entry.id} className="flex items-start space-x-3">
              <div className="flex-shrink-0 w-2 h-2 mt-2 rounded-full bg-primary-500"></div>
              <div>
                <p className="font-medium">{entry.action}</p>
                <p className="text-sm text-gray-500">
                  by {entry.performed_by} • {format(new Date(entry.created_at), 'MMM d, yyyy HH:mm')}
                </p>
                {entry.notes && (
                  <p className="text-sm text-gray-600 mt-1">{entry.notes}</p>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default RequestDetails
