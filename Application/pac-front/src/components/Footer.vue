<template>
    <footer class="relative overflow-hidden">
        <!-- Background gradient -->
        <div class="absolute inset-0 bg-gradient-to-br from-phisward-primary via-phisward-secondary to-phisward-primary">
            <!-- Subtle pattern overlay -->
            <div class="absolute inset-0 opacity-5" style="background-image: url('data:image/svg+xml,%3Csvg width=\'60\' height=\'60\' viewBox=\'0 0 60 60\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cg fill=\'none\' fill-rule=\'evenodd\'%3E%3Cg fill=\'%23ffffff\' fill-opacity=\'1\'%3E%3Cpath d=\'M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z\'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E');"></div>
        </div>

        <!-- Separator line -->
        <div class="h-px bg-gradient-to-r from-transparent via-white/30 to-transparent"></div>

        <!-- Main footer content -->
        <div class="relative z-10 py-16">
            <div class="container mx-auto px-6">
                <div class="grid grid-cols-1 lg:grid-cols-4 gap-12 mb-12">

                    <!-- Brand Section -->
                    <div class="lg:col-span-2">
                        <div class="flex items-center gap-4 mb-6 group cursor-pointer">
                            <!-- Logo -->
                            <div class="relative">
                                <div class="absolute inset-0 bg-white rounded-lg blur-md opacity-0 group-hover:opacity-50 transition-opacity duration-300"></div>
                                <img
                                    class="relative w-16 h-16 transform group-hover:scale-105 transition-all duration-300 drop-shadow-2xl"
                                    src="../assets/logos/logo.png"
                                    alt="Phish Ward Logo"
                                >
                            </div>

                            <div>
                                <h1 class="text-3xl font-bold text-white mb-1 group-hover:scale-105 transition-transform duration-300">
                                    Phish Ward
                                </h1>
                                <div class="text-white/80 text-sm font-medium">
                                    Enterprise Security Training Platform
                                </div>
                            </div>
                        </div>

                        <p class="text-white/80 text-base leading-relaxed mb-8 max-w-md">
                            Protecting organizations worldwide with AI-powered phishing simulations and comprehensive security awareness training. Build a resilient security culture across your entire organization.
                        </p>

                        <!-- Social Links -->
                        <div class="flex items-center gap-4 mb-8">
                            <h3 class="text-white font-semibold mr-2">Connect:</h3>
                            <div class="flex gap-3">
                                <a href="#" class="group relative w-11 h-11 bg-white/10 backdrop-blur-sm rounded-lg flex items-center justify-center hover:bg-white/20 transition-all duration-300 transform hover:-translate-y-1">
                                    <i class="fab fa-linkedin text-white text-lg group-hover:scale-110 transition-transform duration-300"></i>
                                </a>
                                <a href="#" class="group relative w-11 h-11 bg-white/10 backdrop-blur-sm rounded-lg flex items-center justify-center hover:bg-white/20 transition-all duration-300 transform hover:-translate-y-1">
                                    <i class="fab fa-twitter text-white text-lg group-hover:scale-110 transition-transform duration-300"></i>
                                </a>
                                <a href="#" class="group relative w-11 h-11 bg-white/10 backdrop-blur-sm rounded-lg flex items-center justify-center hover:bg-white/20 transition-all duration-300 transform hover:-translate-y-1">
                                    <i class="fab fa-github text-white text-lg group-hover:scale-110 transition-transform duration-300"></i>
                                </a>
                                <a href="#" class="group relative w-11 h-11 bg-white/10 backdrop-blur-sm rounded-lg flex items-center justify-center hover:bg-white/20 transition-all duration-300 transform hover:-translate-y-1">
                                    <i class="fab fa-youtube text-white text-lg group-hover:scale-110 transition-transform duration-300"></i>
                                </a>
                            </div>
                        </div>

                        <!-- Security Certifications -->
                        <div class="flex items-center gap-4 text-white/60 text-xs">
                            <div class="flex items-center gap-1">
                                <i class="fas fa-shield-alt"></i>
                                <span>SOC 2 Type II</span>
                            </div>
                            <span>•</span>
                            <div class="flex items-center gap-1">
                                <i class="fas fa-certificate"></i>
                                <span>ISO 27001</span>
                            </div>
                            <span>•</span>
                            <div class="flex items-center gap-1">
                                <i class="fas fa-lock"></i>
                                <span>GDPR Compliant</span>
                            </div>
                        </div>
                    </div>

                    <!-- Product Links -->
                    <div>
                        <h3 class="text-xl font-bold text-white mb-6 flex items-center gap-2">
                            <i class="fas fa-shield-alt text-phisward-third"></i>
                            Product
                        </h3>
                        <ul class="space-y-4">
                            <li>
                                <a href="/features" class="group flex items-center gap-3 text-white/80 hover:text-white transition-all duration-300">
                                    <i class="fas fa-chevron-right text-xs opacity-0 group-hover:opacity-100 transform -translate-x-2 group-hover:translate-x-0 transition-all duration-300"></i>
                                    <span class="group-hover:translate-x-2 transition-transform duration-300">Features</span>
                                </a>
                            </li>
                            <li>
                                <a href="/pricing" class="group flex items-center gap-3 text-white/80 hover:text-white transition-all duration-300">
                                    <i class="fas fa-chevron-right text-xs opacity-0 group-hover:opacity-100 transform -translate-x-2 group-hover:translate-x-0 transition-all duration-300"></i>
                                    <span class="group-hover:translate-x-2 transition-transform duration-300">Pricing</span>
                                </a>
                            </li>
                            <li>
                                <a href="/demo" class="group flex items-center gap-3 text-white/80 hover:text-white transition-all duration-300">
                                    <i class="fas fa-chevron-right text-xs opacity-0 group-hover:opacity-100 transform -translate-x-2 group-hover:translate-x-0 transition-all duration-300"></i>
                                    <span class="group-hover:translate-x-2 transition-transform duration-300">Request Demo</span>
                                </a>
                            </li>
                            <li>
                                <a href="/about" class="group flex items-center gap-3 text-white/80 hover:text-white transition-all duration-300">
                                    <i class="fas fa-chevron-right text-xs opacity-0 group-hover:opacity-100 transform -translate-x-2 group-hover:translate-x-0 transition-all duration-300"></i>
                                    <span class="group-hover:translate-x-2 transition-transform duration-300">About Us</span>
                                </a>
                            </li>
                            <li>
                                <a href="/security" class="group flex items-center gap-3 text-white/80 hover:text-white transition-all duration-300">
                                    <i class="fas fa-chevron-right text-xs opacity-0 group-hover:opacity-100 transform -translate-x-2 group-hover:translate-x-0 transition-all duration-300"></i>
                                    <span class="group-hover:translate-x-2 transition-transform duration-300">Security</span>
                                </a>
                            </li>
                        </ul>
                    </div>

                    <!-- Support Links -->
                    <div>
                        <h3 class="text-xl font-bold text-white mb-6 flex items-center gap-2">
                            <i class="fas fa-life-ring text-phisward-third"></i>
                            Support
                        </h3>
                        <ul class="space-y-4">
                            <li>
                                <a href="/documentation" class="group flex items-center gap-3 text-white/80 hover:text-white transition-all duration-300">
                                    <i class="fas fa-chevron-right text-xs opacity-0 group-hover:opacity-100 transform -translate-x-2 group-hover:translate-x-0 transition-all duration-300"></i>
                                    <span class="group-hover:translate-x-2 transition-transform duration-300">Documentation</span>
                                </a>
                            </li>
                            <li>
                                <a href="/help" class="group flex items-center gap-3 text-white/80 hover:text-white transition-all duration-300">
                                    <i class="fas fa-chevron-right text-xs opacity-0 group-hover:opacity-100 transform -translate-x-2 group-hover:translate-x-0 transition-all duration-300"></i>
                                    <span class="group-hover:translate-x-2 transition-transform duration-300">Help Center</span>
                                </a>
                            </li>
                            <li>
                                <a href="/contact" class="group flex items-center gap-3 text-white/80 hover:text-white transition-all duration-300">
                                    <i class="fas fa-chevron-right text-xs opacity-0 group-hover:opacity-100 transform -translate-x-2 group-hover:translate-x-0 transition-all duration-300"></i>
                                    <span class="group-hover:translate-x-2 transition-transform duration-300">Contact Us</span>
                                </a>
                            </li>
                            <li>
                                <a href="/status" class="group flex items-center gap-3 text-white/80 hover:text-white transition-all duration-300">
                                    <i class="fas fa-chevron-right text-xs opacity-0 group-hover:opacity-100 transform -translate-x-2 group-hover:translate-x-0 transition-all duration-300"></i>
                                    <span class="group-hover:translate-x-2 transition-transform duration-300">System Status</span>
                                </a>
                            </li>
                            <li>
                                <a href="/api" class="group flex items-center gap-3 text-white/80 hover:text-white transition-all duration-300">
                                    <i class="fas fa-chevron-right text-xs opacity-0 group-hover:opacity-100 transform -translate-x-2 group-hover:translate-x-0 transition-all duration-300"></i>
                                    <span class="group-hover:translate-x-2 transition-transform duration-300">API Documentation</span>
                                </a>
                            </li>
                        </ul>
                    </div>
                </div>

                <!-- Newsletter Subscription -->
                <div class="mb-12 bg-white/10 backdrop-blur-sm rounded-xl p-8 border border-white/20">
                    <div class="flex flex-col md:flex-row items-center justify-between gap-6">
                        <div class="flex-1 text-center md:text-left">
                            <h3 class="text-2xl font-bold text-white mb-2">Stay Informed</h3>
                            <p class="text-white/80">Get the latest security insights and product updates delivered to your inbox.</p>
                        </div>
                        <div class="flex-1 max-w-md">
                            <div class="flex gap-3">
                                <input
                                    type="email"
                                    placeholder="Enter your email"
                                    class="flex-1 px-4 py-3 rounded-lg bg-white/20 border border-white/30 text-white placeholder-white/60 focus:outline-none focus:border-white/60 transition-colors duration-300"
                                >
                                <button class="px-6 py-3 bg-white text-phisward-primary rounded-lg font-semibold hover:bg-phisward-fourth transition-all duration-300 whitespace-nowrap cursor-pointer">
                                    <i class="fas fa-paper-plane mr-2"></i>
                                    Subscribe
                                </button>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Bottom Section -->
                <div class="flex flex-col md:flex-row items-center justify-between pt-8 border-t border-white/20">
                    <!-- Copyright -->
                    <div class="text-center md:text-left mb-4 md:mb-0">
                        <div class="text-white/80 mb-2">
                            © {{ currentYear }} Phish Ward. All rights reserved.
                        </div>
                        <div class="flex items-center gap-2 text-white/60 text-sm justify-center md:justify-start">
                            <i class="fas fa-code"></i>
                            <span>Developed by</span>
                            <strong class="text-white">Hugo Bonnell</strong>
                        </div>
                    </div>

                    <!-- Legal Links -->
                    <div class="flex flex-wrap items-center justify-center gap-6">
                        <a href="/privacy" class="text-white/70 hover:text-white text-sm transition-colors duration-300">Privacy Policy</a>
                        <span class="text-white/30">•</span>
                        <a href="/terms" class="text-white/70 hover:text-white text-sm transition-colors duration-300">Terms of Service</a>
                        <span class="text-white/30">•</span>
                        <a href="/cookies" class="text-white/70 hover:text-white text-sm transition-colors duration-300">Cookie Policy</a>
                        <span class="text-white/30">•</span>
                        <a href="/compliance" class="text-white/70 hover:text-white text-sm transition-colors duration-300">Compliance</a>
                    </div>
                </div>

                <!-- Trust Indicators -->
                <div class="mt-8 pt-8 border-t border-white/20">
                    <div class="text-center">
                        <h4 class="text-white font-semibold mb-4">Trusted by Enterprise Organizations</h4>
                        <div class="flex flex-wrap items-center justify-center gap-8 opacity-70">
                            <div class="flex items-center gap-2 text-white/70 hover:text-white/90 transition-colors duration-300">
                                <i class="fas fa-shield-alt text-green-400 text-lg"></i>
                                <span class="text-sm">Bank-Grade Encryption</span>
                            </div>
                            <div class="flex items-center gap-2 text-white/70 hover:text-white/90 transition-colors duration-300">
                                <i class="fas fa-cloud text-blue-400 text-lg"></i>
                                <span class="text-sm">Cloud Native</span>
                            </div>
                            <div class="flex items-center gap-2 text-white/70 hover:text-white/90 transition-colors duration-300">
                                <i class="fas fa-clock text-yellow-400 text-lg"></i>
                                <span class="text-sm">99.9% Uptime SLA</span>
                            </div>
                            <div class="flex items-center gap-2 text-white/70 hover:text-white/90 transition-colors duration-300">
                                <i class="fas fa-headset text-purple-400 text-lg"></i>
                                <span class="text-sm">24/7 Support</span>
                            </div>
                            <div class="flex items-center gap-2 text-white/70 hover:text-white/90 transition-colors duration-300">
                                <i class="fas fa-globe text-cyan-400 text-lg"></i>
                                <span class="text-sm">Global Infrastructure</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </footer>
</template>

<script setup>
import { computed } from 'vue'

const currentYear = computed(() => new Date().getFullYear())
</script>

<style scoped>
.container {
    max-width: 1400px;
}

.backdrop-blur-sm {
    backdrop-filter: blur(4px);
}

input:focus {
    outline: none;
}

a, button {
    transition: all 0.3s ease;
}

/* Smooth transitions for all interactive elements */
.group:hover .animate-pulse {
    animation-duration: 0.5s;
}

/* Custom scrollbar */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
    background: #2C5E8A;
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: #102A43;
}
</style>
