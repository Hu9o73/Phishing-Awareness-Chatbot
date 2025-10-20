<template>
  <div class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4" @click.self="$emit('close')">
    <div class="bg-white rounded-2xl shadow-2xl max-w-md w-full p-6 transform transition-all">
      <div class="flex items-center justify-between mb-6">
        <h2 class="text-2xl font-bold text-phisward-primary">Create Company</h2>
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
          <label for="name" class="block text-sm font-semibold text-gray-700 mb-2">Company Name *</label>
          <input
            id="name"
            v-model="formData.name"
            type="text"
            required
            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-phisward-secondary focus:border-transparent transition-all"
            placeholder="Acme Corporation"
          />
        </div>

        <div>
          <label for="description" class="block text-sm font-semibold text-gray-700 mb-2">Description (Optional)</label>
          <textarea
            id="description"
            v-model="formData.description"
            rows="3"
            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-phisward-secondary focus:border-transparent transition-all resize-none"
            placeholder="Brief description of the company..."
          ></textarea>
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
              <i class="fas fa-plus mr-2"></i>
              Create Company
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
  name: '',
  description: ''
})

const loading = ref(false)
const error = ref('')

const handleSubmit = async () => {
  loading.value = true
  error.value = ''

  try {
    const token = localStorage.getItem('user_jwt_token')
    const params = new URLSearchParams({
      organization_name: formData.value.name
    })
    
    if (formData.value.description) {
      params.append('organization_description', formData.value.description)
    }

    const response = await fetch(`/api/authentication/admin/organization?${params}`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })

    if (!response.ok) {
      const data = await response.json()
      throw new Error(data.detail || 'Failed to create company')
    }

    emit('created')
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}
</script>
