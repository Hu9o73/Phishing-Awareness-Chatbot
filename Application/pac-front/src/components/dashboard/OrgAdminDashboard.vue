<template>
  <DashboardLayout :role="role">
    <div class="space-y-8">
      <div class="bg-white rounded-2xl shadow p-4 flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
        <div>
          <h2 class="text-xl font-semibold text-phisward-primary">Organization Controls</h2>
          <p class="text-sm text-gray-600">Toggle between the employee directory and user accounts.</p>
        </div>
        <div class="flex flex-wrap gap-2">
          <button
            v-for="tab in tabOptions"
            :key="tab.key"
            @click="navigateToTab(tab.key)"
            class="inline-flex items-center gap-2 px-4 py-2 rounded-lg border transition-all duration-200 font-semibold"
            :class="activeTab === tab.key ? 'bg-phisward-secondary text-white border-phisward-secondary shadow-lg' : 'bg-white text-gray-600 border-gray-200 hover:border-phisward-secondary/60 hover:text-phisward-secondary'"
          >
            <i :class="tab.icon"></i>
            {{ tab.label }}
          </button>
        </div>
      </div>

      <section v-if="activeTab === 'org-members'" class="space-y-6">
        <header class="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
          <div>
            <h1 class="text-3xl font-bold text-phisward-primary">Employee Directory</h1>
            <p class="text-gray-600">
              Maintain the list of employees that belong to your organization.
            </p>
          </div>
          <button
            @click="showCreateMemberModal = true"
            class="self-start lg:self-auto px-6 py-3 bg-gradient-to-r from-phisward-secondary to-phisward-third text-white rounded-lg font-semibold shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 transition-all duration-300"
          >
            <i class="fas fa-user-plus mr-2"></i>
            Add Employee
          </button>
        </header>

        <div v-if="membersError" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg flex items-center gap-2">
          <i class="fas fa-exclamation-triangle"></i>
          <span>{{ membersError }}</span>
        </div>

        <div
          v-if="membersLoading"
          class="flex items-center justify-center py-16 bg-white rounded-2xl shadow"
        >
          <i class="fas fa-spinner fa-spin text-3xl text-phisward-secondary"></i>
        </div>

        <div
          v-else-if="members.length === 0"
          class="flex flex-col items-center justify-center py-16 bg-white rounded-2xl shadow text-center space-y-4"
        >
          <div class="w-16 h-16 rounded-full bg-phisward-fourth/50 flex items-center justify-center">
            <i class="fas fa-users text-2xl text-phisward-secondary"></i>
          </div>
          <div>
            <h2 class="text-xl font-semibold text-phisward-primary">No employees yet</h2>
            <p class="text-gray-600">Start by adding your first employee to keep the directory up to date.</p>
          </div>
        </div>

        <div v-else class="bg-white rounded-2xl shadow divide-y divide-gray-100">
          <article
            v-for="member in members"
            :key="member.id"
            class="px-6 py-5 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4"
          >
            <div>
              <h3 class="text-lg font-semibold text-gray-900">
                {{ member.first_name }} {{ member.last_name }}
              </h3>
              <p class="text-sm text-gray-600">{{ member.email }}</p>
              <p class="text-xs text-gray-400 mt-1">
                Added {{ formatDate(member.created_at) }}
              </p>
            </div>
            <button
              @click="deleteOrgMember(member.id)"
              class="self-start sm:self-auto px-4 py-2 border border-red-200 text-red-600 rounded-lg font-semibold hover:bg-red-50 transition-all duration-200 disabled:opacity-50"
              :disabled="deletingMemberId === member.id"
            >
              <span v-if="deletingMemberId !== member.id">
                <i class="fas fa-trash-alt mr-2"></i>
                Remove
              </span>
              <span v-else>
                <i class="fas fa-spinner fa-spin mr-2"></i>
                Removing...
              </span>
            </button>
          </article>
        </div>
      </section>

      <section v-else-if="activeTab === 'org-users'" class="space-y-6">
        <header class="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
          <div>
            <h1 class="text-3xl font-bold text-phisward-primary">User Accounts</h1>
            <p class="text-gray-600">
              Create and manage login accounts (role <span class="font-semibold">MEMBER</span>) for your employees.
            </p>
          </div>
          <button
            @click="showCreateUserModal = true"
            class="self-start lg:self-auto px-6 py-3 bg-gradient-to-r from-phisward-secondary to-phisward-third text-white rounded-lg font-semibold shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 transition-all duration-300"
          >
            <i class="fas fa-user-plus mr-2"></i>
            Create User
          </button>
        </header>

        <div v-if="usersError" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg flex items-center gap-2">
          <i class="fas fa-exclamation-triangle"></i>
          <span>{{ usersError }}</span>
        </div>

        <div
          v-if="usersLoading"
          class="flex items-center justify-center py-16 bg-white rounded-2xl shadow"
        >
          <i class="fas fa-spinner fa-spin text-3xl text-phisward-secondary"></i>
        </div>

        <div
          v-else-if="users.length === 0"
          class="flex flex-col items-center justify-center py-16 bg-white rounded-2xl shadow text-center space-y-4"
        >
          <div class="w-16 h-16 rounded-full bg-phisward-fourth/50 flex items-center justify-center">
            <i class="fas fa-user-friends text-2xl text-phisward-secondary"></i>
          </div>
          <div>
            <h2 class="text-xl font-semibold text-phisward-primary">No users yet</h2>
            <p class="text-gray-600">Create user accounts so your employees can log in to the platform.</p>
          </div>
        </div>

        <div v-else class="bg-white rounded-2xl shadow divide-y divide-gray-100">
          <article
            v-for="user in users"
            :key="user.id"
            class="px-6 py-5 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4"
          >
            <div>
              <h3 class="text-lg font-semibold text-gray-900">
                {{ user.first_name }} {{ user.last_name }}
              </h3>
              <p class="text-sm text-gray-600">{{ user.email }}</p>
              <div class="flex flex-wrap items-center gap-4 mt-2 text-xs text-gray-500">
                <span class="inline-flex items-center gap-1">
                  <i class="fas fa-id-badge"></i>
                  {{ user.role }}
                </span>
                <span class="inline-flex items-center gap-1">
                  <i class="fas fa-coins"></i>
                  {{ user.credits }} credits
                </span>
                <span class="inline-flex items-center gap-1">
                  <i class="fas fa-clock"></i>
                  Joined {{ formatDate(user.created_at) }}
                </span>
              </div>
            </div>
            <button
              @click="deleteOrgUser(user.id)"
              class="self-start sm:self-auto px-4 py-2 border border-red-200 text-red-600 rounded-lg font-semibold hover:bg-red-50 transition-all duration-200 disabled:opacity-50"
              :disabled="deletingUserId === user.id"
            >
              <span v-if="deletingUserId !== user.id">
                <i class="fas fa-user-minus mr-2"></i>
                Delete
              </span>
              <span v-else>
                <i class="fas fa-spinner fa-spin mr-2"></i>
                Deleting...
              </span>
            </button>
          </article>
        </div>
      </section>

      <section v-else class="bg-white rounded-2xl shadow p-10 text-center">
        <h2 class="text-2xl font-semibold text-phisward-primary mb-3">Welcome back!</h2>
        <p class="text-gray-600">
          Use the navigation to access your employee directory or user accounts.
        </p>
      </section>
    </div>

    <CreateOrgMemberModal
      v-if="showCreateMemberModal"
      @close="showCreateMemberModal = false"
      @created="onMemberCreated"
    />

    <CreateOrgUserModal
      v-if="showCreateUserModal"
      @close="showCreateUserModal = false"
      @created="onUserCreated"
    />
  </DashboardLayout>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import DashboardLayout from '@/components/dashboard/DashboardLayout.vue'
import CreateOrgMemberModal from '@/components/dashboard/orgadmin/CreateOrgMemberModal.vue'
import CreateOrgUserModal from '@/components/dashboard/orgadmin/CreateOrgUserModal.vue'

defineProps({
  role: {
    type: String,
    required: true
  }
})

const route = useRoute()
const router = useRouter()

const validTabs = ['org-members', 'org-users']

const showCreateMemberModal = ref(false)
const showCreateUserModal = ref(false)

const members = ref([])
const membersLoading = ref(false)
const membersError = ref('')
const deletingMemberId = ref('')

const users = ref([])
const usersLoading = ref(false)
const usersError = ref('')
const deletingUserId = ref('')

const tabOptions = [
  {
    key: 'org-members',
    label: 'Employee Directory',
    icon: 'fas fa-address-book'
  },
  {
    key: 'org-users',
    label: 'User Accounts',
    icon: 'fas fa-user-friends'
  }
]

const activeTab = computed(() => {
  const tab = route.query.tab
  if (typeof tab === 'string' && validTabs.includes(tab)) {
    return tab
  }
  return 'org-members'
})

watch(
  () => route.query.tab,
  (tab) => {
    if (typeof tab !== 'string' || !validTabs.includes(tab)) {
      router.replace({ name: 'dashboard', query: { tab: 'org-members' } })
    }
  },
  { immediate: true }
)

const navigateToTab = (tabKey) => {
  if (!validTabs.includes(tabKey)) {
    return
  }
  if (activeTab.value === tabKey) {
    return
  }
  router.replace({ name: 'dashboard', query: { ...route.query, tab: tabKey } })
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
    if (typeof data?.message === 'string') {
      return data.message
    }
  } catch (err) {
    // ignore json parsing issues
  }
  return fallback
}

const fetchOrgMembers = async () => {
  membersLoading.value = true
  membersError.value = ''
  try {
    const token = localStorage.getItem('user_jwt_token')
    if (!token) {
      throw new Error('Authentication token is missing. Please log in again.')
    }

    const response = await fetch('/api/authentication/orgadmin/members', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })

    if (!response.ok) {
      const message = await extractErrorMessage(response, 'Failed to retrieve organization employees.')
      throw new Error(message)
    }

    members.value = await response.json()
  } catch (error) {
    membersError.value = error.message || 'Failed to retrieve organization employees.'
    members.value = []
  } finally {
    membersLoading.value = false
  }
}

const fetchOrgUsers = async () => {
  usersLoading.value = true
  usersError.value = ''
  try {
    const token = localStorage.getItem('user_jwt_token')
    if (!token) {
      throw new Error('Authentication token is missing. Please log in again.')
    }

    const response = await fetch('/api/authentication/orgadmin/users', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })

    if (!response.ok) {
      const message = await extractErrorMessage(response, 'Failed to retrieve organization users.')
      throw new Error(message)
    }

    users.value = await response.json()
  } catch (error) {
    usersError.value = error.message || 'Failed to retrieve organization users.'
    users.value = []
  } finally {
    usersLoading.value = false
  }
}

const deleteOrgMember = async (memberId) => {
  if (!window.confirm('Remove this employee from your organization directory?')) {
    return
  }

  deletingMemberId.value = memberId
  membersError.value = ''

  try {
    const token = localStorage.getItem('user_jwt_token')
    if (!token) {
      throw new Error('Authentication token is missing. Please log in again.')
    }

    const response = await fetch(`/api/authentication/orgadmin/member?member_id=${memberId}`, {
      method: 'DELETE',
      headers: {
        Authorization: `Bearer ${token}`
      }
    })

    if (!response.ok) {
      const message = await extractErrorMessage(response, 'Failed to remove employee.')
      throw new Error(message)
    }

    await fetchOrgMembers()
  } catch (error) {
    membersError.value = error.message || 'Failed to remove employee.'
  } finally {
    deletingMemberId.value = ''
  }
}

const deleteOrgUser = async (userId) => {
  if (!window.confirm('Delete this user account? This action cannot be undone.')) {
    return
  }

  deletingUserId.value = userId
  usersError.value = ''

  try {
    const token = localStorage.getItem('user_jwt_token')
    if (!token) {
      throw new Error('Authentication token is missing. Please log in again.')
    }

    const response = await fetch(`/api/authentication/orgadmin/user?user_id=${userId}`, {
      method: 'DELETE',
      headers: {
        Authorization: `Bearer ${token}`
      }
    })

    if (!response.ok) {
      const message = await extractErrorMessage(response, 'Failed to delete user.')
      throw new Error(message)
    }

    await fetchOrgUsers()
  } catch (error) {
    usersError.value = error.message || 'Failed to delete user.'
  } finally {
    deletingUserId.value = ''
  }
}

const onMemberCreated = () => {
  showCreateMemberModal.value = false
  fetchOrgMembers()
}

const onUserCreated = () => {
  showCreateUserModal.value = false
  fetchOrgUsers()
}

watch(
  activeTab,
  (tab) => {
    if (tab === 'org-members') {
      fetchOrgMembers()
    } else if (tab === 'org-users') {
      fetchOrgUsers()
    }
  },
  { immediate: true }
)

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
