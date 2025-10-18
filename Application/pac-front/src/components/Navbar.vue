<template>
    <div class="sticky top-0 z-60 bg-white/95 backdrop-blur-lg border-b border-gray-200/50 shadow-lg">
        <div class="relative overflow-hidden">
            <!-- Subtle background gradient -->
            <div class="absolute inset-0 bg-gradient-to-r from-phisward-primary/5 via-transparent to-phisward-secondary/5"></div>

            <nav class="relative container mx-auto px-6 py-4">
                <div class="flex flex-col lg:flex-row w-full justify-between items-center">

                    <!-- Logo Section -->
                    <div class="flex items-center w-full lg:w-auto justify-between">
                        <div class="flex items-center gap-4 group cursor-pointer" @click="$router.push('/')">
                            <!-- Logo -->
                            <div class="relative">
                                <div class="absolute inset-0 bg-phisward-secondary/20 rounded-lg blur-md opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                                <img
                                    class="relative w-12 h-12 transform group-hover:scale-105 transition-all duration-300"
                                    src="../assets/logos/logo.png"
                                    alt="Phish Ward Logo"
                                >
                            </div>

                            <!-- Brand Name -->
                            <div class="flex flex-col">
                                <h1 class="text-2xl md:text-3xl font-bold text-phisward-primary group-hover:text-phisward-secondary transition-colors duration-300">
                                    Phish Ward
                                </h1>
                                <div class="text-xs text-gray-600 font-medium">
                                    Enterprise Security Training
                                </div>
                            </div>
                        </div>

                        <!-- Mobile menu button -->
                        <button
                            @click="toggleMobileMenu"
                            class="lg:hidden relative w-10 h-10 rounded-lg bg-phisward-primary text-white flex items-center justify-center hover:bg-phisward-secondary transform transition-all duration-300 shadow-md cursor-pointer"
                        >
                            <div class="space-y-1.5">
                                <div class="w-5 h-0.5 bg-white transition-all duration-300" :class="{ 'rotate-45 translate-y-2': mobileMenuOpen }"></div>
                                <div class="w-5 h-0.5 bg-white transition-all duration-300" :class="{ 'opacity-0': mobileMenuOpen }"></div>
                                <div class="w-5 h-0.5 bg-white transition-all duration-300" :class="{ '-rotate-45 -translate-y-2': mobileMenuOpen }"></div>
                            </div>
                        </button>
                    </div>

                    <!-- Desktop menu -->
                    <div class="hidden lg:flex items-center gap-8">
                        <!-- Navigation Links -->
                        <div class="flex items-center gap-6">
                            <button
                                @click="$router.push('/features')"
                                class="relative group px-4 py-2 text-gray-700 hover:text-phisward-primary font-semibold transition-all duration-300 cursor-pointer"
                            >
                                <span class="relative z-10 flex items-center gap-2">
                                    <i class="fas fa-shield-alt text-sm"></i>
                                    Features
                                </span>
                                <div class="absolute bottom-0 left-1/2 w-0 h-0.5 bg-phisward-secondary group-hover:w-full group-hover:left-0 transition-all duration-300"></div>
                            </button>

                            <button
                                @click="$router.push('/pricing')"
                                class="relative group px-4 py-2 text-gray-700 hover:text-phisward-primary font-semibold transition-all duration-300 cursor-pointer"
                            >
                                <span class="relative z-10 flex items-center gap-2">
                                    <i class="fas fa-tag text-sm"></i>
                                    Pricing
                                </span>
                                <div class="absolute bottom-0 left-1/2 w-0 h-0.5 bg-phisward-secondary group-hover:w-full group-hover:left-0 transition-all duration-300"></div>
                            </button>

                            <button
                                @click="$router.push('/about')"
                                class="relative group px-4 py-2 text-gray-700 hover:text-phisward-primary font-semibold transition-all duration-300 cursor-pointer"
                            >
                                <span class="relative z-10 flex items-center gap-2">
                                    <i class="fas fa-info-circle text-sm"></i>
                                    About
                                </span>
                                <div class="absolute bottom-0 left-1/2 w-0 h-0.5 bg-phisward-secondary group-hover:w-full group-hover:left-0 transition-all duration-300"></div>
                            </button>
                        </div>

                        <!-- Divider -->
                        <div class="h-8 w-px bg-gray-300"></div>

                        <!-- Auth Buttons -->
                        <div class="flex items-center gap-3">
                            <!-- Login Button -->
                            <button
                                v-if="!logged_in"
                                @click="$router.push('/login')"
                                class="group relative px-6 py-2.5 border-2 border-phisward-primary text-phisward-primary rounded-lg font-semibold hover:bg-phisward-primary hover:text-white transition-all duration-300 cursor-pointer"
                            >
                                <span class="relative z-10 flex items-center gap-2">
                                    <i class="fas fa-sign-in-alt text-sm"></i>
                                    Log In
                                </span>
                            </button>
                            
                            <!-- Logout Button -->
                            <button
                                v-else
                                @click="logout"
                                class="group relative px-6 py-2.5 border-2 border-red-500 text-red-600 rounded-lg font-semibold hover:bg-red-500 hover:text-white transition-all duration-300 cursor-pointer"
                            >
                                <span class="relative z-10 flex items-center gap-2">
                                    <i class="fas fa-sign-out-alt text-sm"></i>
                                    Log Out
                                </span>
                            </button>

                            <!-- Sign Up / Access App Button -->
                            <button
                                v-if="!logged_in"
                                @click="$router.push('/signup')"
                                class="group relative px-6 py-2.5 bg-phisward-primary text-white rounded-lg font-semibold shadow-lg hover:bg-phisward-secondary hover:shadow-xl transform hover:-translate-y-0.5 transition-all duration-300 cursor-pointer"
                            >
                                <span class="relative z-10 flex items-center gap-2">
                                    Get Started
                                    <i class="fas fa-arrow-right text-sm transform group-hover:translate-x-1 transition-transform duration-300"></i>
                                </span>
                            </button>
                            <button
                                v-else
                                @click="$router.push('/app/dashboard')"
                                class="group relative px-6 py-2.5 bg-phisward-secondary text-white rounded-lg font-semibold shadow-lg hover:bg-phisward-primary hover:shadow-xl transform hover:-translate-y-0.5 transition-all duration-300 cursor-pointer"
                            >
                                <span class="relative z-10 flex items-center gap-2">
                                    <i class="fas fa-th-large text-sm"></i>
                                    Access App
                                </span>
                            </button>
                        </div>
                    </div>
                </div>

                <!-- Mobile menu -->
                <div
                    class="lg:hidden overflow-hidden transition-all duration-500 ease-out"
                    :class="mobileMenuOpen ? 'max-h-96 opacity-100 mt-6' : 'max-h-0 opacity-0 mt-0'"
                >
                    <div class="bg-white/90 backdrop-blur-lg rounded-xl border border-gray-200 shadow-xl p-6 space-y-4">
                        <!-- Mobile Navigation Links -->
                        <div class="space-y-3">
                            <button
                                @click="$router.push('/features'); toggleMobileMenu()"
                                class="w-full group flex items-center justify-between p-4 rounded-lg hover:bg-phisward-fourth transition-all duration-300 cursor-pointer"
                            >
                                <div class="flex items-center gap-3">
                                    <div class="w-10 h-10 bg-phisward-primary rounded-lg flex items-center justify-center">
                                        <i class="fas fa-shield-alt text-white"></i>
                                    </div>
                                    <span class="font-semibold text-gray-700">Features</span>
                                </div>
                                <i class="fas fa-chevron-right text-gray-400"></i>
                            </button>

                            <button
                                @click="$router.push('/pricing'); toggleMobileMenu()"
                                class="w-full group flex items-center justify-between p-4 rounded-lg hover:bg-phisward-fourth transition-all duration-300 cursor-pointer"
                            >
                                <div class="flex items-center gap-3">
                                    <div class="w-10 h-10 bg-phisward-secondary rounded-lg flex items-center justify-center">
                                        <i class="fas fa-tag text-white"></i>
                                    </div>
                                    <span class="font-semibold text-gray-700">Pricing</span>
                                </div>
                                <i class="fas fa-chevron-right text-gray-400"></i>
                            </button>

                            <button
                                @click="$router.push('/about'); toggleMobileMenu()"
                                class="w-full group flex items-center justify-between p-4 rounded-lg hover:bg-phisward-fourth transition-all duration-300 cursor-pointer"
                            >
                                <div class="flex items-center gap-3">
                                    <div class="w-10 h-10 bg-phisward-third rounded-lg flex items-center justify-center">
                                        <i class="fas fa-info-circle text-white"></i>
                                    </div>
                                    <span class="font-semibold text-gray-700">About</span>
                                </div>
                                <i class="fas fa-chevron-right text-gray-400"></i>
                            </button>
                        </div>

                        <!-- Mobile Auth Buttons -->
                        <div class="pt-4 border-t border-gray-200 space-y-3">
                            <button
                                v-if="!logged_in"
                                @click="$router.push('/login'); toggleMobileMenu()"
                                class="w-full px-6 py-3 border-2 border-phisward-primary text-phisward-primary rounded-lg font-semibold hover:bg-phisward-primary hover:text-white transition-all duration-300 cursor-pointer"
                            >
                                <i class="fas fa-sign-in-alt mr-2"></i>
                                Log In
                            </button>
                            <button
                                v-else
                                @click="logout(); toggleMobileMenu()"
                                class="w-full px-6 py-3 border-2 border-red-500 text-red-600 rounded-lg font-semibold hover:bg-red-500 hover:text-white transition-all duration-300 cursor-pointer"
                            >
                                <i class="fas fa-sign-out-alt mr-2"></i>
                                Log Out
                            </button>

                            <button
                                v-if="!logged_in"
                                @click="$router.push('/signup'); toggleMobileMenu()"
                                class="w-full px-6 py-3 bg-phisward-primary text-white rounded-lg font-semibold shadow-lg hover:bg-phisward-secondary transition-all duration-300 cursor-pointer"
                            >
                                Get Started
                                <i class="fas fa-arrow-right ml-2"></i>
                            </button>
                            <button
                                v-else
                                @click="$router.push('/app/dashboard'); toggleMobileMenu()"
                                class="w-full px-6 py-3 bg-phisward-secondary text-white rounded-lg font-semibold shadow-lg hover:bg-phisward-primary transition-all duration-300 cursor-pointer"
                            >
                                <i class="fas fa-th-large mr-2"></i>
                                Access App
                            </button>
                        </div>
                    </div>
                </div>
            </nav>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const AUTH_API_URL = import.meta.env.VITE_AUTH_API_URL
const logged_in = ref(false)
const mobileMenuOpen = ref(false)

const toggleMobileMenu = () => {
  mobileMenuOpen.value = !mobileMenuOpen.value
}

const logout = () => {
  logged_in.value = false
  localStorage.removeItem('user_jwt_token')
  window.location.href = '/'
}

const getAuthHeaders = () => {
  const token = localStorage.getItem('user_jwt_token')
  return {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  }
}

const verifyToken = async (token) => {
  try {
    const response = await fetch(AUTH_API_URL + '/auth/verifyjwt', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    
    if (response.ok) {
      logged_in.value = true
    } else {
      logged_in.value = false
      localStorage.removeItem('user_jwt_token')
    }
  } catch (error) {
    logged_in.value = false
    localStorage.removeItem('user_jwt_token')
  }
}

onMounted(async () => {
  const token = localStorage.getItem('user_jwt_token')
  if (token) {
    await verifyToken(token)
  }
})
</script>

<style scoped>
.container {
    max-width: 1400px;
}

.backdrop-blur-lg {
    backdrop-filter: blur(16px);
}

html {
    scroll-behavior: smooth;
}
</style>
