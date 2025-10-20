<template>
  <div class="bg-white rounded-xl shadow-lg border border-gray-200 p-6">
    <div class="flex items-center justify-between mb-4">
      <h2 class="text-xl font-bold text-phisward-primary flex items-center gap-2">
        <i class="fas fa-user-tie"></i>
        Organization Admins
      </h2>
      
      <button
        v-if="selectedCompany"
        @click="$emit('create')"
        class="px-4 py-2 bg-phisward-secondary text-white rounded-lg font-semibold hover:bg-phisward-primary transition-all duration-200"
      >
        <i class="fas fa-plus mr-1"></i>
        Add Admin
      </button>
    </div>

    <div v-if="!selectedCompany" class="text-center py-12 text-gray-500">
      <i class="fas fa-arrow-left text-4xl mb-4 opacity-50"></i>
      <p>Select a company to view its admins</p>
    </div>

    <div v-else-if="loading" class="flex items-center justify-center py-12">
      <i class="fas fa-spinner fa-spin text-3xl text-phisward-secondary"></i>
    </div>

    <div v-else-if="orgAdmins.length === 0" class="text-center py-12 text-gray-500">
      <i class="fas fa-user-slash text-4xl mb-4 opacity-50"></i>
      <p>No admins found for this company</p>
    </div>

    <div v-else class="space-y-3 max-h-[600px] overflow-y-auto">
      <div
        v-for="admin in orgAdmins"
        :key="admin.id"
        class="p-4 rounded-lg border border-gray-200 hover:border-phisward-third hover:bg-gray-50 transition-all duration-200"
      >
        <div class="flex items-start justify-between">
          <div class="flex-1">
            <div class="flex items-center gap-2 mb-2">
              <div class="w-10 h-10 rounded-full bg-gradient-to-r from-phisward-secondary to-phisward-third flex items-center justify-center text-white font-semibold">
                {{ admin.first_name[0] }}{{ admin.last_name[0] }}
              </div>
              <div>
                <h3 class="font-semibold text-phisward-primary">
                  {{ admin.first_name }} {{ admin.last_name }}
                </h3>
                <p class="text-sm text-gray-600">{{ admin.email }}</p>
              </div>
            </div>
            
            <div class="flex items-center gap-4 mt-3 text-xs">
              <span class="text-gray-500">
                <i class="fas fa-user-shield mr-1"></i>
                {{ admin.role }}
              </span>
              
              <span class="text-gray-500">
                <i class="fas fa-coins mr-1"></i>
                {{ admin.credits }} credits
              </span>
            </div>
          </div>
          
          <button
            @click="$emit('delete', admin.id)"
            class="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
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
  orgAdmins: {
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

defineEmits(['create', 'delete'])
</script>
