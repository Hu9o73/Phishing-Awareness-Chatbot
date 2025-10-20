<template>
  <div class="min-h-screen bg-phisward-fourth/30">
    <Navbar />
    
    <div>
      <DashboardNavbar :role="role" />
      
      <div class="container mx-auto px-6 py-8">
        <slot />
      </div>
    </div>
  </div>
</template>

<script setup>
import Navbar from '@/components/Navbar.vue'
import DashboardNavbar from '@/components/dashboard/DashboardNavbar.vue'

defineProps({
  role: {
    type: String,
    required: true
  }
})
</script>
