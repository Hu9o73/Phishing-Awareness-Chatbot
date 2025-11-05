<template>
  <div class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4" @click.self="$emit('close')">
    <div class="bg-white rounded-2xl shadow-2xl max-w-2xl w-full p-6 transform transition-all">
      <div class="flex items-center justify-between mb-6">
        <h2 class="text-2xl font-bold text-phisward-primary">
          {{ mode === 'create' ? 'Create Scenario' : 'Edit Scenario' }}
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
            <label for="scenario_name" class="block text-sm font-semibold text-gray-700 mb-2">Scenario Name *</label>
            <input
              id="scenario_name"
              v-model="formData.name"
              type="text"
              required
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-phisward-secondary focus:border-transparent transition-all"
              placeholder="Quarterly Security Awareness"
            />
          </div>

          <div>
            <label for="scenario_complexity" class="block text-sm font-semibold text-gray-700 mb-2">Complexity *</label>
            <select
              id="scenario_complexity"
              v-model="formData.complexity"
              required
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-phisward-secondary focus:border-transparent transition-all uppercase tracking-wide text-sm font-semibold"
            >
              <option value="EASY">Easy</option>
              <option value="MEDIUM">Medium</option>
              <option value="HARD">Hard</option>
            </select>
          </div>
        </div>

        <div>
          <label for="scenario_prompt" class="block text-sm font-semibold text-gray-700 mb-2">System Prompt *</label>
          <textarea
            id="scenario_prompt"
            v-model="formData.system_prompt"
            required
            rows="6"
            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-phisward-secondary focus:border-transparent transition-all"
            placeholder="Describe the phishing scenario that will guide the simulation..."
          />
        </div>

        <div>
          <label for="scenario_misc" class="block text-sm font-semibold text-gray-700 mb-2">Misc Information (JSON)</label>
          <textarea
            id="scenario_misc"
            v-model="formData.miscInfo"
            rows="4"
            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-phisward-secondary focus:border-transparent transition-all font-mono text-sm"
            placeholder='{"industry": "finance", "target_role": "accountant"}'
          />
          <p class="text-xs text-gray-500 mt-1">
            Leave empty if not needed. Provide valid JSON to store additional metadata.
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
              {{ mode === 'create' ? 'Create Scenario' : 'Save Changes' }}
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
  scenario: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['close', 'saved'])

const formData = ref({
  name: '',
  complexity: 'EASY',
  system_prompt: '',
  miscInfo: ''
})

const loading = ref(false)
const error = ref('')

const fillForm = () => {
  if (props.mode === 'edit' && props.scenario) {
    formData.value = {
      name: props.scenario.name || '',
      complexity: props.scenario.complexity || 'EASY',
      system_prompt: props.scenario.system_prompt || '',
      miscInfo: props.scenario.misc_info ? JSON.stringify(props.scenario.misc_info, null, 2) : ''
    }
  } else {
    formData.value = {
      name: '',
      complexity: 'EASY',
      system_prompt: '',
      miscInfo: ''
    }
  }
}

watch(
  () => [props.mode, props.scenario],
  () => {
    fillForm()
  },
  { immediate: true }
)

const handleSubmit = async () => {
  loading.value = true
  error.value = ''

  try {
    let miscPayload = null
    if (formData.value.miscInfo.trim()) {
      try {
        miscPayload = JSON.parse(formData.value.miscInfo)
      } catch (err) {
        throw new Error('Misc information must be valid JSON.')
      }
    }

    const payload = {
      name: formData.value.name,
      complexity: formData.value.complexity,
      system_prompt: formData.value.system_prompt,
      misc_info: miscPayload
    }

    const token = localStorage.getItem('user_jwt_token')
    if (!token) {
      throw new Error('Missing authentication token. Please log in again.')
    }

    let response
    if (props.mode === 'edit' && props.scenario?.id) {
      response = await fetch(`/api/challenges/user/scenarios?scenario_id=${props.scenario.id}`, {
        method: 'PUT',
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
      })
    } else {
      response = await fetch('/api/challenges/user/scenarios', {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
      })
    }

    if (!response.ok) {
      let message = 'Failed to save scenario.'
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

    const successMessage = props.mode === 'edit' ? 'Scenario updated successfully.' : 'Scenario created successfully.'
    emit('saved', successMessage)
  } catch (err) {
    error.value = err.message || 'Failed to save scenario.'
  } finally {
    loading.value = false
  }
}
</script>
