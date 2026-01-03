<template>
  <div class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4" @click.self="$emit('close')">
    <div class="bg-white rounded-2xl shadow-2xl w-full max-w-4xl p-6">
      <div class="flex items-start justify-between mb-6">
        <div>
          <p class="text-sm text-gray-500">Challenge workflow</p>
          <h2 class="text-2xl font-bold text-phisward-primary">Workflow Dashboard</h2>
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

      <div v-if="loading" class="flex items-center justify-center py-16">
        <i class="fas fa-spinner fa-spin text-3xl text-phisward-secondary"></i>
      </div>

      <div v-else>
        <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg flex items-center gap-2 mb-4">
          <i class="fas fa-exclamation-circle"></i>
          <span>{{ error }}</span>
        </div>

        <div class="rounded-2xl border border-phisward-fourth/60 bg-phisward-fourth/20 p-6 mb-6">
          <div class="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
            <div class="flex items-center gap-4">
              <div
                class="w-14 h-14 rounded-2xl flex items-center justify-center text-xl"
                :class="statusMeta.badgeClass"
              >
                <i :class="statusMeta.icon"></i>
              </div>
              <div>
                <p class="text-xs uppercase tracking-wide text-gray-500">Current Status</p>
                <h3 class="text-3xl font-bold" :class="statusMeta.textClass">{{ statusMeta.label }}</h3>
                <p class="text-sm text-gray-600">Step: {{ stepLabel }}</p>
              </div>
            </div>
            <div v-if="showScore" class="flex items-center gap-3 bg-white/70 border border-white rounded-2xl px-5 py-3">
              <div class="w-10 h-10 rounded-full bg-phisward-secondary/10 text-phisward-secondary flex items-center justify-center">
                <i class="fas fa-trophy"></i>
              </div>
              <div>
                <p class="text-xs uppercase tracking-wide text-gray-500">Score</p>
                <p class="text-2xl font-bold text-gray-900">{{ displayScore }}</p>
              </div>
            </div>
          </div>
        </div>

        <div class="mb-8">
          <p class="text-sm font-semibold text-gray-700 uppercase tracking-wide mb-4">Workflow Progress</p>
          <div class="flex items-center">
            <div
              v-for="(step, index) in steps"
              :key="step.key"
              class="flex-1 flex items-center"
            >
              <div class="flex flex-col items-center text-center">
                <div
                  class="w-12 h-12 rounded-full flex items-center justify-center text-base font-semibold transition-all duration-300"
                  :class="stepCircleClass(index)"
                >
                  <i :class="step.icon"></i>
                </div>
                <p class="mt-3 text-xs font-semibold uppercase tracking-wide" :class="stepLabelClass(index)">
                  {{ step.label }}
                </p>
              </div>
              <div
                v-if="index < steps.length - 1"
                class="flex-1 h-1 mx-2 rounded-full transition-all duration-300"
                :class="stepLineClass(index)"
              ></div>
            </div>
          </div>
        </div>

        <div>
          <div class="flex items-center justify-between mb-3">
            <p class="text-sm font-semibold text-gray-700 uppercase tracking-wide">Conversation Feed</p>
            <span class="text-xs text-gray-500">{{ exchanges.length }} messages</span>
          </div>
          <div v-if="exchanges.length === 0" class="bg-gray-50 border border-gray-100 rounded-xl p-6 text-center text-gray-500">
            No exchanges yet.
          </div>
          <div v-else class="space-y-4 max-h-80 overflow-y-auto pr-2">
            <article
              v-for="exchange in exchanges"
              :key="exchange.id"
              class="bg-white border border-gray-100 rounded-2xl p-4 shadow-sm"
            >
              <div class="flex flex-wrap items-center justify-between gap-2 text-xs text-gray-500">
                <span class="inline-flex items-center gap-2 px-2 py-1 rounded-full" :class="roleBadgeClass(exchange.role)">
                  <i :class="roleIcon(exchange.role)"></i>
                  {{ formatRole(exchange.role) }}
                </span>
                <span v-if="exchange.sender_email">{{ exchange.sender_email }}</span>
                <span v-if="exchange.created_at">{{ formatDate(exchange.created_at) }}</span>
              </div>
              <h4 v-if="exchange.subject" class="mt-3 text-sm font-semibold text-gray-800">
                {{ exchange.subject }}
              </h4>
              <p class="mt-2 text-sm text-gray-700 whitespace-pre-wrap">
                {{ exchange.body || 'No content provided.' }}
              </p>
            </article>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'

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

const emit = defineEmits(['close'])

const loading = ref(false)
const error = ref('')
const workflowData = ref(null)

const steps = [
  { key: 'AI_EMAIL_SENT', label: 'AI Email Sent', icon: 'fas fa-paper-plane' },
  { key: 'USER_ANSWERED', label: 'User Answered', icon: 'fas fa-user-check' },
  { key: 'AI_ANSWER_READY', label: 'AI Answer Ready', icon: 'fas fa-robot' }
]

const exchanges = computed(() => workflowData.value?.exchanges ?? [])

const workflowState = computed(() => workflowData.value?.workflow_state || props.challenge?.status || 'ONGOING')
const workflowStep = computed(() => workflowData.value?.workflow_step || steps[0].key)

const statusMeta = computed(() => {
  if (workflowState.value === 'SUCCESS') {
    return {
      label: 'Success',
      badgeClass: 'bg-green-100 text-green-700',
      textClass: 'text-green-700',
      icon: 'fas fa-check-circle'
    }
  }
  if (workflowState.value === 'FAILURE') {
    return {
      label: 'Failure',
      badgeClass: 'bg-red-100 text-red-700',
      textClass: 'text-red-700',
      icon: 'fas fa-times-circle'
    }
  }
  return {
    label: 'Ongoing',
    badgeClass: 'bg-phisward-fourth text-phisward-primary',
    textClass: 'text-phisward-primary',
    icon: 'fas fa-spinner'
  }
})

const showScore = computed(() => workflowState.value === 'SUCCESS' || workflowState.value === 'FAILURE')
const displayScore = computed(() => {
  const score = workflowData.value?.score
  if (score === null || score === undefined) {
    return 'N/A'
  }
  const numericScore = Number(score)
  if (Number.isNaN(numericScore)) {
    return 'N/A'
  }
  return numericScore
})

const stepLabel = computed(() => {
  const match = steps.find((step) => step.key === workflowStep.value)
  return match ? match.label : steps[0].label
})

const currentStepIndex = computed(() => {
  const index = steps.findIndex((step) => step.key === workflowStep.value)
  return index === -1 ? 0 : index
})

const stepCircleClass = (index) => {
  if (index < currentStepIndex.value) {
    return 'bg-phisward-secondary text-white shadow'
  }
  if (index === currentStepIndex.value) {
    return 'bg-phisward-primary text-white shadow-lg'
  }
  return 'bg-gray-100 text-gray-400'
}

const stepLineClass = (index) => {
  if (index < currentStepIndex.value) {
    return 'bg-phisward-secondary'
  }
  if (index === currentStepIndex.value) {
    return 'bg-phisward-secondary/60'
  }
  return 'bg-gray-200'
}

const stepLabelClass = (index) => {
  if (index <= currentStepIndex.value) {
    return 'text-phisward-primary'
  }
  return 'text-gray-400'
}

const roleBadgeClass = (role) => {
  if (role === 'USER') {
    return 'bg-blue-100 text-blue-700'
  }
  if (role === 'AI') {
    return 'bg-phisward-fourth text-phisward-primary'
  }
  if (role === 'HOOK') {
    return 'bg-amber-100 text-amber-700'
  }
  return 'bg-gray-100 text-gray-700'
}

const roleIcon = (role) => {
  if (role === 'USER') {
    return 'fas fa-user'
  }
  if (role === 'AI') {
    return 'fas fa-robot'
  }
  if (role === 'HOOK') {
    return 'fas fa-paper-plane'
  }
  return 'fas fa-envelope'
}

const formatRole = (role) => {
  if (!role) {
    return 'Unknown'
  }
  return role.charAt(0) + role.slice(1).toLowerCase()
}

const formatDate = (value) => {
  try {
    const date = new Date(value)
    return date.toLocaleString()
  } catch (err) {
    return value
  }
}

const extractErrorMessage = async (response, fallback) => {
  try {
    const data = await response.json()
    if (typeof data?.detail === 'string') {
      return data.detail
    }
    if (Array.isArray(data?.detail)) {
      return data.detail.join(', ')
    }
  } catch (err) {
    // ignore parsing errors
  }
  return fallback
}

const loadWorkflow = async () => {
  if (!props.challenge?.id) {
    return
  }
  loading.value = true
  error.value = ''

  try {
    const token = localStorage.getItem('user_jwt_token')
    if (!token) {
      throw new Error('Missing authentication token. Please log in again.')
    }
    const response = await fetch(`/api/monitoring/challenges/${props.challenge.id}`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    if (!response.ok) {
      const message = await extractErrorMessage(response, 'Failed to load workflow data.')
      throw new Error(message)
    }
    workflowData.value = await response.json()
  } catch (err) {
    error.value = err.message || 'Failed to load workflow data.'
  } finally {
    loading.value = false
  }
}

onMounted(loadWorkflow)
watch(
  () => props.challenge?.id,
  () => {
    loadWorkflow()
  }
)
</script>
