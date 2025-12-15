<template>
  <DashboardLayout :role="role">
    <div class="space-y-8">
      <div class="bg-white rounded-2xl shadow p-4 flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
        <div>
          <h2 class="text-xl font-semibold text-phisward-primary">Member Workspace</h2>
          <p class="text-sm text-gray-600">Jump between your organization directory, scenarios, hook emails, and tools.</p>
        </div>
        <div class="flex flex-wrap gap-2">
          <button
            v-for="tab in tabOptions"
            :key="tab.key"
            @click="navigateToTab(tab.key)"
            class="inline-flex items-center gap-2 px-4 py-2 rounded-lg border transition-all duration-200 font-semibold"
            :class="activeTab === tab.key ? 'bg-phisward-secondary text-white border-phisward-secondary shadow-lg' : 'bg-white text-gray-600 border-gray-200 hover:border-phisward-secondary/60 hover:text-phisward-secondary'"
          >
            <i :class="`${tab.icon} mr-2`"></i>
            {{ tab.label }}
          </button>
        </div>
      </div>

      <section v-if="activeTab === 'org-directory'" class="space-y-6">
        <header class="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
          <div>
            <h1 class="text-3xl font-bold text-phisward-primary">Organization Directory</h1>
            <p class="text-gray-600">
              Review the employees that belong to your organization. This list is maintained by your org admin.
            </p>
          </div>
          <button
            @click="refreshOrgMembers"
            class="self-start lg:self-auto px-6 py-3 border border-phisward-secondary text-phisward-secondary rounded-lg font-semibold hover:bg-phisward-secondary/10 transition-all duration-200 disabled:opacity-50"
            :disabled="orgMembersLoading"
          >
            <span v-if="!orgMembersLoading">
              <i class="fas fa-sync-alt mr-2"></i>
              Refresh Directory
            </span>
            <span v-else>
              <i class="fas fa-spinner fa-spin mr-2"></i>
              Refreshing...
            </span>
          </button>
        </header>

        <div v-if="orgMembersError" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg flex items-center gap-2">
          <i class="fas fa-exclamation-triangle"></i>
          <span>{{ orgMembersError }}</span>
        </div>

        <div
          v-if="orgMembersLoading && orgMembers.length === 0"
          class="flex items-center justify-center py-16 bg-white rounded-2xl shadow"
        >
          <i class="fas fa-spinner fa-spin text-3xl text-phisward-secondary"></i>
        </div>

        <div
          v-else-if="orgMembers.length === 0"
          class="flex flex-col items-center justify-center py-16 bg-white rounded-2xl shadow text-center space-y-4"
        >
          <div class="w-16 h-16 rounded-full bg-phisward-fourth/50 flex items-center justify-center">
            <i class="fas fa-users text-2xl text-phisward-secondary"></i>
          </div>
          <div>
            <h2 class="text-xl font-semibold text-phisward-primary">No employees listed yet</h2>
            <p class="text-gray-600">
              Ask your organization admin to populate the directory, then refresh this view.
            </p>
          </div>
        </div>

        <div v-else class="bg-white rounded-2xl shadow divide-y divide-gray-100">
          <div
            v-for="member in orgMembers"
            :key="member.id"
            class="px-6 py-4 flex flex-col md:flex-row md:items-center md:justify-between gap-3"
          >
            <div class="flex items-start gap-3">
              <div class="w-12 h-12 rounded-full bg-phisward-fourth flex items-center justify-center text-phisward-secondary text-lg font-semibold">
                {{ (member.first_name || '?')[0] }}{{ (member.last_name || '')[0] || '' }}
              </div>
              <div>
                <h2 class="text-lg font-semibold text-phisward-primary">
                  {{ member.first_name }} {{ member.last_name }}
                </h2>
                <p class="text-sm text-gray-600">{{ member.email }}</p>
              </div>
            </div>
            <div class="flex flex-col gap-3 sm:items-end">
              <div class="text-xs text-gray-500 flex flex-wrap gap-4 sm:justify-end">
                <span class="inline-flex items-center gap-1">
                  <i class="fas fa-id-card"></i>
                  {{ member.id }}
                </span>
                <span class="inline-flex items-center gap-1" v-if="member.created_at">
                  <i class="fas fa-clock"></i>
                  Added {{ formatDate(member.created_at) }}
                </span>
              </div>
              <button
                @click="openStartChallengeModal(member)"
                :disabled="scenarios.length === 0"
                :title="scenarios.length === 0 ? 'Create a scenario first to start a challenge.' : ''"
                class="self-start sm:self-auto px-4 py-2 bg-gradient-to-r from-phisward-secondary to-phisward-third text-white rounded-lg font-semibold shadow-lg hover:shadow-xl transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <i class="fas fa-flag-checkered mr-2"></i>
                Start Challenge
              </button>
            </div>
          </div>
        </div>
      </section>

      <section v-else-if="activeTab === 'challenges'" class="space-y-6">
        <header class="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
          <div>
            <h1 class="text-3xl font-bold text-phisward-primary">Challenges</h1>
            <p class="text-gray-600">
              Monitor phishing awareness challenges started for your organization.
            </p>
          </div>
          <div class="flex flex-col sm:flex-row gap-3 w-full lg:w-auto sm:items-center">
            <div class="flex items-center gap-2">
              <label for="challenge_status_filter" class="text-sm font-semibold text-gray-700">Status</label>
              <select
                id="challenge_status_filter"
                v-model="challengeStatusFilter"
                @change="fetchChallenges"
                class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-phisward-secondary focus:border-transparent transition-all bg-white text-sm"
              >
                <option
                  v-for="option in challengeStatusOptions"
                  :key="option.value"
                  :value="option.value"
                >
                  {{ option.label }}
                </option>
              </select>
            </div>
            <button
              @click="fetchChallenges"
              class="px-5 py-2 border border-phisward-secondary text-phisward-secondary rounded-lg font-semibold hover:bg-phisward-secondary/10 transition-all duration-200 disabled:opacity-50"
              :disabled="challengesLoading"
            >
              <span v-if="!challengesLoading">
                <i class="fas fa-sync-alt mr-2"></i>
                Refresh Challenges
              </span>
              <span v-else>
                <i class="fas fa-spinner fa-spin mr-2"></i>
                Loading...
              </span>
            </button>
          </div>
        </header>

        <div class="bg-white rounded-2xl border border-gray-100 shadow-sm p-4 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
          <div class="flex items-center gap-3">
            <div class="w-12 h-12 rounded-xl bg-phisward-fourth flex items-center justify-center text-phisward-secondary">
              <i class="fas fa-envelope-open-text text-xl"></i>
            </div>
            <div>
              <p class="text-sm text-gray-500">Pending emails</p>
              <p class="text-2xl font-semibold text-phisward-primary">
                <span v-if="pendingEmailsLoading" class="text-base text-gray-500">
                  <i class="fas fa-spinner fa-spin"></i>
                  Loading...
                </span>
                <span v-else>{{ pendingEmailsCount }}</span>
              </p>
              <p v-if="pendingEmailsError" class="text-sm text-red-600">{{ pendingEmailsError }}</p>
            </div>
          </div>
          <button
            @click="sendAllPendingEmails"
            class="inline-flex items-center justify-center gap-2 px-4 py-2 bg-gradient-to-r from-phisward-secondary to-phisward-third text-white rounded-lg font-semibold shadow hover:shadow-lg transition-all duration-200 disabled:opacity-50"
            :disabled="sendingPending || pendingEmailsLoading || pendingEmailsCount === 0"
          >
            <span v-if="!sendingPending">
              <i class="fas fa-paper-plane"></i>
              Send all pending
            </span>
            <span v-else>
              <i class="fas fa-spinner fa-spin"></i>
              Sending...
            </span>
          </button>
        </div>

        <div v-if="challengesError" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg flex items-center gap-2">
          <i class="fas fa-exclamation-triangle"></i>
          <span>{{ challengesError }}</span>
        </div>

        <div v-if="challengesSuccess" class="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg flex items-center gap-2">
          <i class="fas fa-check-circle"></i>
          <span>{{ challengesSuccess }}</span>
        </div>

        <div
          v-if="challengesLoading"
          class="flex items-center justify-center py-16 bg-white rounded-2xl shadow"
        >
          <i class="fas fa-spinner fa-spin text-3xl text-phisward-secondary"></i>
        </div>

        <div
          v-else-if="challenges.length === 0"
          class="flex flex-col items-center justify-center py-16 bg-white rounded-2xl shadow text-center space-y-4"
        >
          <div class="w-16 h-16 rounded-full bg-phisward-fourth/50 flex items-center justify-center">
            <i class="fas fa-flag text-2xl text-phisward-secondary"></i>
          </div>
          <div>
            <h2 class="text-xl font-semibold text-phisward-primary">No challenges to display</h2>
            <p class="text-gray-600">
              Start a challenge from the directory to see it tracked here.
            </p>
          </div>
        </div>

        <div v-else class="bg-white rounded-2xl shadow divide-y divide-gray-100">
          <article
            v-for="challenge in challenges"
            :key="challenge.id"
            class="px-6 py-5 flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4"
          >
            <div class="space-y-2">
              <div class="flex flex-wrap items-center gap-3">
                <h3 class="text-lg font-semibold text-gray-900">
                  {{ getMemberName(challenge.employee_id) }}
                </h3>
                <span class="text-sm text-gray-600">
                  {{ getMemberEmail(challenge.employee_id) || 'No email' }}
                </span>
                <span
                  class="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-semibold uppercase tracking-wide"
                  :class="statusBadgeClass(challenge.status)"
                >
                  <i class="fas fa-bullseye"></i>
                  {{ formatStatusLabel(challenge.status) }}
                </span>
                <span
                  class="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-semibold uppercase tracking-wide"
                  :class="emailStatusBadgeClass(challengeEmailStatuses[challenge.id])"
                >
                  <i class="fas fa-envelope-open"></i>
                  {{ formatEmailStatusLabel(challengeEmailStatuses[challenge.id]) }}
                </span>
              </div>
              <p class="text-sm text-gray-700">
                Scenario:
                <span class="font-semibold text-phisward-primary">{{ getScenarioName(challenge.scenario_id) }}</span>
              </p>
              <div class="flex flex-wrap gap-4 text-xs text-gray-500">
                <span class="inline-flex items-center gap-1">
                  <i class="fas fa-percentage"></i>
                  Score: {{ formatScore(challenge.score) }}
                </span>
                <span class="inline-flex items-center gap-1" v-if="challenge.created_at">
                  <i class="fas fa-clock"></i>
                  Started {{ formatDate(challenge.created_at) }}
                </span>
                <span class="inline-flex items-center gap-1" v-if="challenge.updated_at && challenge.updated_at !== challenge.created_at">
                  <i class="fas fa-history"></i>
                  Updated {{ formatDate(challenge.updated_at) }}
                </span>
                <span class="inline-flex items-center gap-1">
                  <i class="fas fa-envelope"></i>
                  Exchanges: {{ challengeExchangeCounts[challenge.id] ?? '—' }}
                </span>
              </div>
            </div>
            <div class="flex flex-col sm:flex-row gap-2 w-full lg:w-auto">
              <button
                v-if="canGenerateAiResponse(challenge)"
                @click="generateAiResponse(challenge.id)"
                class="flex-1 sm:flex-none px-4 py-2 bg-gradient-to-r from-phisward-secondary to-phisward-third text-white rounded-lg font-semibold shadow hover:shadow-lg transition-all duration-200 disabled:opacity-50"
                :disabled="generatingAiChallengeId === challenge.id"
              >
                <span v-if="generatingAiChallengeId !== challenge.id">
                  <i class="fas fa-robot mr-2"></i>
                  Generate AI Response
                </span>
                <span v-else>
                  <i class="fas fa-spinner fa-spin mr-2"></i>
                  Generating...
                </span>
              </button>
              <button
                @click="openChallengeStatusModal(challenge)"
                class="flex-1 sm:flex-none px-4 py-2 bg-phisward-primary text-white rounded-lg font-semibold hover:bg-phisward-primary/90 transition-all duration-200"
              >
                <i class="fas fa-pen mr-2"></i>
                Update Status
              </button>
              <button
                @click="deleteChallenge(challenge.id)"
                class="flex-1 sm:flex-none px-4 py-2 border border-red-200 text-red-600 rounded-lg font-semibold hover:bg-red-50 transition-all duration-200 disabled:opacity-50"
                :disabled="deletingChallengeId === challenge.id"
              >
                <span v-if="deletingChallengeId !== challenge.id">
                  <i class="fas fa-trash mr-2"></i>
                  Delete
                </span>
                <span v-else>
                  <i class="fas fa-spinner fa-spin mr-2"></i>
                  Deleting...
                </span>
              </button>
            </div>
          </article>
        </div>
      </section>

      <section v-else-if="activeTab === 'scenarios'" class="space-y-6">
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
                  <span
                    class="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-semibold uppercase tracking-wide"
                    :class="isHookConfigured(scenario.id) ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-600'"
                  >
                    <i :class="isHookConfigured(scenario.id) ? 'fas fa-check' : 'fas fa-envelope-open-text'"></i>
                    {{ isHookConfigured(scenario.id) ? 'Hook Configured' : 'Hook Missing' }}
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

    <StartChallengeModal
      v-if="showStartChallengeModal && startChallengeMember"
      :member="startChallengeMember"
      :scenarios="scenarios"
      @close="closeStartChallengeModal"
      @started="onChallengeStarted"
    />

    <ChallengeStatusModal
      v-if="showStatusModal && statusModalChallenge"
      :challenge="statusModalChallenge"
      :employee-name="getMemberName(statusModalChallenge.employee_id)"
      :scenario-name="getScenarioName(statusModalChallenge.scenario_id)"
      @close="closeChallengeStatusModal"
      @updated="onChallengeUpdated"
    />
  </DashboardLayout>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import DashboardLayout from '@/components/dashboard/DashboardLayout.vue'
import ScenarioFormModal from '@/components/dashboard/member/ScenarioFormModal.vue'
import HookEmailModal from '@/components/dashboard/member/HookEmailModal.vue'
import StartChallengeModal from '@/components/dashboard/member/StartChallengeModal.vue'
import ChallengeStatusModal from '@/components/dashboard/member/ChallengeStatusModal.vue'

defineProps({
  role: {
    type: String,
    required: true
  }
})

const route = useRoute()
const router = useRouter()

const validTabs = ['org-directory', 'challenges', 'scenarios', 'hook-email', 'import-export']

const orgMembers = ref([])
const orgMembersLoading = ref(false)
const orgMembersError = ref('')
const orgMembersLoaded = ref(false)

const challenges = ref([])
const challengesLoading = ref(false)
const challengesError = ref('')
const challengesSuccess = ref('')
const challengeStatusFilter = ref('ALL')
const deletingChallengeId = ref('')
const generatingAiChallengeId = ref('')
const pendingEmailsCount = ref(0)
const pendingEmailsLoading = ref(false)
const pendingEmailsError = ref('')
const sendingPending = ref(false)
const showStartChallengeModal = ref(false)
const showStatusModal = ref(false)
const startChallengeMember = ref(null)
const statusModalChallenge = ref(null)
const challengeExchangeCounts = ref({})
const challengeEmailStatuses = ref({})

const memberCache = ref({})
const scenarioCache = ref({})

const challengeStatusOptions = [
  { value: 'ALL', label: 'All statuses' },
  { value: 'ONGOING', label: 'Ongoing' },
  { value: 'SUCCESS', label: 'Success' },
  { value: 'FAILURE', label: 'Failure' }
]

const tabOptions = [
  { key: 'org-directory', label: 'Directory', icon: 'fas fa-users' },
  { key: 'challenges', label: 'Challenges', icon: 'fas fa-flag-checkered' },
  { key: 'scenarios', label: 'Scenarios', icon: 'fas fa-tasks' },
  { key: 'hook-email', label: 'Hook Emails', icon: 'fas fa-envelope-open-text' },
  { key: 'import-export', label: 'Import/Export', icon: 'fas fa-file-import' }
]

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
const hookStatus = ref({})

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
  return 'org-directory'
})

watch(
  () => route.query.tab,
  (tab) => {
    if (typeof tab !== 'string' || !validTabs.includes(tab)) {
      router.replace({ name: 'dashboard', query: { tab: 'org-directory' } })
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

const getUserIdFromToken = () => {
  const token = localStorage.getItem('user_jwt_token')
  if (!token) {
    return ''
  }
  const parts = token.split('.')
  if (parts.length < 2) {
    return ''
  }
  try {
    const payload = JSON.parse(atob(parts[1]))
    return payload?.user_id || ''
  } catch (err) {
    return ''
  }
}

const cacheMembers = (members) => {
  if (!Array.isArray(members)) {
    return
  }
  members.forEach((member) => {
    if (member?.id) {
      memberCache.value[member.id] = member
    }
  })
}

const cacheScenarios = (items) => {
  if (!Array.isArray(items)) {
    return
  }
  items.forEach((scenario) => {
    if (scenario?.id) {
      scenarioCache.value[scenario.id] = scenario
    }
  })
}

const fetchOrgMembers = async (force = false) => {
  if (orgMembersLoading.value) {
    return
  }

  if (!force && orgMembersLoaded.value) {
    return
  }

  orgMembersLoading.value = true
  orgMembersError.value = ''
  const hadMembers = orgMembersLoaded.value && orgMembers.value.length > 0

  try {
    const token = localStorage.getItem('user_jwt_token')
    if (!token) {
      throw new Error('Authentication token is missing. Please log in again.')
    }

    const response = await fetch('/api/challenges/user/organization/members', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })

    if (!response.ok) {
      const message = await extractErrorMessage(response, 'Failed to load organization directory.')
      throw new Error(message)
    }

    orgMembers.value = await response.json()
    cacheMembers(orgMembers.value)
    orgMembersLoaded.value = true
  } catch (error) {
    orgMembersError.value = error.message || 'Failed to load organization directory.'
    if (!hadMembers) {
      orgMembers.value = []
    }
    orgMembersLoaded.value = false
  } finally {
    orgMembersLoading.value = false
  }
}

const refreshOrgMembers = () => {
  fetchOrgMembers(true)
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
    cacheScenarios(scenarios.value)
    ensureScenarioSelection()
    await preloadHookStatuses()
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
  orgMembers,
  (members) => {
    cacheMembers(members)
  },
  { deep: true }
)

watch(
  scenarios,
  (items) => {
    cacheScenarios(items)
  },
  { deep: true }
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
      hookStatus.value[scenarioId] = false
      return
    }

    if (!response.ok) {
      const message = await extractErrorMessage(response, 'Failed to load hook email.')
      throw new Error(message)
    }

    hookEmail.value = await response.json()
    hookStatus.value[scenarioId] = true
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
  hookStatus.value[selectedScenarioId.value] = true
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
    hookStatus.value[selectedScenarioId.value] = false
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

const resolveMember = async (memberId) => {
  if (!memberId) {
    return null
  }
  if (memberCache.value[memberId]) {
    return memberCache.value[memberId]
  }
  const existingMember = orgMembers.value.find((member) => member.id === memberId)
  if (existingMember) {
    memberCache.value[memberId] = existingMember
    return existingMember
  }

  try {
    const token = localStorage.getItem('user_jwt_token')
    if (!token) {
      throw new Error('Authentication token is missing. Please log in again.')
    }
    const response = await fetch(`/api/challenges/user/organization/members?id=${memberId}`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    if (!response.ok) {
      return null
    }
    const data = await response.json()
    if (Array.isArray(data) && data[0]?.id) {
      memberCache.value[data[0].id] = data[0]
      return data[0]
    }
  } catch (err) {
    // swallow errors and let the UI fallback to IDs
  }
  return null
}

const resolveScenario = async (scenarioId) => {
  if (!scenarioId) {
    return null
  }
  if (scenarioCache.value[scenarioId]) {
    return scenarioCache.value[scenarioId]
  }
  const existingScenario = scenarios.value.find((scenario) => scenario.id === scenarioId)
  if (existingScenario) {
    scenarioCache.value[scenarioId] = existingScenario
    return existingScenario
  }

  try {
    const token = localStorage.getItem('user_jwt_token')
    if (!token) {
      throw new Error('Authentication token is missing. Please log in again.')
    }
    const response = await fetch(`/api/challenges/user/scenarios?id=${scenarioId}`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    if (!response.ok) {
      return null
    }
    const data = await response.json()
    if (Array.isArray(data?.items) && data.items[0]?.id) {
      scenarioCache.value[data.items[0].id] = data.items[0]
      return data.items[0]
    }
  } catch (err) {
    // ignore detail fetch errors
  }
  return null
}

const resolveChallengeDetails = async (items) => {
  if (!Array.isArray(items)) {
    return
  }
  await Promise.all(
    items.map(async (challenge) => {
      await Promise.all([resolveMember(challenge.employee_id), resolveScenario(challenge.scenario_id)])
    })
  )
}

const checkScenarioHook = async (scenarioId, force = false) => {
  if (!scenarioId) {
    return false
  }
  if (!force && scenarioId in hookStatus.value) {
    return hookStatus.value[scenarioId]
  }

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
      hookStatus.value[scenarioId] = false
      return false
    }

    if (!response.ok) {
      const message = await extractErrorMessage(response, 'Failed to verify hook email.')
      throw new Error(message)
    }

    hookStatus.value[scenarioId] = true
    return true
  } catch (error) {
    // keep previous known value if we have one
    return hookStatus.value[scenarioId] ?? false
  }
}

const preloadHookStatuses = async () => {
  const scenarioIds = scenarios.value.map((scenario) => scenario.id)
  await Promise.allSettled(scenarioIds.map((id) => checkScenarioHook(id)))
}

const fetchPendingEmailsCount = async () => {
  const userId = getUserIdFromToken()
  if (!userId) {
    pendingEmailsError.value = 'Could not identify user. Please log in again.'
    pendingEmailsCount.value = 0
    return
  }

  pendingEmailsLoading.value = true
  pendingEmailsError.value = ''

  try {
    const token = localStorage.getItem('user_jwt_token')
    if (!token) {
      throw new Error('Authentication token is missing. Please log in again.')
    }

    const response = await fetch(`/api/monitoring/pending-emails/count?user_id=${userId}`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })

    if (!response.ok) {
      const message = await extractErrorMessage(response, 'Failed to load pending emails.')
      throw new Error(message)
    }

    const data = await response.json()
    pendingEmailsCount.value = typeof data?.count === 'number' ? data.count : 0
  } catch (error) {
    pendingEmailsError.value = error.message || 'Failed to load pending emails.'
    pendingEmailsCount.value = 0
  } finally {
    pendingEmailsLoading.value = false
  }
}

const fetchChallengeExchangeCounts = async (items) => {
  challengeExchangeCounts.value = {}
  if (!Array.isArray(items) || items.length === 0) {
    return
  }

  const token = localStorage.getItem('user_jwt_token')
  if (!token) {
    pendingEmailsError.value = 'Authentication token is missing. Please log in again.'
    return
  }

  const queries = items.map(async (challenge) => {
    try {
      const response = await fetch(`/api/monitoring/get-exchanges/count?challenge_id=${challenge.id}`, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
      if (!response.ok) {
        return
      }
      const data = await response.json()
      challengeExchangeCounts.value[challenge.id] = typeof data?.count === 'number' ? data.count : 0
    } catch (err) {
      // skip failing counts to avoid blocking the rest
    }
  })

  await Promise.allSettled(queries)
}

const fetchChallengeEmailStatuses = async (items) => {
  challengeEmailStatuses.value = {}
  if (!Array.isArray(items) || items.length === 0) {
    return
  }

  const token = localStorage.getItem('user_jwt_token')
  if (!token) {
    challengesError.value = 'Authentication token is missing. Please log in again.'
    return
  }

  const queries = items.map(async (challenge) => {
    try {
      const response = await fetch(`/api/monitoring/challenge-last-email-status?challenge_id=${challenge.id}`, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
      if (!response.ok) {
        return
      }
      const data = await response.json()
      challengeEmailStatuses.value[challenge.id] = data?.status ?? null
    } catch (err) {
      // ignore failing status fetches
    }
  })

  await Promise.allSettled(queries)
}

const fetchChallenges = async () => {
  challengesLoading.value = true
  challengesError.value = ''
  pendingEmailsError.value = ''

  const params = new URLSearchParams()
  if (challengeStatusFilter.value !== 'ALL') {
    params.append('status', challengeStatusFilter.value)
  }
  const query = params.toString() ? `?${params.toString()}` : ''

  try {
    const token = localStorage.getItem('user_jwt_token')
    if (!token) {
      throw new Error('Authentication token is missing. Please log in again.')
    }

    const response = await fetch(`/api/monitoring/challenges${query}`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })

    if (!response.ok) {
      const message = await extractErrorMessage(response, 'Failed to load challenges.')
      throw new Error(message)
    }

    const data = await response.json()
    challenges.value = Array.isArray(data?.items) ? data.items : []
    challengesLoading.value = false

    await Promise.allSettled([
      resolveChallengeDetails(challenges.value),
      fetchChallengeExchangeCounts(challenges.value),
      fetchChallengeEmailStatuses(challenges.value),
      fetchPendingEmailsCount()
    ])
  } catch (error) {
    challengesError.value = error.message || 'Failed to load challenges.'
    challenges.value = []
  } finally {
    challengesLoading.value = false
  }
}

const openStartChallengeModal = (member) => {
  if (!member || scenarios.value.length === 0) {
    challengesError.value = scenarios.value.length === 0 ? 'Create a scenario before starting a challenge.' : 'Select a valid employee.'
    return
  }
  challengesError.value = ''
  challengesSuccess.value = ''
  startChallengeMember.value = member
  showStartChallengeModal.value = true
}

const closeStartChallengeModal = () => {
  showStartChallengeModal.value = false
  startChallengeMember.value = null
}

const onChallengeStarted = async (challenge) => {
  closeStartChallengeModal()
  if (challenge?.id) {
    challengesSuccess.value = 'Challenge started successfully.'
    if (activeTab.value !== 'challenges') {
      navigateToTab('challenges')
    } else {
      await fetchChallenges()
    }
  }
}

const sendAllPendingEmails = async () => {
  sendingPending.value = true
  challengesError.value = ''
  challengesSuccess.value = ''
  pendingEmailsError.value = ''

  try {
    const token = localStorage.getItem('user_jwt_token')
    if (!token) {
      throw new Error('Authentication token is missing. Please log in again.')
    }

    const response = await fetch('/api/monitoring/send-all-pending', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`
      }
    })

    if (!response.ok) {
      const message = await extractErrorMessage(response, 'Failed to send pending emails.')
      throw new Error(message)
    }

    challengesSuccess.value = 'Pending emails sent successfully.'
    await Promise.all([fetchChallenges(), fetchPendingEmailsCount()])
  } catch (error) {
    challengesError.value = error.message || 'Failed to send pending emails.'
  } finally {
    sendingPending.value = false
  }
}

const generateAiResponse = async (challengeId) => {
  if (!challengeId) {
    return
  }

  const challenge = challenges.value.find((item) => item.id === challengeId)
  if (!canGenerateAiResponse(challenge)) {
    challengesError.value = 'AI responses can only be generated for ongoing challenges.'
    return
  }

  generatingAiChallengeId.value = challengeId
  challengesError.value = ''
  challengesSuccess.value = ''

  try {
    const token = localStorage.getItem('user_jwt_token')
    if (!token) {
      throw new Error('Authentication token is missing. Please log in again.')
    }

    const response = await fetch(`/api/agentic/email-agentic-flow?challenge_id=${challengeId}`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`
      }
    })

    if (!response.ok) {
      const message = await extractErrorMessage(response, 'Failed to generate AI response.')
      throw new Error(message)
    }

    challengesSuccess.value = 'AI response generated successfully.'
    await fetchChallenges()
  } catch (error) {
    challengesError.value = error.message || 'Failed to generate AI response.'
  } finally {
    generatingAiChallengeId.value = ''
  }
}

const openChallengeStatusModal = (challenge) => {
  if (!challenge) {
    return
  }
  challengesError.value = ''
  challengesSuccess.value = ''
  statusModalChallenge.value = challenge
  showStatusModal.value = true
}

const closeChallengeStatusModal = () => {
  showStatusModal.value = false
  statusModalChallenge.value = null
}

const onChallengeUpdated = async (updatedChallenge, message) => {
  closeChallengeStatusModal()
  if (updatedChallenge?.id) {
    challengesSuccess.value = message || 'Challenge updated successfully.'
    await fetchChallenges()
  }
}

const deleteChallenge = async (challengeId) => {
  if (!challengeId) {
    return
  }

  if (!window.confirm('Delete this challenge? Only completed challenges can be removed.')) {
    return
  }

  deletingChallengeId.value = challengeId
  challengesError.value = ''
  challengesSuccess.value = ''

  try {
    const token = localStorage.getItem('user_jwt_token')
    if (!token) {
      throw new Error('Authentication token is missing. Please log in again.')
    }

    const response = await fetch(`/api/monitoring/challenges?challenge_id=${challengeId}`, {
      method: 'DELETE',
      headers: {
        Authorization: `Bearer ${token}`
      }
    })

    if (!response.ok) {
      const message = await extractErrorMessage(response, 'Failed to delete challenge.')
      throw new Error(message)
    }

    challengesSuccess.value = 'Challenge deleted successfully.'
    await fetchChallenges()
  } catch (error) {
    challengesError.value = error.message || 'Failed to delete challenge.'
  } finally {
    deletingChallengeId.value = ''
  }
}

watch(
  activeTab,
  (tab) => {
    if (tab === 'org-directory') {
      fetchOrgMembers()
    }

    if (tab === 'challenges') {
      fetchOrgMembers()
      fetchChallenges()
    }

    if (tab === 'import-export') {
      exportError.value = ''
      exportSuccess.value = ''
      importError.value = ''
      importSuccess.value = ''
    }
  },
  { immediate: true }
)

onMounted(() => {
  fetchScenarios()
})

const navigateToTab = (tabKey) => {
  if (!validTabs.includes(tabKey)) {
    return
  }
  if (activeTab.value === tabKey) {
    return
  }
  const nextQuery = { ...route.query, tab: tabKey }
  router.replace({ name: 'dashboard', query: nextQuery })
}

const prettyJson = (value) => {
  try {
    return JSON.stringify(value, null, 2)
  } catch (err) {
    return String(value)
  }
}

const getMemberName = (memberId) => {
  const member = memberCache.value[memberId] || orgMembers.value.find((item) => item.id === memberId)
  if (!member) {
    return 'Unknown employee'
  }
  return `${member.first_name} ${member.last_name}`
}

const getMemberEmail = (memberId) => {
  const member = memberCache.value[memberId] || orgMembers.value.find((item) => item.id === memberId)
  return member?.email || ''
}

const getScenarioName = (scenarioId) => {
  const scenario = scenarioCache.value[scenarioId] || scenarios.value.find((item) => item.id === scenarioId)
  return scenario?.name || 'Unknown scenario'
}

const statusBadgeClass = (status) => {
  if (status === 'SUCCESS') {
    return 'bg-green-100 text-green-700'
  }
  if (status === 'FAILURE') {
    return 'bg-red-100 text-red-700'
  }
  if (status === 'ONGOING') {
    return 'bg-phisward-fourth text-phisward-primary'
  }
  return 'bg-gray-100 text-gray-700'
}

const emailStatusBadgeClass = (status) => {
  if (status === 'RECIEVED') {
    return 'bg-green-100 text-green-700'
  }
  if (status === 'SENT') {
    return 'bg-blue-100 text-blue-700'
  }
  if (status === 'PENDING') {
    return 'bg-yellow-100 text-yellow-700'
  }
  return 'bg-gray-100 text-gray-700'
}

const formatStatusLabel = (status) => {
  if (!status) {
    return ''
  }
  return status.charAt(0) + status.slice(1).toLowerCase()
}

const canGenerateAiResponse = (challenge) => {
  if (!challenge) {
    return false
  }
  return (challenge.status || '').toUpperCase() === 'ONGOING'
}

const formatEmailStatusLabel = (status) => {
  if (status === 'RECIEVED') {
    return 'Received'
  }
  if (status === 'SENT') {
    return 'Sent'
  }
  if (status === 'PENDING') {
    return 'Pending'
  }
  if (status === null) {
    return 'No email yet'
  }
  if (!status) {
    return 'No email yet'
  }
  return status.charAt(0) + status.slice(1).toLowerCase()
}

const formatScore = (score) => {
  if (score === null || score === undefined) {
    return 'N/A'
  }
  const numericScore = Number(score)
  if (Number.isNaN(numericScore)) {
    return 'N/A'
  }
  return numericScore
}

const isHookConfigured = (scenarioId) => {
  if (!scenarioId) {
    return false
  }
  return Boolean(hookStatus.value[scenarioId])
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
