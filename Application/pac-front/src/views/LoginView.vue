<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-phisward-fourth via-white to-phisward-fourth">
    <div class="absolute inset-0 overflow-hidden">
      <div class="absolute top-20 left-10 w-72 h-72 bg-phisward-third/10 rounded-full blur-3xl"></div>
      <div class="absolute bottom-20 right-10 w-96 h-96 bg-phisward-secondary/10 rounded-full blur-3xl"></div>
    </div>

    <div class="relative z-10 w-full max-w-md px-6">
      <div class="bg-white rounded-2xl shadow-2xl p-8 border border-gray-100">
        <div class="text-center mb-8">
          <div class="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r from-phisward-secondary to-phisward-third rounded-xl mb-4">
            <i class="fas fa-shield-alt text-white text-2xl"></i>
          </div>
          <h1 class="text-3xl font-bold text-phisward-primary mb-2">Welcome Back</h1>
          <p class="text-gray-600">Sign in to access your dashboard</p>
        </div>

        <form @submit.prevent="handleLogin" class="space-y-6">
          <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg flex items-center gap-2">
            <i class="fas fa-exclamation-circle"></i>
            <span>{{ error }}</span>
          </div>

          <div>
            <label for="email" class="block text-sm font-semibold text-gray-700 mb-2">Email Address</label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <i class="fas fa-envelope text-gray-400"></i>
              </div>
              <input
                id="email"
                v-model="email"
                type="email"
                required
                class="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-phisward-secondary focus:border-transparent transition-all"
                placeholder="your@email.com"
              />
            </div>
          </div>

          <div>
            <label for="password" class="block text-sm font-semibold text-gray-700 mb-2">Password</label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <i class="fas fa-lock text-gray-400"></i>
              </div>
              <input
                id="password"
                v-model="password"
                :type="showPassword ? 'text' : 'password'"
                required
                class="w-full pl-10 pr-12 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-phisward-secondary focus:border-transparent transition-all"
                placeholder="••••••••"
              />
              <button
                type="button"
                @click="showPassword = !showPassword"
                class="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-gray-600"
              >
                <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
              </button>
            </div>
          </div>

          <button
            type="submit"
            :disabled="loading"
            class="w-full bg-gradient-to-r from-phisward-secondary to-phisward-third text-white py-3 rounded-lg font-semibold shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="!loading" class="flex items-center justify-center gap-2">
              <i class="fas fa-sign-in-alt"></i>
              Sign In
            </span>
            <span v-else class="flex items-center justify-center gap-2">
              <i class="fas fa-spinner fa-spin"></i>
              Signing In...
            </span>
          </button>
        </form>

        <div class="mt-6 text-center text-sm text-gray-600">
          Protected by enterprise-grade security
          <div class="flex items-center justify-center gap-4 mt-2">
            <i class="fas fa-shield-alt text-phisward-secondary"></i>
            <i class="fas fa-lock text-phisward-secondary"></i>
            <i class="fas fa-certificate text-phisward-secondary"></i>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const email = ref('')
const password = ref('')
const showPassword = ref(false)
const loading = ref(false)
const error = ref('')

const handleLogin = async () => {
  loading.value = true
  error.value = ''

  try {
    const params = new URLSearchParams({
      email: email.value,
      password: password.value
    })

    const response = await fetch(`/api/authentication/auth/login?${params}`, {
      method: 'POST'
    })

    const data = await response.json()

    if (!response.ok) {
      const errorMsg = typeof data.detail === 'string' 
        ? data.detail 
        : 'Login failed. Please check your credentials.'
      throw new Error(errorMsg)
    }

    localStorage.setItem('user_jwt_token', data.access_token)
    
    router.push('/app/dashboard')
  } catch (err) {
    error.value = err.message || 'An error occurred during login'
  } finally {
    loading.value = false
  }
}
</script>
