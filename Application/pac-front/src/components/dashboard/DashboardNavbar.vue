<template>
  <div class="bg-white border-b border-gray-200 shadow-sm">
    <div class="container mx-auto px-6">
      <nav class="flex space-x-1">
        <template v-if="role === 'ADMIN'">
          <router-link
            to="/app/dashboard"
            class="px-6 py-4 text-gray-700 hover:text-phisward-primary font-semibold border-b-2 transition-all duration-200"
            :class="isActive('/app/dashboard') ? 'border-phisward-primary text-phisward-primary' : 'border-transparent'"
          >
            <i class="fas fa-building mr-2"></i>
            Companies
          </router-link>
        </template>

        <template v-else-if="role === 'ORGADMIN'">
          <router-link
            to="/app/dashboard"
            class="px-6 py-4 text-gray-700 hover:text-phisward-primary font-semibold border-b-2 transition-all duration-200"
            :class="isActive('/app/dashboard') ? 'border-phisward-primary text-phisward-primary' : 'border-transparent'"
          >
            <i class="fas fa-home mr-2"></i>
            Dashboard
          </router-link>
        </template>

        <template v-else-if="role === 'MEMBER'">
          <router-link
            to="/app/dashboard"
            class="px-6 py-4 text-gray-700 hover:text-phisward-primary font-semibold border-b-2 transition-all duration-200"
            :class="isActive('/app/dashboard') ? 'border-phisward-primary text-phisward-primary' : 'border-transparent'"
          >
            <i class="fas fa-home mr-2"></i>
            Dashboard
          </router-link>
        </template>
      </nav>
    </div>
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router'

defineProps({
  role: {
    type: String,
    required: true
  }
})

const route = useRoute()

const isActive = (path) => {
  return route.path === path
}
</script>
