<template>
    <div class="relative min-h-screen flex items-center justify-center overflow-hidden bg-gradient-to-br from-phisward-fourth via-white to-phisward-fourth">
        <!-- Animated Background Elements -->
        <div class="absolute inset-0 overflow-hidden">
            <!-- Floating security elements -->
            <div class="absolute top-20 left-10 w-72 h-72 bg-phisward-third/10 rounded-full blur-3xl animate-float-slow"></div>
            <div class="absolute bottom-20 right-10 w-96 h-96 bg-phisward-secondary/10 rounded-full blur-3xl animate-float-slower"></div>
            
            <!-- Animated Icons -->
            <div class="absolute top-32 right-1/4 text-phisward-secondary/20 animate-float">
                <i class="fas fa-shield-alt text-6xl"></i>
            </div>
            <div class="absolute bottom-32 left-1/4 text-phisward-third/20 animate-float-slow">
                <i class="fas fa-lock text-5xl"></i>
            </div>
            <div class="absolute top-1/4 left-20 text-phisward-primary/15 animate-float-slower">
                <i class="fas fa-user-shield text-4xl"></i>
            </div>
        </div>

        <!-- Main Content -->
        <div class="container mx-auto px-6 relative z-10 py-20">
            <div class="flex flex-col lg:flex-row items-center gap-16">

                <!-- Left Content -->
                <div class="flex-1 text-center lg:text-left">
                    <!-- Security Badge -->
                    <div class="inline-flex items-center gap-2 bg-phisward-primary/10 border border-phisward-primary/20 rounded-full px-6 py-3 mb-8 animate-fade-in-up">
                        <div class="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
                        <span class="text-phisward-primary font-semibold">Enterprise-Grade Security Training</span>
                    </div>

                    <!-- Main Title -->
                    <h1 class="text-5xl md:text-6xl lg:text-7xl font-bold mb-6 animate-fade-in-up animation-delay-200">
                        <span class="text-phisward-primary leading-tight">
                            Protect Your Team From
                        </span>
                        <br />
                        <span class="bg-gradient-to-r from-phisward-secondary to-phisward-third bg-clip-text text-transparent leading-tight">
                            Phishing Attacks
                        </span>
                    </h1>

                    <!-- Subtitle -->
                    <p class="text-xl md:text-2xl text-gray-600 mb-8 max-w-2xl animate-fade-in-up animation-delay-400">
                        Advanced AI-powered simulations that train your employees to identify and prevent phishing threats across all communication channels.
                    </p>

                    <!-- Key Value Props -->
                    <div class="flex flex-col sm:flex-row gap-4 mb-12 animate-fade-in-up animation-delay-600">
                        <div class="flex items-center gap-2 text-gray-700">
                            <i class="fas fa-check-circle text-green-500 text-xl"></i>
                            <span class="font-medium">Multi-Channel Simulations</span>
                        </div>
                        <div class="flex items-center gap-2 text-gray-700">
                            <i class="fas fa-check-circle text-green-500 text-xl"></i>
                            <span class="font-medium">AI-Powered Personalization</span>
                        </div>
                        <div class="flex items-center gap-2 text-gray-700">
                            <i class="fas fa-check-circle text-green-500 text-xl"></i>
                            <span class="font-medium">Real-Time Analytics</span>
                        </div>
                    </div>

                    <!-- CTA Buttons -->
                    <div class="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start mb-12 animate-fade-in-up animation-delay-800">
                        <button 
                            class="group px-8 py-4 bg-phisward-primary text-white rounded-lg font-semibold text-lg shadow-lg hover:bg-phisward-secondary hover:shadow-xl transform hover:-translate-y-1 transition-all duration-300 flex items-center justify-center gap-3 cursor-pointer"
                            @click="$router.push('/signup')"
                        >
                            <i class="fas fa-rocket"></i>
                            Get Started
                            <i class="fas fa-arrow-right transform group-hover:translate-x-1 transition-transform duration-300"></i>
                        </button>

                        <button 
                            class="group px-8 py-4 bg-white text-phisward-primary border-2 border-phisward-primary/20 rounded-lg font-semibold text-lg hover:border-phisward-primary hover:shadow-lg transform hover:-translate-y-1 transition-all duration-300 flex items-center justify-center gap-3 cursor-pointer"
                            @click="$router.push('/demo')"
                        >
                            <i class="fas fa-play-circle"></i>
                            Request Demo
                        </button>
                    </div>

                    <!-- Trust Indicators -->
                    <div class="flex flex-wrap items-center justify-center lg:justify-start gap-6 text-sm text-gray-600 animate-fade-in-up animation-delay-1000">
                        <div class="flex items-center gap-2">
                            <i class="fas fa-lock text-phisward-secondary"></i>
                            <span>SOC 2 Compliant</span>
                        </div>
                        <div class="flex items-center gap-2">
                            <i class="fas fa-shield-alt text-phisward-secondary"></i>
                            <span>GDPR Ready</span>
                        </div>
                        <div class="flex items-center gap-2">
                            <i class="fas fa-certificate text-phisward-secondary"></i>
                            <span>ISO 27001</span>
                        </div>
                    </div>
                </div>

                <!-- Right Content - Logo & Visualization -->
                <div class="flex-1 flex items-center justify-center">
                    <div class="relative group">
                        <!-- Main Logo with Shield Effect -->
                        <div class="relative z-10 transform group-hover:scale-105 transition-transform duration-500">
                            <div class="absolute inset-0 bg-gradient-to-r from-phisward-secondary to-phisward-third rounded-full blur-2xl opacity-30 group-hover:opacity-50 transition-opacity duration-500 animate-pulse-slow"></div>
                            <img
                                class="relative w-80 sm:w-96 md:w-[500px] lg:w-[600px] drop-shadow-2xl animate-float"
                                src="../../assets/logos/logo.png"
                                alt="Phish Ward Logo"
                            >
                        </div>

                        <!-- Orbiting Security Elements -->
                        <div class="absolute inset-0 animate-spin-very-slow">
                            <!-- Email Icon -->
                            <div class="absolute top-0 left-1/2 transform -translate-x-1/2 -translate-y-4">
                                <div class="w-16 h-16 bg-white rounded-xl shadow-xl flex items-center justify-center border border-phisward-secondary/20 hover:scale-110 transition-transform duration-300">
                                    <i class="fas fa-envelope text-phisward-secondary text-xl"></i>
                                </div>
                            </div>

                            <!-- Slack Icon -->
                            <div class="absolute top-1/2 right-0 transform translate-x-4 -translate-y-1/2">
                                <div class="w-14 h-14 bg-white rounded-lg shadow-xl flex items-center justify-center border border-phisward-third/20 hover:scale-110 transition-transform duration-300">
                                    <i class="fab fa-slack text-phisward-third text-lg"></i>
                                </div>
                            </div>

                            <!-- Telegram Icon -->
                            <div class="absolute bottom-0 left-1/2 transform -translate-x-1/2 translate-y-4">
                                <div class="w-12 h-12 bg-white rounded-lg shadow-xl flex items-center justify-center border border-phisward-primary/20 hover:scale-110 transition-transform duration-300">
                                    <i class="fab fa-telegram text-phisward-primary"></i>
                                </div>
                            </div>

                            <!-- AI Brain Icon -->
                            <div class="absolute top-1/2 left-0 transform -translate-x-4 -translate-y-1/2">
                                <div class="w-14 h-14 bg-white rounded-lg shadow-xl flex items-center justify-center border border-green-500/20 hover:scale-110 transition-transform duration-300">
                                    <i class="fas fa-brain text-green-500 text-lg"></i>
                                </div>
                            </div>
                        </div>

                        <!-- Floating Feature Cards -->
                        <div class="absolute -top-8 -left-8 animate-float-reverse">
                            <div class="bg-white/95 backdrop-blur-sm rounded-xl p-4 shadow-xl border border-phisward-primary/20">
                                <div class="flex items-center gap-3">
                                    <div class="w-8 h-8 bg-green-500 rounded-lg flex items-center justify-center">
                                        <i class="fas fa-check text-white text-sm"></i>
                                    </div>
                                    <div>
                                        <div class="font-semibold text-gray-800 text-sm">Real-Time Detection</div>
                                        <div class="text-xs text-gray-600">24/7 Monitoring</div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div class="absolute -bottom-8 -right-8 animate-float animation-delay-500">
                            <div class="bg-white/95 backdrop-blur-sm rounded-xl p-4 shadow-xl border border-phisward-third/20">
                                <div class="flex items-center gap-3">
                                    <div class="w-8 h-8 bg-phisward-secondary rounded-lg flex items-center justify-center">
                                        <i class="fas fa-chart-line text-white text-sm"></i>
                                    </div>
                                    <div>
                                        <div class="font-semibold text-gray-800 text-sm">Advanced Analytics</div>
                                        <div class="text-xs text-gray-600">Threat Intelligence</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Scroll Indicator -->
        <div class="absolute bottom-8 left-1/2 transform -translate-x-1/2 animate-bounce">
            <div class="flex flex-col items-center gap-2 text-gray-400">
                <span class="text-sm font-medium">Explore Features</span>
                <i class="fas fa-chevron-down text-lg"></i>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
</script>

<style scoped>
.container {
    max-width: 1400px;
}

/* Custom Animations */
@keyframes float {
    0%, 100% { transform: translateY(0px) rotate(0deg); }
    50% { transform: translateY(-20px) rotate(2deg); }
}

@keyframes float-slow {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-30px); }
}

@keyframes float-slower {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-15px); }
}

@keyframes float-reverse {
    0%, 100% { transform: translateY(0px) rotate(0deg); }
    50% { transform: translateY(15px) rotate(-1deg); }
}

@keyframes pulse-slow {
    0%, 100% { opacity: 0.8; }
    50% { opacity: 0.4; }
}

@keyframes spin-very-slow {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

@keyframes fade-in-up {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.animate-float {
    animation: float 6s ease-in-out infinite;
}

.animate-float-slow {
    animation: float-slow 8s ease-in-out infinite;
}

.animate-float-slower {
    animation: float-slower 12s ease-in-out infinite;
}

.animate-float-reverse {
    animation: float-reverse 7s ease-in-out infinite;
}

.animate-pulse-slow {
    animation: pulse-slow 4s ease-in-out infinite;
}

.animate-spin-very-slow {
    animation: spin-very-slow 60s linear infinite;
}

.animate-fade-in-up {
    opacity: 0;
    animation: fade-in-up 0.8s ease-out forwards;
}

.animation-delay-200 { animation-delay: 200ms; }
.animation-delay-400 { animation-delay: 400ms; }
.animation-delay-500 { animation-delay: 500ms; }
.animation-delay-600 { animation-delay: 600ms; }
.animation-delay-800 { animation-delay: 800ms; }
.animation-delay-1000 { animation-delay: 1000ms; }

.bg-clip-text {
    -webkit-background-clip: text;
    background-clip: text;
}

.backdrop-blur-sm {
    backdrop-filter: blur(4px);
}
</style>
