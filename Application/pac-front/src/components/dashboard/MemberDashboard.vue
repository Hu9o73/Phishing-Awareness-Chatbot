<template>
  <DashboardLayout :role="role">
    <div class="text-center py-20">
      <div class="inline-flex items-center justify-center w-24 h-24 bg-gradient-to-r from-phisward-secondary to-phisward-third rounded-full mb-6">
        <i class="fas fa-user-shield text-white text-4xl"></i>
      </div>
      <h1 class="text-4xl font-bold text-phisward-primary mb-4">Member Dashboard</h1>
      <p class="text-xl text-gray-600 max-w-2xl mx-auto">
        Welcome to your personal security training dashboard. Features coming soon!
      </p>
    </div>
  </DashboardLayout>
</template>

<script setup>
import DashboardLayout from '@/components/dashboard/DashboardLayout.vue'

defineProps({
  role: {
    type: String,
    required: true
  }
})
</script>
