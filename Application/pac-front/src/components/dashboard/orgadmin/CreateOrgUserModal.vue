<template>
  <div class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4" @click.self="$emit('close')">
    <div class="bg-white rounded-2xl shadow-2xl max-w-md w-full p-6 transform transition-all">
      <div class="flex items-center justify-between mb-6">
        <h2 class="text-2xl font-bold text-phisward-primary">Create User Account</h2>
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

        <div>
          <label for="user_first_name" class="block text-sm font-semibold text-gray-700 mb-2">First Name *</label>
          <input
            id="user_first_name"
            v-model="formData.first_name"
            type="text"
            required
            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-phisward-secondary focus:border-transparent transition-all"
            placeholder="Jane"
          />
        </div>

        <div>
          <label for="user_last_name" class="block text-sm font-semibold text-gray-700 mb-2">Last Name *</label>
          <input
            id="user_last_name"
            v-model="formData.last_name"
            type="text"
            required
            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-phisward-secondary focus:border-transparent transition-all"
            placeholder="Doe"
          />
        </div>

        <div>
          <label for="user_email" class="block text-sm font-semibold text-gray-700 mb-2">Email *</label>
          <input
            id="user_email"
            v-model="formData.email"
            type="email"
            required
            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-phisward-secondary focus:border-transparent transition-all"
            placeholder="jane.doe@company.com"
          />
        </div>

        <div>
          <label for="user_password" class="block text-sm font-semibold text-gray-700 mb-2">Password *</label>
          <input
            id="user_password"
            v-model="formData.password"
            type="password"
            required
            minlength="8"
            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-phisward-secondary focus:border-transparent transition-all"
            placeholder="At least 8 characters"
          />
        </div>

        <div>
          <label for="user_confirm_password" class="block text-sm font-semibold text-gray-700 mb-2">Confirm Password *</label>
          <input
            id="user_confirm_password"
            v-model="formData.confirmPassword"
            type="password"
            required
            minlength="8"
            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-phisward-secondary focus:border-transparent transition-all"
            placeholder="Repeat the password"
          />
        </div>

        <div class="flex gap-3 pt-4">
          <button
            type="button"
            @click="$emit('close')"
            class="flex-1 px-6 py-3 border-2 border-gray-300 text-gray-700 rounded-lg font-semibold hover:bg-gray-50 transition-all duration-200"
          >
            Cancel
          </button>
          <button
            type="submit"
            :disabled="loading"
            class="flex-1 px-6 py-3 bg-gradient-to-r from-phisward-secondary to-phisward-third text-white rounded-lg font-semibold shadow-lg hover:shadow-xl transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="!loading">
              <i class="fas fa-user-plus mr-2"></i>
              Create Account
            </span>
            <span v-else>
              <i class="fas fa-spinner fa-spin mr-2"></i>
              Creating...
            </span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const emit = defineEmits(['close', 'created'])

const formData = ref({
  first_name: '',
  last_name: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const loading = ref(false)
const error = ref('')

const resetForm = () => {
  formData.value = {
    first_name: '',
    last_name: '',
    email: '',
    password: '',
    confirmPassword: ''
  }
}

const handleSubmit = async () => {
  loading.value = true
  error.value = ''

  try {
    if (formData.value.password !== formData.value.confirmPassword) {
      throw new Error('Passwords do not match.')
    }

    const token = localStorage.getItem('user_jwt_token')
    if (!token) {
      throw new Error('Missing authentication token. Please log in again.')
    }

    const params = new URLSearchParams({
      email: formData.value.email,
      password: formData.value.password,
      first_name: formData.value.first_name,
      last_name: formData.value.last_name,
      recaptcha_token: 'dev_token'
    })

    const response = await fetch(`/api/authentication/orgadmin/user?${params.toString()}`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`
      }
    })

    if (!response.ok) {
      let message = 'Failed to create user account.'
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
        // ignore JSON parsing errors
      }
      throw new Error(message)
    }

    resetForm()
    emit('created')
  } catch (err) {
    error.value = err.message || 'Failed to create user account.'
  } finally {
    loading.value = false
  }
}
</script>
