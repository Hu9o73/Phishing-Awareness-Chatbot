<template>
  <div class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4" @click.self="$emit('close')">
    <div class="bg-white rounded-2xl shadow-2xl w-full max-w-xl p-6">
      <div class="flex items-center justify-between mb-6">
        <div>
          <p class="text-sm text-gray-500">Start challenge for</p>
          <h2 class="text-2xl font-bold text-phisward-primary">
            {{ member.first_name }} {{ member.last_name }}
          </h2>
          <p class="text-sm text-gray-600">{{ member.email }}</p>
        </div>
        <button
          @click="$emit('close')"
          class="text-gray-400 hover:text-gray-600 transition-colors"
        >
          <i class="fas fa-times text-xl"></i>
        </button>
      </div>

      <form @submit.prevent="handleStart" class="space-y-4">
        <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg flex items-center gap-2">
          <i class="fas fa-exclamation-circle"></i>
          <span>{{ error }}</span>
        </div>

        <div class="space-y-2">
          <label for="start_challenge_scenario" class="block text-sm font-semibold text-gray-700">
            Scenario
          </label>
          <select
            id="start_challenge_scenario"
            v-model="selectedScenarioId"
            required
            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-phisward-secondary focus:border-transparent transition-all"
          >
            <option
              v-for="scenario in scenarios"
              :key="scenario.id"
              :value="scenario.id"
            >
              {{ scenario.name }} ({{ scenario.complexity }})
            </option>
          </select>
          <p class="text-xs text-gray-500">Only scenarios you have access to are listed.</p>
        </div>

        <div class="flex flex-col-reverse sm:flex-row sm:justify-end gap-3 pt-2">
          <button
            type="button"
            @click="$emit('close')"
            class="px-5 py-3 border border-gray-300 text-gray-700 rounded-lg font-semibold hover:bg-gray-50 transition-all duration-200"
          >
            Cancel
          </button>
          <button
            type="submit"
            :disabled="loading || !selectedScenarioId"
            class="px-5 py-3 bg-gradient-to-r from-phisward-secondary to-phisward-third text-white rounded-lg font-semibold shadow-lg hover:shadow-xl transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="!loading">
              <i class="fas fa-play mr-2"></i>
              Start Challenge
            </span>
            <span v-else>
              <i class="fas fa-spinner fa-spin mr-2"></i>
              Starting...
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
  member: {
    type: Object,
    required: true
  },
  scenarios: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['close', 'started'])

const selectedScenarioId = ref('')
const loading = ref(false)
const error = ref('')

const extractErrorMessage = async (response, fallback) => {
  try {
    const data = await response.json()
    if (typeof data?.detail === 'string') {
      return data.detail
    }
  } catch (err) {
    // ignore parsing issues
  }
  return fallback
}

const setDefaultScenario = () => {
  if (!selectedScenarioId.value && props.scenarios.length > 0) {
    selectedScenarioId.value = props.scenarios[0].id
  }
}

watch(
  () => props.scenarios,
  () => {
    setDefaultScenario()
  },
  { immediate: true, deep: true }
)

const handleStart = async () => {
  if (!selectedScenarioId.value) {
    error.value = 'Select a scenario to start.'
    return
  }

  loading.value = true
  error.value = ''

  try {
    const token = localStorage.getItem('user_jwt_token')
    if (!token) {
      throw new Error('Missing authentication token. Please log in again.')
    }

    const response = await fetch(
      `/api/monitoring/start-challenge?employee_id=${props.member.id}&scenario_id=${selectedScenarioId.value}`,
      {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    )

    if (!response.ok) {
      const message = await extractErrorMessage(response, 'Failed to start challenge.')
      throw new Error(message)
    }

    const challenge = await response.json()
    emit('started', challenge)
    emit('close')
  } catch (err) {
    error.value = err.message || 'Failed to start challenge.'
  } finally {
    loading.value = false
  }
}
</script>
