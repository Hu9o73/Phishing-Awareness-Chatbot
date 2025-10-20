<template>
  <DashboardLayout :role="role">
    <div class="space-y-6">
      <div class="flex items-center justify-between">
        <h1 class="text-3xl font-bold text-phisward-primary">Company Management</h1>
        <button
          @click="showCreateCompanyModal = true"
          class="px-6 py-3 bg-gradient-to-r from-phisward-secondary to-phisward-third text-white rounded-lg font-semibold shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 transition-all duration-300"
        >
          <i class="fas fa-plus mr-2"></i>
          Create Company
        </button>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <CompanyList
          :companies="companies"
          :loading="loadingCompanies"
          :selected-company="selectedCompany"
          @select="selectCompany"
          @delete="deleteCompany"
        />

        <OrgAdminList
          :org-admins="orgAdmins"
          :loading="loadingOrgAdmins"
          :selected-company="selectedCompany"
          @create="showCreateOrgAdminModal = true"
          @delete="deleteOrgAdmin"
        />
      </div>
    </div>

    <CreateCompanyModal
      v-if="showCreateCompanyModal"
      @close="showCreateCompanyModal = false"
      @created="onCompanyCreated"
    />

    <CreateOrgAdminModal
      v-if="showCreateOrgAdminModal"
      :organization-id="selectedCompany?.id"
      @close="showCreateOrgAdminModal = false"
      @created="onOrgAdminCreated"
    />
  </DashboardLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import DashboardLayout from '@/components/dashboard/DashboardLayout.vue'
import CompanyList from '@/components/dashboard/admin/CompanyList.vue'
import OrgAdminList from '@/components/dashboard/admin/OrgAdminList.vue'
import CreateCompanyModal from '@/components/dashboard/admin/CreateCompanyModal.vue'
import CreateOrgAdminModal from '@/components/dashboard/admin/CreateOrgAdminModal.vue'

defineProps({
  role: {
    type: String,
    required: true
  }
})

const companies = ref([])
const orgAdmins = ref([])
const selectedCompany = ref(null)
const loadingCompanies = ref(false)
const loadingOrgAdmins = ref(false)
const showCreateCompanyModal = ref(false)
const showCreateOrgAdminModal = ref(false)

const fetchCompanies = async () => {
  loadingCompanies.value = true
  try {
    const token = localStorage.getItem('user_jwt_token')
    const response = await fetch('/api/authentication/admin/organizations', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })

    if (response.ok) {
      companies.value = await response.json()
    }
  } catch (err) {
    console.error('Error fetching companies:', err)
  } finally {
    loadingCompanies.value = false
  }
}

const fetchOrgAdmins = async () => {
  if (!selectedCompany.value) {
    orgAdmins.value = []
    return
  }

  loadingOrgAdmins.value = true
  try {
    const token = localStorage.getItem('user_jwt_token')
    const response = await fetch(`/api/authentication/admin/user/orgadmins?organization_id=${selectedCompany.value.id}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })

    if (response.ok) {
      orgAdmins.value = await response.json()
    } else {
      orgAdmins.value = []
    }
  } catch (err) {
    console.error('Error fetching org admins:', err)
    orgAdmins.value = []
  } finally {
    loadingOrgAdmins.value = false
  }
}

const selectCompany = (company) => {
  selectedCompany.value = company
  fetchOrgAdmins()
}

const deleteCompany = async (companyId) => {
  if (!confirm('Are you sure you want to delete this company? This will also delete all associated org admins and users.')) {
    return
  }

  try {
    const token = localStorage.getItem('user_jwt_token')
    const response = await fetch(`/api/authentication/admin/organization?organization_id=${companyId}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })

    if (response.ok) {
      if (selectedCompany.value?.id === companyId) {
        selectedCompany.value = null
        orgAdmins.value = []
      }
      await fetchCompanies()
    }
  } catch (err) {
    console.error('Error deleting company:', err)
  }
}

const deleteOrgAdmin = async (userId) => {
  if (!confirm('Are you sure you want to delete this org admin?')) {
    return
  }

  try {
    const token = localStorage.getItem('user_jwt_token')
    const response = await fetch(`/api/authentication/admin/user?user_id=${userId}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })

    if (response.ok) {
      await fetchOrgAdmins()
    }
  } catch (err) {
    console.error('Error deleting org admin:', err)
  }
}

const onCompanyCreated = () => {
  showCreateCompanyModal.value = false
  fetchCompanies()
}

const onOrgAdminCreated = () => {
  showCreateOrgAdminModal.value = false
  fetchOrgAdmins()
}

onMounted(() => {
  fetchCompanies()
})
</script>
