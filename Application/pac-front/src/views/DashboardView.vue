<template>
  <div>
    <div v-if="loading" class="min-h-screen flex items-center justify-center bg-phisward-fourth/30">
      <div class="text-center">
        <i class="fas fa-spinner fa-spin text-5xl text-phisward-secondary mb-4"></i>
        <p class="text-xl text-gray-600">Loading dashboard...</p>
      </div>
    </div>

    <AdminDashboard v-else-if="userRole === 'ADMIN'" :role="userRole" />
    <OrgAdminDashboard v-else-if="userRole === 'ORG_ADMIN'" :role="userRole" />
    <MemberDashboard v-else-if="userRole === 'MEMBER'" :role="userRole" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import AdminDashboard from '@/components/dashboard/admin/AdminDashboard.vue'
import OrgAdminDashboard from '@/components/dashboard/OrgAdminDashboard.vue'
import MemberDashboard from '@/components/dashboard/MemberDashboard.vue'

const router = useRouter()
const route = useRoute()
const userRole = ref('')
const loading = ref(true)

const ensureDefaultTab = (role) => {
  if (route.name !== 'dashboard') {
    return
  }

  if (route.query.tab) {
    return
  }

  if (role === 'ADMIN') {
    router.replace({ name: 'dashboard', query: { tab: 'companies' } })
  } else if (role === 'ORG_ADMIN') {
    router.replace({ name: 'dashboard', query: { tab: 'org-members' } })
  } else if (role === 'MEMBER') {
    router.replace({ name: 'dashboard', query: { tab: 'scenarios' } })
  }
}

onMounted(async () => {
  const token = localStorage.getItem('user_jwt_token')
  
  if (!token) {
    router.push('/login')
    return
  }

  try {
    const response = await fetch('/api/authentication/auth/user', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })

    if (!response.ok) {
      localStorage.removeItem('user_jwt_token')
      router.push('/login')
      return
    }

    const userData = await response.json()
    userRole.value = userData.role
    ensureDefaultTab(userData.role)
  } catch (err) {
    console.error('Error fetching user data:', err)
    router.push('/login')
  } finally {
    loading.value = false
  }
})
</script>
