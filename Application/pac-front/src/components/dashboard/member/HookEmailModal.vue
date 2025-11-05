<template>
  <div class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4" @click.self="$emit('close')">
    <div class="bg-white rounded-2xl shadow-2xl max-w-2xl w-full p-6 transform transition-all">
      <div class="flex items-center justify-between mb-6">
        <h2 class="text-2xl font-bold text-phisward-primary">
          {{ mode === 'create' ? 'Create Hook Email' : 'Edit Hook Email' }}
        </h2>
        <button
          @click="$emit('close')"
          class="text-gray-400 hover:text-gray-600 transition-colors"
        >
          <i class="fas fa-times text-xl"></i>
        </button>
      </div>

      <form @submit.prevent="handleSubmit" class="space-y-4">
        <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg flex items-center gap-2">
          <i class="fas fa-exclamation-circle"></i>
          <span>{{ error }}</span>
        </div>

        <div class="grid gap-4 md:grid-cols-2">
          <div>
            <label for="hook_email_sender" class="block text-sm font-semibold text-gray-700 mb-2">Sender Email *</label>
            <input
              id="hook_email_sender"
              v-model="formData.sender_email"
              type="email"
              required
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-phisward-secondary focus:border-transparent transition-all"
              placeholder="security@company.com"
            />
          </div>

          <div>
            <label for="hook_email_language" class="block text-sm font-semibold text-gray-700 mb-2">Language *</label>
            <input
              id="hook_email_language"
              v-model="formData.language"
              type="text"
              required
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-phisward-secondary focus:border-transparent transition-all uppercase"
              placeholder="en"
            />
          </div>
        </div>

        <div>
          <label for="hook_email_subject" class="block text-sm font-semibold text-gray-700 mb-2">Subject</label>
          <input
            id="hook_email_subject"
            v-model="formData.subject"
            type="text"
            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-phisward-secondary focus:border-transparent transition-all"
            placeholder="Important: Password Reset Required"
          />
        </div>

        <div>
          <label for="hook_email_body" class="block text-sm font-semibold text-gray-700 mb-2">Email Body *</label>
          <textarea
            id="hook_email_body"
            v-model="formData.body"
            rows="6"
            required
            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-phisward-secondary focus:border-transparent transition-all"
            placeholder="Write the content of the hook email..."
          />
        </div>

        <div>
          <label for="hook_email_variables" class="block text-sm font-semibold text-gray-700 mb-2">Variables (JSON)</label>
          <textarea
            id="hook_email_variables"
            v-model="formData.variables"
            rows="4"
            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-phisward-secondary focus:border-transparent transition-all font-mono text-sm"
            placeholder='{"employee_name": "{{employee_name}}"}'
          />
          <p class="text-xs text-gray-500 mt-1">
            Optional key/value pairs (must be valid JSON). Leave blank if not needed.
          </p>
        </div>

        <div class="flex flex-col-reverse md:flex-row md:justify-end md:gap-3 pt-4 gap-3">
          <button
            type="button"
            @click="$emit('close')"
            class="px-6 py-3 border-2 border-gray-300 text-gray-700 rounded-lg font-semibold hover:bg-gray-50 transition-all duration-200"
          >
            Cancel
          </button>
          <button
            type="submit"
            :disabled="loading"
            class="px-6 py-3 bg-gradient-to-r from-phisward-secondary to-phisward-third text-white rounded-lg font-semibold shadow-lg hover:shadow-xl transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="!loading">
              <i :class="mode === 'create' ? 'fas fa-plus mr-2' : 'fas fa-save mr-2'"></i>
              {{ mode === 'create' ? 'Create Hook Email' : 'Save Changes' }}
            </span>
            <span v-else>
              <i class="fas fa-spinner fa-spin mr-2"></i>
              Saving...
            </span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  mode: {
    type: String,
    default: 'create'
  },
  scenarioId: {
    type: String,
    required: true
  },
  initialEmail: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['close', 'saved'])

const formData = ref({
  subject: '',
  sender_email: '',
  language: 'en',
  body: '',
  variables: ''
})

const loading = ref(false)
const error = ref('')

const populateForm = () => {
  if (props.initialEmail) {
    formData.value = {
      subject: props.initialEmail.subject || '',
      sender_email: props.initialEmail.sender_email || '',
      language: props.initialEmail.language || 'en',
      body: props.initialEmail.body || '',
      variables: props.initialEmail.variables ? JSON.stringify(props.initialEmail.variables, null, 2) : ''
    }
  } else {
    formData.value = {
      subject: '',
      sender_email: '',
      language: 'en',
      body: '',
      variables: ''
    }
  }
}

watch(
  () => [props.mode, props.initialEmail],
  () => {
    populateForm()
  },
  { immediate: true }
)

const handleSubmit = async () => {
  loading.value = true
  error.value = ''

  try {
    let variablesPayload = undefined
    if (formData.value.variables.trim()) {
      try {
        variablesPayload = JSON.parse(formData.value.variables)
      } catch (err) {
        throw new Error('Variables must be valid JSON.')
      }
    }

    const payload = {
      subject: formData.value.subject || undefined,
      sender_email: formData.value.sender_email,
      language: formData.value.language,
      body: formData.value.body || undefined,
      variables: variablesPayload
    }

    const token = localStorage.getItem('user_jwt_token')
    if (!token) {
      throw new Error('Missing authentication token. Please log in again.')
    }

    let response
    if (props.mode === 'edit') {
      response = await fetch(`/api/challenges/user/scenarios/hook-email?scenario_id=${props.scenarioId}`, {
        method: 'PUT',
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
      })
    } else {
      response = await fetch(`/api/challenges/user/scenarios/hook-email?scenario_id=${props.scenarioId}`, {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
      })
    }

    if (!response.ok) {
      let message = 'Failed to save hook email.'
      try {
        const data = await response.json()
        if (typeof data?.detail === 'string') {
          message = data.detail
        } else if (Array.isArray(data?.detail)) {
          message = data.detail.join(', ')
        } else if (typeof data?.message === 'string') {
          message = data.message
        }
      } catch (err) {
        // ignore json parsing errors
      }
      throw new Error(message)
    }

    const successMessage = props.mode === 'edit' ? 'Hook email updated successfully.' : 'Hook email created successfully.'
    emit('saved', successMessage)
  } catch (err) {
    error.value = err.message || 'Failed to save hook email.'
  } finally {
    loading.value = false
  }
}
</script>
