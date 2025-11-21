<template>
  <div class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4" @click.self="$emit('close')">
    <div class="bg-white rounded-2xl shadow-2xl w-full max-w-xl p-6">
      <div class="flex items-center justify-between mb-6">
        <div>
          <p class="text-sm text-gray-500">Update challenge</p>
          <h2 class="text-2xl font-bold text-phisward-primary">Status &amp; Score</h2>
          <p class="text-sm text-gray-600">
            {{ scenarioName }} · {{ employeeName }}
          </p>
        </div>
        <button
          @click="$emit('close')"
          class="text-gray-400 hover:text-gray-600 transition-colors"
        >
          <i class="fas fa-times text-xl"></i>
        </button>
      </div>

      <form @submit.prevent="handleUpdate" class="space-y-4">
        <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg flex items-center gap-2">
          <i class="fas fa-exclamation-circle"></i>
          <span>{{ error }}</span>
        </div>

        <div class="grid gap-4 md:grid-cols-2">
          <div>
            <label for="challenge_status" class="block text-sm font-semibold text-gray-700 mb-2">
              Status
            </label>
            <select
              id="challenge_status"
              v-model="selectedStatus"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-phisward-secondary focus:border-transparent transition-all uppercase tracking-wide text-sm font-semibold"
            >
              <option value="SUCCESS">Success</option>
              <option value="FAILURE">Failure</option>
            </select>
          </div>
          <div>
            <label for="challenge_score" class="block text-sm font-semibold text-gray-700 mb-2">
              Score (optional)
            </label>
            <input
              id="challenge_score"
              v-model="scoreInput"
              type="number"
              step="1"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-phisward-secondary focus:border-transparent transition-all"
              placeholder="0"
            />
            <p class="text-xs text-gray-500 mt-1">Leave empty to default to 0.</p>
          </div>
        </div>

        <div class="flex flex-col-reverse md:flex-row md:justify-end gap-3 pt-2">
          <button
            type="button"
            @click="$emit('close')"
            class="px-5 py-3 border border-gray-300 text-gray-700 rounded-lg font-semibold hover:bg-gray-50 transition-all duration-200"
          >
            Cancel
          </button>
          <button
            type="submit"
            :disabled="loading"
            class="px-5 py-3 bg-phisward-primary text-white rounded-lg font-semibold shadow-lg hover:bg-phisward-primary/90 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="!loading">
              <i class="fas fa-save mr-2"></i>
              Update Challenge
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
  challenge: {
    type: Object,
    required: true
  },
  employeeName: {
    type: String,
    default: ''
  },
  scenarioName: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['close', 'updated'])

const selectedStatus = ref('SUCCESS')
const scoreInput = ref('')
const loading = ref(false)
const error = ref('')

const extractErrorMessage = async (response, fallback) => {
  try {
    const data = await response.json()
    if (typeof data?.detail === 'string') {
      return data.detail
    }
  } catch (err) {
    // ignore parsing details
  }
  return fallback
}

const syncForm = () => {
  if (props.challenge?.status === 'FAILURE') {
    selectedStatus.value = 'FAILURE'
  } else {
    selectedStatus.value = 'SUCCESS'
  }
  scoreInput.value = props.challenge?.score ?? ''
}

watch(
  () => props.challenge,
  () => {
    syncForm()
  },
  { immediate: true, deep: true }
)

const handleUpdate = async () => {
  loading.value = true
  error.value = ''

  let payload = { status: selectedStatus.value }
  if (scoreInput.value !== '' && scoreInput.value !== null && scoreInput.value !== undefined) {
    const parsed = Number.parseInt(scoreInput.value, 10)
    if (Number.isNaN(parsed)) {
      error.value = 'Score must be a number.'
      loading.value = false
      return
    }
    payload = { ...payload, score: parsed }
  }

  try {
    const token = localStorage.getItem('user_jwt_token')
    if (!token) {
      throw new Error('Missing authentication token. Please log in again.')
    }

    const response = await fetch(`/api/monitoring/challenges/status?challenge_id=${props.challenge.id}`, {
      method: 'PUT',
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    })

    if (!response.ok) {
      const message = await extractErrorMessage(response, 'Failed to update challenge.')
      throw new Error(message)
    }

    const updated = await response.json()
    emit('updated', updated, 'Challenge updated successfully.')
    emit('close')
  } catch (err) {
    error.value = err.message || 'Failed to update challenge.'
  } finally {
    loading.value = false
  }
}
</script>
