<template>
  <div class="bg-white rounded-xl shadow-lg border border-gray-200 p-6">
    <h2 class="text-xl font-bold text-phisward-primary mb-4 flex items-center gap-2">
      <i class="fas fa-building"></i>
      Companies
    </h2>

    <div v-if="loading" class="flex items-center justify-center py-12">
      <i class="fas fa-spinner fa-spin text-3xl text-phisward-secondary"></i>
    </div>

    <div v-else-if="companies.length === 0" class="text-center py-12 text-gray-500">
      <i class="fas fa-building text-4xl mb-4 opacity-50"></i>
      <p>No companies found</p>
    </div>

    <div v-else class="space-y-2 max-h-[600px] overflow-y-auto">
      <div
        v-for="company in companies"
        :key="company.id"
        @click="$emit('select', company)"
        class="p-4 rounded-lg border-2 transition-all duration-200 cursor-pointer"
        :class="selectedCompany?.id === company.id 
          ? 'border-phisward-secondary bg-phisward-secondary/5' 
          : 'border-gray-200 hover:border-phisward-third hover:bg-gray-50'"
      >
        <div class="flex items-center justify-between">
          <div class="flex-1">
            <h3 class="font-semibold text-phisward-primary text-lg">{{ company.name }}</h3>
            <p v-if="company.description" class="text-sm text-gray-600 mt-1">{{ company.description }}</p>
          </div>
          
          <button
            @click.stop="$emit('delete', company.id)"
            class="ml-4 p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
          >
            <i class="fas fa-trash"></i>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  companies: {
    type: Array,
    required: true
  },
  loading: {
    type: Boolean,
    default: false
  },
  selectedCompany: {
    type: Object,
    default: null
  }
})

defineEmits(['select', 'delete'])
</script>
