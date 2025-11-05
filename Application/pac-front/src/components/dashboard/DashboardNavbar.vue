<template>
  <div class="bg-white border-b border-gray-200 shadow-sm">
    <div class="container mx-auto px-6">
      <nav class="flex space-x-1">
        <router-link
          v-for="link in navLinks"
          :key="link.label"
          :to="link.to"
          class="px-6 py-4 text-gray-700 hover:text-phisward-primary font-semibold border-b-2 transition-all duration-200 flex items-center"
          :class="isActive(link) ? 'border-phisward-primary text-phisward-primary' : 'border-transparent'"
        >
          <i :class="`${link.icon} mr-2`"></i>
          {{ link.label }}
        </router-link>
      </nav>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const props = defineProps({
  role: {
    type: String,
    required: true
  }
})

const route = useRoute()
const router = useRouter()

const navLinks = computed(() => {
  switch (props.role) {
    case 'ADMIN':
      return [
        {
          label: 'Companies',
          icon: 'fas fa-building',
          to: { name: 'dashboard', query: { tab: 'companies' } }
        }
      ]
    case 'ORG_ADMIN':
      return [
        {
          label: 'Employee Directory',
          icon: 'fas fa-address-book',
          to: { name: 'dashboard', query: { tab: 'org-members' } }
        },
        {
          label: 'User Accounts',
          icon: 'fas fa-user-friends',
          to: { name: 'dashboard', query: { tab: 'org-users' } }
        }
      ]
    case 'MEMBER':
      return [
        {
          label: 'Organization Directory',
          icon: 'fas fa-users',
          to: { name: 'dashboard', query: { tab: 'org-directory' } }
        },
        {
          label: 'Scenarios',
          icon: 'fas fa-tasks',
          to: { name: 'dashboard', query: { tab: 'scenarios' } }
        },
        {
          label: 'Hook Emails',
          icon: 'fas fa-envelope-open-text',
          to: { name: 'dashboard', query: { tab: 'hook-email' } }
        },
        {
          label: 'Import / Export',
          icon: 'fas fa-file-import',
          to: { name: 'dashboard', query: { tab: 'import-export' } }
        }
      ]
    default:
      return [
        {
          label: 'Dashboard',
          icon: 'fas fa-home',
          to: { name: 'dashboard' }
        }
      ]
  }
})

const isActive = (link) => {
  const resolved = router.resolve(link.to)

  if (resolved.route.path !== route.path) {
    return false
  }

  const targetQuery = resolved.route.query || {}
  const currentQuery = route.query || {}

  return Object.entries(targetQuery).every(([key, value]) => currentQuery[key] === value)
}
</script>
