<template>
  <DashboardLayout :role="role">
    <div class="space-y-8">
      <section v-if="activeTab === 'scenarios'" class="space-y-6">
        <header class="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
          <div>
            <h1 class="text-3xl font-bold text-phisward-primary">Training Scenarios</h1>
            <p class="text-gray-600">
              Build and curate the phishing simulations available to your organization.
            </p>
          </div>
          <button
            @click="openCreateScenarioModal"
            class="self-start lg:self-auto px-6 py-3 bg-gradient-to-r from-phisward-secondary to-phisward-third text-white rounded-lg font-semibold shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 transition-all duration-300"
          >
            <i class="fas fa-plus mr-2"></i>
            New Scenario
          </button>
        </header>

        <div v-if="scenariosError" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg flex items-center gap-2">
          <i class="fas fa-exclamation-triangle"></i>
          <span>{{ scenariosError }}</span>
        </div>

        <div v-if="scenariosSuccess" class="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg flex items-center gap-2">
          <i class="fas fa-check-circle"></i>
          <span>{{ scenariosSuccess }}</span>
        </div>

        <div
          v-if="scenariosLoading"
          class="flex items-center justify-center py-16 bg-white rounded-2xl shadow"
        >
          <i class="fas fa-spinner fa-spin text-3xl text-phisward-secondary"></i>
        </div>

        <div
          v-else-if="scenarios.length === 0"
          class="flex flex-col items-center justify-center py-16 bg-white rounded-2xl shadow text-center space-y-4"
        >
          <div class="w-16 h-16 rounded-full bg-phisward-fourth/50 flex items-center justify-center">
            <i class="fas fa-tasks text-2xl text-phisward-secondary"></i>
          </div>
          <div>
            <h2 class="text-xl font-semibold text-phisward-primary">No scenarios yet</h2>
            <p class="text-gray-600">Create your first scenario to begin training your organization.</p>
          </div>
        </div>

        <div v-else class="grid gap-6">
          <article
            v-for="scenario in scenarios"
            :key="scenario.id"
            class="bg-white rounded-2xl shadow p-6 border-2 transition-all duration-200"
            :class="scenario.id === selectedScenarioId ? 'border-phisward-secondary' : 'border-transparent hover:border-phisward-secondary/60'"
          >
            <div class="flex flex-col gap-4 lg:flex-row lg:justify-between lg:items-start">
              <div class="space-y-2">
                <div class="flex flex-wrap items-center gap-3">
                  <h2 class="text-2xl font-semibold text-phisward-primary">{{ scenario.name }}</h2>
                  <span class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-phisward-fourth text-phisward-primary text-sm font-semibold uppercase tracking-wide">
                    <i class="fas fa-signal"></i>
                    {{ scenario.complexity }}
                  </span>
                </div>
                <p class="text-sm text-gray-500">
                  Updated {{ formatDate(scenario.updated_at || scenario.created_at) }}
                </p>
                <div class="bg-gray-50 border border-gray-100 rounded-lg p-4">
                  <h3 class="text-sm font-semibold text-gray-700 uppercase tracking-wide mb-2">System Prompt</h3>
                  <p class="text-gray-700 whitespace-pre-wrap leading-relaxed">{{ scenario.system_prompt }}</p>
                </div>
                <div v-if="scenario.misc_info" class="bg-gray-50 border border-gray-100 rounded-lg p-4">
                  <h3 class="text-sm font-semibold text-gray-700 uppercase tracking-wide mb-2">Misc Info</h3>
                  <pre class="text-xs text-gray-700 overflow-x-auto">{{ prettyJson(scenario.misc_info) }}</pre>
                </div>
              </div>

              <div class="flex flex-col gap-2 w-full lg:w-auto">
                <button
                  @click="selectScenario(scenario.id)"
                  class="w-full lg:w-48 px-4 py-2 border-2 border-phisward-secondary text-phisward-secondary font-semibold rounded-lg hover:bg-phisward-secondary/10 transition-all duration-200"
                >
                  <i class="fas fa-thumbtack mr-2"></i>
                  {{ scenario.id === selectedScenarioId ? 'Selected' : 'Select Scenario' }}
                </button>
                <button
                  @click="openEditScenarioModal(scenario)"
                  class="w-full lg:w-48 px-4 py-2 bg-phisward-primary text-white font-semibold rounded-lg hover:bg-phisward-primary/90 transition-all duration-200"
                >
                  <i class="fas fa-edit mr-2"></i>
                  Edit
                </button>
                <button
                  @click="goToHookEmail(scenario.id)"
                  class="w-full lg:w-48 px-4 py-2 bg-gradient-to-r from-phisward-secondary to-phisward-third text-white font-semibold rounded-lg hover:shadow-lg transition-all duration-200"
                >
                  <i class="fas fa-envelope-open-text mr-2"></i>
                  Hook Email
                </button>
                <button
                  @click="deleteScenario(scenario.id)"
                  class="w-full lg:w-48 px-4 py-2 border-2 border-red-200 text-red-600 font-semibold rounded-lg hover:bg-red-50 transition-all duration-200 disabled:opacity-50"
                  :disabled="deletingScenarioId === scenario.id"
                >
                  <span v-if="deletingScenarioId !== scenario.id">
                    <i class="fas fa-trash mr-2"></i>
                    Delete
                  </span>
                  <span v-else>
                    <i class="fas fa-spinner fa-spin mr-2"></i>
                    Deleting...
                  </span>
                </button>
              </div>
            </div>
          </article>
        </div>
      </section>

      <section v-else-if="activeTab === 'hook-email'" class="space-y-6">
        <header class="flex flex-col gap-3">
          <h1 class="text-3xl font-bold text-phisward-primary">Hook Emails</h1>
          <p class="text-gray-600">
            Craft the initial email that will be sent for a selected scenario.
          </p>
        </header>

        <div v-if="scenarios.length === 0" class="bg-white rounded-2xl shadow p-10 text-center space-y-4">
          <div class="w-16 h-16 rounded-full bg-phisward-fourth/60 flex items-center justify-center mx-auto">
            <i class="fas fa-envelope text-2xl text-phisward-secondary"></i>
          </div>
          <h2 class="text-xl font-semibold text-phisward-primary">No scenarios available</h2>
          <p class="text-gray-600">
            Create a scenario first to configure its hook email.
          </p>
          <button
            @click="openCreateScenarioModal"
            class="px-6 py-3 bg-gradient-to-r from-phisward-secondary to-phisward-third text-white rounded-lg font-semibold shadow-lg hover:shadow-xl transition-all duration-200"
          >
            <i class="fas fa-plus mr-2"></i>
            Create Scenario
          </button>
        </div>

        <div v-else class="space-y-6">
          <div class="bg-white rounded-2xl shadow p-6 space-y-4">
            <div>
              <label for="hook_email_scenario" class="block text-sm font-semibold text-gray-700 mb-2">
                Scenario
              </label>
              <select
                id="hook_email_scenario"
                v-model="selectedScenarioId"
                @change="selectScenario(selectedScenarioId)"
                class="w-full lg:w-96 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-phisward-secondary focus:border-transparent transition-all"
              >
                <option
                  v-for="scenario in scenarios"
                  :key="scenario.id"
                  :value="scenario.id"
                >
                  {{ scenario.name }} ({{ scenario.complexity }})
                </option>
              </select>
            </div>

            <div v-if="hookEmailError" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg flex items-center gap-2">
              <i class="fas fa-exclamation-triangle"></i>
              <span>{{ hookEmailError }}</span>
            </div>

            <div v-if="hookEmailSuccess" class="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg flex items-center gap-2">
              <i class="fas fa-check-circle"></i>
              <span>{{ hookEmailSuccess }}</span>
            </div>

            <div
              v-if="hookEmailLoading"
              class="flex items-center justify-center py-12 text-phisward-secondary"
            >
              <i class="fas fa-spinner fa-spin text-3xl"></i>
            </div>

            <div
              v-else-if="!hookEmail"
              class="flex flex-col items-center justify-center py-12 border border-dashed border-phisward-secondary/40 rounded-xl text-center space-y-4 bg-phisward-fourth/20"
            >
              <i class="fas fa-envelope-open text-3xl text-phisward-secondary"></i>
              <div>
                <h3 class="text-lg font-semibold text-phisward-primary">No hook email yet</h3>
                <p class="text-gray-600">Create your hook email to complete this scenario.</p>
              </div>
              <button
                @click="openCreateHookEmailModal"
                class="px-5 py-3 bg-gradient-to-r from-phisward-secondary to-phisward-third text-white rounded-lg font-semibold shadow-lg hover:shadow-xl transition-all duration-200"
              >
                <i class="fas fa-plus mr-2"></i>
                Create Hook Email
              </button>
            </div>

            <div v-else class="bg-gray-50 border border-gray-200 rounded-2xl p-6 space-y-4">
              <div class="flex flex-wrap gap-4 text-sm text-gray-600">
                <span class="inline-flex items-center gap-2">
                  <i class="fas fa-user"></i>
                  {{ hookEmail.sender_email }}
                </span>
                <span class="inline-flex items-center gap-2">
                  <i class="fas fa-globe"></i>
                  {{ hookEmail.language.toUpperCase() }}
                </span>
              </div>
              <div v-if="hookEmail.subject" class="bg-white border border-gray-200 rounded-lg p-4">
                <h3 class="text-sm font-semibold text-gray-700 uppercase tracking-wide mb-2">Subject</h3>
                <p class="text-gray-800">{{ hookEmail.subject }}</p>
              </div>
              <div class="bg-white border border-gray-200 rounded-lg p-4">
                <h3 class="text-sm font-semibold text-gray-700 uppercase tracking-wide mb-2">Body</h3>
                <p class="text-gray-800 whitespace-pre-wrap leading-relaxed">{{ hookEmail.body }}</p>
              </div>
              <div v-if="hookEmail.variables" class="bg-white border border-gray-200 rounded-lg p-4">
                <h3 class="text-sm font-semibold text-gray-700 uppercase tracking-wide mb-2">Variables</h3>
                <pre class="text-xs text-gray-700 overflow-x-auto">{{ prettyJson(hookEmail.variables) }}</pre>
              </div>
              <div class="flex flex-col sm:flex-row gap-3 pt-2">
                <button
                  @click="openEditHookEmailModal"
                  class="flex-1 px-4 py-2 bg-phisward-primary text-white rounded-lg font-semibold hover:bg-phisward-primary/90 transition-all duration-200"
                >
                  <i class="fas fa-edit mr-2"></i>
                  Edit Hook Email
                </button>
                <button
                  @click="deleteHookEmail"
                  class="flex-1 px-4 py-2 border border-red-200 text-red-600 rounded-lg font-semibold hover:bg-red-50 transition-all duration-200 disabled:opacity-50"
                  :disabled="deletingHookEmail"
                >
                  <span v-if="!deletingHookEmail">
                    <i class="fas fa-trash mr-2"></i>
                    Delete
                  </span>
                  <span v-else>
                    <i class="fas fa-spinner fa-spin mr-2"></i>
                    Deleting...
                  </span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section v-else-if="activeTab === 'import-export'" class="space-y-6">
        <header class="space-y-2">
          <h1 class="text-3xl font-bold text-phisward-primary">Import &amp; Export</h1>
          <p class="text-gray-600">
            Share scenarios with other teams or restore from a backup.
          </p>
        </header>

        <div class="grid gap-6 md:grid-cols-2">
          <div class="bg-white rounded-2xl shadow p-6 space-y-4">
            <h2 class="text-xl font-semibold text-phisward-primary">Export Scenario</h2>
            <p class="text-gray-600 text-sm">
              Download the selected scenario as a JSON file to reuse it later.
            </p>

            <div v-if="exportError" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg flex items-center gap-2">
              <i class="fas fa-exclamation-triangle"></i>
              <span>{{ exportError }}</span>
            </div>

            <div v-if="exportSuccess" class="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg flex items-center gap-2">
              <i class="fas fa-check-circle"></i>
              <span>{{ exportSuccess }}</span>
            </div>

            <div class="space-y-3">
              <label for="export_scenario" class="block text-sm font-semibold text-gray-700">
                Scenario
              </label>
              <select
                id="export_scenario"
                v-model="selectedScenarioId"
                @change="selectScenario(selectedScenarioId)"
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
            </div>

            <button
              @click="exportScenario"
              :disabled="exportingScenario || !selectedScenarioId"
              class="w-full px-6 py-3 bg-gradient-to-r from-phisward-secondary to-phisward-third text-white rounded-lg font-semibold shadow-lg hover:shadow-xl transition-all duration-200 disabled:opacity-50"
            >
              <span v-if="!exportingScenario">
                <i class="fas fa-file-export mr-2"></i>
                Download JSON
              </span>
              <span v-else>
                <i class="fas fa-spinner fa-spin mr-2"></i>
                Preparing...
              </span>
            </button>
          </div>

          <div class="bg-white rounded-2xl shadow p-6 space-y-4">
            <h2 class="text-xl font-semibold text-phisward-primary">Import Scenario</h2>
            <p class="text-gray-600 text-sm">
              Upload a scenario JSON file previously exported from the platform.
            </p>

            <div v-if="importError" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg flex items-center gap-2">
              <i class="fas fa-exclamation-triangle"></i>
              <span>{{ importError }}</span>
            </div>

            <div v-if="importSuccess" class="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg flex items-center gap-2">
              <i class="fas fa-check-circle"></i>
              <span>{{ importSuccess }}</span>
            </div>

            <div class="flex flex-col gap-3">
              <input
                ref="importInput"
                type="file"
                accept="application/json"
                @change="onImportFileChange"
                class="block w-full text-sm text-gray-500
                       file:mr-4 file:py-2 file:px-4
                       file:rounded-full file:border-0
                       file:text-sm file:font-semibold
                       file:bg-phisward-secondary/10 file:text-phisward-secondary
                       hover:file:bg-phisward-secondary/20"
              />
              <button
                @click="importScenario"
                :disabled="importingScenario || !fileToImport"
                class="w-full px-6 py-3 bg-phisward-primary text-white rounded-lg font-semibold shadow-lg hover:shadow-xl transition-all duration-200 disabled:opacity-50"
              >
                <span v-if="!importingScenario">
                  <i class="fas fa-file-import mr-2"></i>
                  Upload JSON
                </span>
                <span v-else>
                  <i class="fas fa-spinner fa-spin mr-2"></i>
                  Uploading...
                </span>
              </button>
            </div>
          </div>
        </div>
      </section>

      <section v-else class="bg-white rounded-2xl shadow p-10 text-center">
        <h2 class="text-2xl font-semibold text-phisward-primary mb-3">Welcome!</h2>
        <p class="text-gray-600">
          Use the navigation to start managing training content.
        </p>
      </section>
    </div>

    <ScenarioFormModal
      v-if="showScenarioModal"
      :mode="scenarioModalMode"
      :scenario="scenarioToEdit"
      @close="closeScenarioModal"
      @saved="onScenarioSaved"
    />

    <HookEmailModal
      v-if="showHookEmailModal && selectedScenarioId"
      :mode="hookEmailModalMode"
      :scenario-id="selectedScenarioId"
      :initial-email="hookEmailInitialData"
      @close="closeHookEmailModal"
      @saved="onHookEmailSaved"
    />
  </DashboardLayout>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import DashboardLayout from '@/components/dashboard/DashboardLayout.vue'
import ScenarioFormModal from '@/components/dashboard/member/ScenarioFormModal.vue'
import HookEmailModal from '@/components/dashboard/member/HookEmailModal.vue'

defineProps({
  role: {
    type: String,
    required: true
  }
})

const route = useRoute()
const router = useRouter()

const validTabs = ['scenarios', 'hook-email', 'import-export']

const scenarios = ref([])
const scenariosLoading = ref(false)
const scenariosError = ref('')
const scenariosSuccess = ref('')
const deletingScenarioId = ref('')

const selectedScenarioId = ref('')

const showScenarioModal = ref(false)
const scenarioModalMode = ref('create')
const scenarioToEdit = ref(null)

const hookEmail = ref(null)
const hookEmailLoading = ref(false)
const hookEmailError = ref('')
const hookEmailSuccess = ref('')
const deletingHookEmail = ref(false)
const hookEmailScenarioLoaded = ref('')

const showHookEmailModal = ref(false)
const hookEmailModalMode = ref('create')
const hookEmailInitialData = ref(null)

const fileToImport = ref(null)
const importError = ref('')
const importSuccess = ref('')
const importingScenario = ref(false)
const importInput = ref(null)

const exportError = ref('')
const exportSuccess = ref('')
const exportingScenario = ref(false)

const activeTab = computed(() => {
  const tab = route.query.tab
  if (typeof tab === 'string' && validTabs.includes(tab)) {
    return tab
  }
  return 'scenarios'
})

watch(
  () => route.query.tab,
  (tab) => {
    if (typeof tab !== 'string' || !validTabs.includes(tab)) {
      router.replace({ name: 'dashboard', query: { tab: 'scenarios' } })
    }
  },
  { immediate: true }
)

const extractErrorMessage = async (response, fallback) => {
  try {
    const data = await response.json()
    if (typeof data?.detail === 'string') {
      return data.detail
    }
    if (Array.isArray(data?.detail)) {
      return data.detail.join(', ')
    }
    if (typeof data?.message === 'string') {
      return data.message
    }
  } catch (err) {
    // ignore parsing errors
  }
  return fallback
}

const fetchScenarios = async () => {
  scenariosLoading.value = true
  scenariosError.value = ''
  scenariosSuccess.value = ''

  try {
    const token = localStorage.getItem('user_jwt_token')
    if (!token) {
      throw new Error('Authentication token is missing. Please log in again.')
    }

    const response = await fetch('/api/challenges/user/scenarios', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })

    if (!response.ok) {
      const message = await extractErrorMessage(response, 'Failed to load scenarios.')
      throw new Error(message)
    }

    const data = await response.json()
    scenarios.value = Array.isArray(data?.items) ? data.items : []
    ensureScenarioSelection()
  } catch (error) {
    scenariosError.value = error.message || 'Failed to load scenarios.'
    scenarios.value = []
    ensureScenarioSelection()
  } finally {
    scenariosLoading.value = false
  }
}

const ensureScenarioSelection = () => {
  const availableIds = scenarios.value.map((scenario) => scenario.id)
  const queryScenario = typeof route.query.scenario === 'string' ? route.query.scenario : ''

  if (queryScenario && availableIds.includes(queryScenario)) {
    selectedScenarioId.value = queryScenario
    return
  }

  if (availableIds.length > 0) {
    const firstId = availableIds[0]
    if (selectedScenarioId.value !== firstId) {
      selectedScenarioId.value = firstId
    }
    updateScenarioInRoute(firstId)
  } else {
    selectedScenarioId.value = ''
    updateScenarioInRoute('')
  }
}

const updateScenarioInRoute = (scenarioId) => {
  const nextQuery = { ...route.query }
  if (scenarioId) {
    if (nextQuery.scenario === scenarioId) {
      return
    }
    nextQuery.scenario = scenarioId
  } else {
    if (!nextQuery.scenario) {
      return
    }
    delete nextQuery.scenario
  }
  router.replace({ name: 'dashboard', query: nextQuery })
}

watch(
  () => route.query.scenario,
  (scenarioId) => {
    if (typeof scenarioId === 'string' && scenarios.value.some((scenario) => scenario.id === scenarioId)) {
      selectedScenarioId.value = scenarioId
    }
  }
)

watch(
  () => [activeTab.value, selectedScenarioId.value],
  ([tab, scenarioId]) => {
    if (tab === 'hook-email' && scenarioId) {
      loadHookEmail(scenarioId)
    }
    if (tab !== 'hook-email') {
      hookEmailScenarioLoaded.value = ''
    }
  }
)

const selectScenario = (scenarioId) => {
  if (!scenarioId) {
    return
  }
  selectedScenarioId.value = scenarioId
  updateScenarioInRoute(scenarioId)
  hookEmailSuccess.value = ''
  hookEmailError.value = ''
}

const openCreateScenarioModal = () => {
  scenarioModalMode.value = 'create'
  scenarioToEdit.value = null
  showScenarioModal.value = true
}

const openEditScenarioModal = (scenario) => {
  scenarioModalMode.value = 'edit'
  scenarioToEdit.value = scenario
  showScenarioModal.value = true
}

const closeScenarioModal = () => {
  showScenarioModal.value = false
}

const onScenarioSaved = async (message) => {
  showScenarioModal.value = false
  scenariosSuccess.value = message || 'Scenario saved successfully.'
  await fetchScenarios()
}

const deleteScenario = async (scenarioId) => {
  if (!window.confirm('Delete this scenario? This will also remove any associated hook emails.')) {
    return
  }

  deletingScenarioId.value = scenarioId
  scenariosError.value = ''
  scenariosSuccess.value = ''

  try {
    const token = localStorage.getItem('user_jwt_token')
    if (!token) {
      throw new Error('Authentication token is missing. Please log in again.')
    }

    const response = await fetch(`/api/challenges/user/scenarios?scenario_id=${scenarioId}`, {
      method: 'DELETE',
      headers: {
        Authorization: `Bearer ${token}`
      }
    })

    if (!response.ok) {
      const message = await extractErrorMessage(response, 'Failed to delete scenario.')
      throw new Error(message)
    }

    scenariosSuccess.value = 'Scenario deleted successfully.'
    await fetchScenarios()
  } catch (error) {
    scenariosError.value = error.message || 'Failed to delete scenario.'
  } finally {
    deletingScenarioId.value = ''
  }
}

const goToHookEmail = (scenarioId) => {
  if (!scenarioId) {
    return
  }
  selectedScenarioId.value = scenarioId
  const nextQuery = { ...route.query, tab: 'hook-email', scenario: scenarioId }
  router.replace({ name: 'dashboard', query: nextQuery })
}

const loadHookEmail = async (scenarioId, force = false) => {
  if (!force && hookEmailScenarioLoaded.value === scenarioId) {
    return
  }

  hookEmailLoading.value = true
  hookEmailError.value = ''
  hookEmailSuccess.value = ''

  try {
    const token = localStorage.getItem('user_jwt_token')
    if (!token) {
      throw new Error('Authentication token is missing. Please log in again.')
    }

    const response = await fetch(`/api/challenges/user/scenarios/hook-email?scenario_id=${scenarioId}`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })

    if (response.status === 404) {
      hookEmail.value = null
      hookEmailScenarioLoaded.value = scenarioId
      return
    }

    if (!response.ok) {
      const message = await extractErrorMessage(response, 'Failed to load hook email.')
      throw new Error(message)
    }

    hookEmail.value = await response.json()
    hookEmailScenarioLoaded.value = scenarioId
  } catch (error) {
    hookEmailError.value = error.message || 'Failed to load hook email.'
    hookEmail.value = null
    hookEmailScenarioLoaded.value = ''
  } finally {
    hookEmailLoading.value = false
  }
}

const openCreateHookEmailModal = () => {
  hookEmailModalMode.value = 'create'
  hookEmailInitialData.value = {
    subject: '',
    sender_email: '',
    language: 'en',
    body: '',
    variables: {}
  }
  showHookEmailModal.value = true
}

const openEditHookEmailModal = () => {
  hookEmailModalMode.value = 'edit'
  hookEmailInitialData.value = hookEmail.value
  showHookEmailModal.value = true
}

const closeHookEmailModal = () => {
  showHookEmailModal.value = false
}

const onHookEmailSaved = async (message) => {
  showHookEmailModal.value = false
  hookEmailSuccess.value = message || 'Hook email saved successfully.'
  await loadHookEmail(selectedScenarioId.value, true)
}

const deleteHookEmail = async () => {
  if (!selectedScenarioId.value) {
    return
  }

  if (!window.confirm('Delete the hook email for this scenario?')) {
    return
  }

  deletingHookEmail.value = true
  hookEmailError.value = ''
  hookEmailSuccess.value = ''

  try {
    const token = localStorage.getItem('user_jwt_token')
    if (!token) {
      throw new Error('Authentication token is missing. Please log in again.')
    }

    const response = await fetch(`/api/challenges/user/scenarios/hook-email?scenario_id=${selectedScenarioId.value}`, {
      method: 'DELETE',
      headers: {
        Authorization: `Bearer ${token}`
      }
    })

    if (!response.ok) {
      const message = await extractErrorMessage(response, 'Failed to delete hook email.')
      throw new Error(message)
    }

    hookEmailSuccess.value = 'Hook email deleted successfully.'
    hookEmail.value = null
    hookEmailScenarioLoaded.value = ''
  } catch (error) {
    hookEmailError.value = error.message || 'Failed to delete hook email.'
  } finally {
    deletingHookEmail.value = false
  }
}

const onImportFileChange = (event) => {
  const [file] = event.target.files
  fileToImport.value = file || null
  importError.value = ''
  importSuccess.value = ''
}

const importScenario = async () => {
  if (!fileToImport.value) {
    importError.value = 'Select a JSON file to import.'
    return
  }

  importError.value = ''
  importSuccess.value = ''
  importingScenario.value = true

  try {
    const token = localStorage.getItem('user_jwt_token')
    if (!token) {
      throw new Error('Authentication token is missing. Please log in again.')
    }

    const formData = new FormData()
    formData.append('file', fileToImport.value)

    const response = await fetch('/api/challenges/user/scenarios/import', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`
      },
      body: formData
    })

    if (!response.ok) {
      const message = await extractErrorMessage(response, 'Failed to import scenario.')
      throw new Error(message)
    }

    importSuccess.value = 'Scenario imported successfully.'
    fileToImport.value = null
    if (importInput.value) {
      importInput.value.value = ''
    }
    await fetchScenarios()
  } catch (error) {
    importError.value = error.message || 'Failed to import scenario.'
  } finally {
    importingScenario.value = false
  }
}

const exportScenario = async () => {
  if (!selectedScenarioId.value) {
    exportError.value = 'Select a scenario to export.'
    return
  }

  exportError.value = ''
  exportSuccess.value = ''
  exportingScenario.value = true

  try {
    const token = localStorage.getItem('user_jwt_token')
    if (!token) {
      throw new Error('Authentication token is missing. Please log in again.')
    }

    const response = await fetch(`/api/challenges/user/scenarios/export?scenario_id=${selectedScenarioId.value}`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })

    if (!response.ok) {
      const message = await extractErrorMessage(response, 'Failed to export scenario.')
      throw new Error(message)
    }

    const blob = await response.blob()
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    const filename =
      response.headers.get('Content-Disposition')?.split('filename=')[1]?.replace(/"/g, '') ||
      `scenario-${selectedScenarioId.value}.json`
    link.href = url
    link.download = filename
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
    exportSuccess.value = 'Scenario exported successfully.'
  } catch (error) {
    exportError.value = error.message || 'Failed to export scenario.'
  } finally {
    exportingScenario.value = false
  }
}

watch(activeTab, (tab) => {
  if (tab === 'import-export') {
    exportError.value = ''
    exportSuccess.value = ''
    importError.value = ''
    importSuccess.value = ''
  }
})

onMounted(() => {
  fetchScenarios()
})

const prettyJson = (value) => {
  try {
    return JSON.stringify(value, null, 2)
  } catch (err) {
    return String(value)
  }
}

const formatDate = (value) => {
  if (!value) {
    return 'recently'
  }

  try {
    const date = new Date(value)
    return date.toLocaleDateString(undefined, {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    })
  } catch (err) {
    return 'recently'
  }
}
</script>
