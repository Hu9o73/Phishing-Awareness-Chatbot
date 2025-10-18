<template>
  <div class="py-20 bg-gradient-to-b from-white to-phisward-fourth/30 relative overflow-hidden">
    <!-- Background Elements -->
    <div class="absolute inset-0 overflow-hidden">
      <div class="absolute top-20 right-10 w-64 h-64 bg-phisward-secondary/5 rounded-full blur-3xl"></div>
      <div class="absolute bottom-20 left-10 w-80 h-80 bg-phisward-third/5 rounded-full blur-3xl"></div>
    </div>

    <div class="container mx-auto px-6 relative z-10">
      <!-- Section Header -->
      <div class="text-center mb-20">
        <div class="inline-flex items-center gap-2 bg-phisward-primary/10 rounded-full px-6 py-3 mb-6">
          <i class="fas fa-shield-alt text-phisward-primary"></i>
          <span class="text-phisward-primary font-semibold">Enterprise Features</span>
        </div>

        <h2 class="text-4xl md:text-5xl lg:text-6xl font-bold text-phisward-primary mb-6">
          Comprehensive <span class="bg-gradient-to-r from-phisward-secondary to-phisward-third bg-clip-text text-transparent">Security Training</span>
        </h2>

        <p class="text-xl text-gray-600 max-w-3xl mx-auto">
          Deploy realistic phishing simulations across multiple channels, track employee performance, and build a security-conscious culture with AI-powered personalization.
        </p>
      </div>

      <!-- Main Features Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 mb-20">

        <!-- Feature 1: Multi-Channel Simulations -->
        <div class="group">
          <div class="bg-white rounded-2xl p-8 shadow-xl border border-gray-100 hover:shadow-2xl transition-all duration-500 transform hover:-translate-y-2">
            <!-- Icon and Badge -->
            <div class="flex items-center justify-between mb-6">
              <div class="w-16 h-16 bg-gradient-to-r from-phisward-secondary to-phisward-third rounded-xl flex items-center justify-center shadow-lg">
                <i class="fas fa-network-wired text-white text-2xl"></i>
              </div>
              <div class="px-4 py-2 bg-phisward-secondary/10 text-phisward-secondary rounded-full text-sm font-semibold">
                Multi-Channel
              </div>
            </div>

            <h3 class="text-2xl font-bold text-phisward-primary mb-4">Multi-Channel Simulations</h3>
            <p class="text-gray-600 mb-6 leading-relaxed">
              Deploy realistic phishing scenarios across email, Slack, Telegram, and other communication channels. Test your employees where they're most vulnerable.
            </p>

            <!-- Channel Preview -->
            <div class="bg-phisward-fourth/50 rounded-xl p-4 border border-phisward-primary/10 group-hover:border-phisward-secondary/30 transition-colors duration-300">
              <div class="flex items-center justify-between mb-3">
                <span class="text-sm font-semibold text-gray-700">Active Channels</span>
                <span class="text-xs text-green-600 font-semibold bg-green-100 px-2 py-1 rounded-full">
                  <i class="fas fa-check-circle mr-1"></i>Live
                </span>
              </div>

              <div class="grid grid-cols-2 gap-3">
                <div v-for="channel in channels" :key="channel.name"
                     class="bg-white rounded-lg p-3 shadow-sm border border-gray-100 hover:border-phisward-secondary/50 transition-colors duration-300">
                  <div class="flex items-center gap-3">
                    <div class="w-10 h-10 rounded-lg flex items-center justify-center"
                         :class="channel.color">
                      <i :class="channel.icon + ' text-white text-lg'"></i>
                    </div>
                    <div class="flex-1">
                      <div class="text-sm font-semibold text-gray-800">{{ channel.name }}</div>
                      <div class="text-xs text-gray-500">{{ channel.campaigns }} campaigns</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Feature 2: AI-Powered Personalization -->
        <div class="group">
          <div class="bg-white rounded-2xl p-8 shadow-xl border border-gray-100 hover:shadow-2xl transition-all duration-500 transform hover:-translate-y-2">
            <!-- Icon and Badge -->
            <div class="flex items-center justify-between mb-6">
              <div class="w-16 h-16 bg-gradient-to-r from-purple-600 to-indigo-600 rounded-xl flex items-center justify-center shadow-lg">
                <i class="fas fa-brain text-white text-2xl"></i>
              </div>
              <div class="px-4 py-2 bg-purple-100 text-purple-600 rounded-full text-sm font-semibold">
                AI Powered
              </div>
            </div>

            <h3 class="text-2xl font-bold text-phisward-primary mb-4">AI-Powered Personalization</h3>
            <p class="text-gray-600 mb-6 leading-relaxed">
              Advanced AI analyzes employee behavior and adapts scenarios in real-time. Each simulation is tailored to individual skill levels and vulnerabilities.
            </p>

            <!-- AI Analytics Demo -->
            <div class="bg-phisward-fourth/50 rounded-xl p-4 border border-phisward-primary/10 group-hover:border-purple-300 transition-colors duration-300">
              <div class="flex items-center justify-between mb-3">
                <div class="flex items-center gap-2">
                  <i class="fas fa-robot text-purple-600"></i>
                  <span class="text-sm font-semibold text-gray-700">AI Adaptation Engine</span>
                </div>
                <div class="text-xs text-purple-600 font-semibold bg-purple-100 px-2 py-1 rounded-full">
                  Learning
                </div>
              </div>

              <div class="space-y-3">
                <div v-for="metric in aiMetrics" :key="metric.label"
                     class="bg-white rounded-lg p-3 border border-gray-100">
                  <div class="flex items-center justify-between mb-2">
                    <span class="text-sm font-medium text-gray-700">{{ metric.label }}</span>
                    <span class="text-sm font-bold text-phisward-secondary">{{ metric.value }}%</span>
                  </div>
                  <div class="w-full h-2 bg-gray-200 rounded-full overflow-hidden">
                    <div class="h-full bg-gradient-to-r from-purple-500 to-indigo-500 rounded-full transition-all duration-500"
                         :style="{ width: metric.value + '%' }"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Feature 3: Interactive Learning Paths -->
        <div class="group">
          <div class="bg-white rounded-2xl p-8 shadow-xl border border-gray-100 hover:shadow-2xl transition-all duration-500 transform hover:-translate-y-2">
            <!-- Icon and Badge -->
            <div class="flex items-center justify-between mb-6">
              <div class="w-16 h-16 bg-gradient-to-r from-green-600 to-emerald-600 rounded-xl flex items-center justify-center shadow-lg">
                <i class="fas fa-graduation-cap text-white text-2xl"></i>
              </div>
              <div class="px-4 py-2 bg-green-100 text-green-600 rounded-full text-sm font-semibold">
                Learning
              </div>
            </div>

            <h3 class="text-2xl font-bold text-phisward-primary mb-4">Interactive Learning Paths</h3>
            <p class="text-gray-600 mb-6 leading-relaxed">
              When employees fall for a simulation, they're immediately guided through targeted learning modules specific to the attack vector they encountered.
            </p>

            <!-- Learning Path Demo -->
            <div class="bg-phisward-fourth/50 rounded-xl p-4 border border-phisward-primary/10 group-hover:border-green-300 transition-colors duration-300">
              <div class="flex items-center justify-between mb-3">
                <span class="text-sm font-semibold text-gray-700">Learning Modules</span>
                <div class="text-xs text-green-600 font-semibold">{{ learningModules.length }} Active</div>
              </div>

              <div class="space-y-2">
                <div v-for="module in learningModules" :key="module.title"
                     class="bg-white rounded-lg p-3 shadow-sm border border-gray-100 flex items-center justify-between">
                  <div class="flex items-center gap-3">
                    <div class="w-8 h-8 rounded-lg flex items-center justify-center"
                         :class="module.completed ? 'bg-green-500' : 'bg-gray-300'">
                      <i :class="(module.completed ? 'fas fa-check' : 'fas fa-lock') + ' text-white text-sm'"></i>
                    </div>
                    <div>
                      <div class="text-sm font-medium text-gray-800">{{ module.title }}</div>
                      <div class="text-xs text-gray-500">{{ module.duration }} • {{ module.difficulty }}</div>
                    </div>
                  </div>
                  <div v-if="module.completed" class="text-xs font-semibold px-2 py-1 rounded-full bg-green-100 text-green-600">
                    Complete
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Feature 4: Real-Time Analytics & Reporting -->
        <div class="group">
          <div class="bg-white rounded-2xl p-8 shadow-xl border border-gray-100 hover:shadow-2xl transition-all duration-500 transform hover:-translate-y-2">
            <!-- Icon and Badge -->
            <div class="flex items-center justify-between mb-6">
              <div class="w-16 h-16 bg-gradient-to-r from-phisward-primary to-phisward-secondary rounded-xl flex items-center justify-center shadow-lg">
                <i class="fas fa-chart-line text-white text-2xl"></i>
              </div>
              <div class="px-4 py-2 bg-phisward-primary/10 text-phisward-primary rounded-full text-sm font-semibold">
                Analytics
              </div>
            </div>

            <h3 class="text-2xl font-bold text-phisward-primary mb-4">Real-Time Analytics & Reporting</h3>
            <p class="text-gray-600 mb-6 leading-relaxed">
              Track campaign performance, employee vulnerability scores, and training effectiveness with comprehensive dashboards and automated reporting.
            </p>

            <!-- Analytics Dashboard Demo -->
            <div class="bg-phisward-fourth/50 rounded-xl p-4 border border-phisward-primary/10 group-hover:border-phisward-secondary/30 transition-colors duration-300">
              <div class="flex items-center justify-between mb-3">
                <span class="text-sm font-semibold text-gray-700">Security Metrics</span>
                <div class="text-xs text-phisward-secondary font-semibold bg-phisward-secondary/10 px-2 py-1 rounded-full">
                  Live Data
                </div>
              </div>

              <div class="grid grid-cols-2 gap-3">
                <div v-for="stat in securityStats" :key="stat.label"
                     class="bg-white rounded-lg p-3 border border-gray-100">
                  <div class="flex items-center gap-2 mb-2">
                    <i :class="stat.icon + ' text-phisward-secondary'"></i>
                    <span class="text-xs text-gray-600">{{ stat.label }}</span>
                  </div>
                  <div class="text-2xl font-bold text-phisward-primary">{{ stat.value }}</div>
                  <div class="flex items-center gap-1 mt-1">
                    <i :class="(stat.trend === 'up' ? 'fas fa-arrow-up text-green-500' : 'fas fa-arrow-down text-red-500') + ' text-xs'"></i>
                    <span :class="(stat.trend === 'up' ? 'text-green-600' : 'text-red-600') + ' text-xs font-semibold'">
                      {{ stat.change }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Feature 5: Scenario Customization -->
        <div class="group">
          <div class="bg-white rounded-2xl p-8 shadow-xl border border-gray-100 hover:shadow-2xl transition-all duration-500 transform hover:-translate-y-2">
            <!-- Icon and Badge -->
            <div class="flex items-center justify-between mb-6">
              <div class="w-16 h-16 bg-gradient-to-r from-orange-600 to-red-600 rounded-xl flex items-center justify-center shadow-lg">
                <i class="fas fa-cogs text-white text-2xl"></i>
              </div>
              <div class="px-4 py-2 bg-orange-100 text-orange-600 rounded-full text-sm font-semibold">
                Customizable
              </div>
            </div>

            <h3 class="text-2xl font-bold text-phisward-primary mb-4">Scenario Customization</h3>
            <p class="text-gray-600 mb-6 leading-relaxed">
              Create custom phishing scenarios tailored to your organization's specific risks, industry threats, and employee roles for maximum relevance.
            </p>

            <!-- Scenario Builder Demo -->
            <div class="bg-phisward-fourth/50 rounded-xl p-4 border border-phisward-primary/10 group-hover:border-orange-300 transition-colors duration-300">
              <div class="flex items-center justify-between mb-3">
                <span class="text-sm font-semibold text-gray-700">Scenario Templates</span>
                <div class="text-xs text-orange-600 font-semibold bg-orange-100 px-2 py-1 rounded-full">
                  {{ scenarioTemplates.length }} Available
                </div>
              </div>

              <div class="space-y-2">
                <div v-for="scenario in scenarioTemplates" :key="scenario.name"
                     class="bg-white rounded-lg p-3 shadow-sm border border-gray-100 hover:border-orange-300 transition-colors duration-300 cursor-pointer">
                  <div class="flex items-center justify-between">
                    <div class="flex items-center gap-3">
                      <div class="w-8 h-8 rounded-lg flex items-center justify-center"
                           :class="'bg-' + scenario.severity + '-100'">
                        <i :class="'fas fa-exclamation-triangle text-' + scenario.severity + '-600 text-sm'"></i>
                      </div>
                      <div>
                        <div class="text-sm font-medium text-gray-800">{{ scenario.name }}</div>
                        <div class="text-xs text-gray-500">{{ scenario.type }}</div>
                      </div>
                    </div>
                    <div :class="'text-xs font-semibold px-2 py-1 rounded-full bg-' + scenario.severity + '-100 text-' + scenario.severity + '-600'">
                      {{ scenario.difficulty }}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Feature 6: Threat Intelligence Integration -->
        <div class="group">
          <div class="bg-white rounded-2xl p-8 shadow-xl border border-gray-100 hover:shadow-2xl transition-all duration-500 transform hover:-translate-y-2">
            <!-- Icon and Badge -->
            <div class="flex items-center justify-between mb-6">
              <div class="w-16 h-16 bg-gradient-to-r from-red-600 to-pink-600 rounded-xl flex items-center justify-center shadow-lg">
                <i class="fas fa-satellite-dish text-white text-2xl"></i>
              </div>
              <div class="px-4 py-2 bg-red-100 text-red-600 rounded-full text-sm font-semibold">
                Real-Time
              </div>
            </div>

            <h3 class="text-2xl font-bold text-phisward-primary mb-4">Threat Intelligence Integration</h3>
            <p class="text-gray-600 mb-6 leading-relaxed">
              Stay ahead of emerging threats with simulations based on real-world phishing campaigns detected globally, updated in real-time.
            </p>

            <!-- Threat Feed Demo -->
            <div class="bg-phisward-fourth/50 rounded-xl p-4 border border-phisward-primary/10 group-hover:border-red-300 transition-colors duration-300">
              <div class="flex items-center justify-between mb-3">
                <div class="flex items-center gap-2">
                  <i class="fas fa-rss text-red-600"></i>
                  <span class="text-sm font-semibold text-gray-700">Live Threat Feed</span>
                </div>
                <div class="text-xs text-red-600 font-semibold bg-red-100 px-2 py-1 rounded-full animate-pulse">
                  Monitoring
                </div>
              </div>

              <div class="space-y-2">
                <div v-for="threat in threatFeed" :key="threat.id"
                     class="bg-white rounded-lg p-3 shadow-sm border border-gray-100">
                  <div class="flex items-center justify-between mb-2">
                    <div class="flex items-center gap-2">
                      <div :class="'w-2 h-2 rounded-full bg-' + threat.severity + '-500 animate-pulse'"></div>
                      <span class="text-sm font-medium text-gray-800">{{ threat.type }}</span>
                    </div>
                    <span class="text-xs text-gray-500">{{ threat.time }}</span>
                  </div>
                  <div class="text-xs text-gray-600">{{ threat.description }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>

      </div>

      <!-- Bottom CTA Section -->
      <div class="text-center bg-gradient-to-r from-phisward-primary to-phisward-secondary rounded-2xl p-12 shadow-2xl">
        <h3 class="text-3xl md:text-4xl font-bold text-white mb-4">
          Ready to Strengthen Your Security?
        </h3>
        <p class="text-xl text-white/90 mb-8 max-w-2xl mx-auto">
          Join leading organizations protecting their teams with Phish Ward's enterprise-grade training platform.
        </p>
        <button 
          class="px-8 py-4 bg-white text-phisward-primary rounded-lg font-semibold text-lg shadow-lg hover:shadow-xl transform hover:-translate-y-1 transition-all duration-300 cursor-pointer"
          @click="$router.push('/signup')"
        >
          <i class="fas fa-rocket mr-2"></i>
          Get Started Today
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

// Mock data for demonstrations
const channels = ref([
  { name: 'Email', icon: 'fas fa-envelope', campaigns: 24, color: 'bg-phisward-secondary' },
  { name: 'Slack', icon: 'fab fa-slack', campaigns: 18, color: 'bg-phisward-third' },
  { name: 'Telegram', icon: 'fab fa-telegram', campaigns: 12, color: 'bg-phisward-primary' },
  { name: 'Teams', icon: 'fab fa-microsoft', campaigns: 15, color: 'bg-blue-600' },
])

const aiMetrics = ref([
  { label: 'Personalization', value: 94 },
  { label: 'Threat Accuracy', value: 89 },
  { label: 'Learning Adaptation', value: 96 },
])

const learningModules = ref([
  { title: 'Email Phishing Basics', duration: '15 min', difficulty: 'Beginner', completed: true },
  { title: 'Social Engineering Tactics', duration: '20 min', difficulty: 'Intermediate', completed: true },
  { title: 'Advanced Threat Detection', duration: '30 min', difficulty: 'Advanced', completed: false },
])

const securityStats = ref([
  { label: 'Awareness', value: '87%', change: '+12%', trend: 'up', icon: 'fas fa-shield-alt' },
  { label: 'Response Time', value: '2.3s', change: '-0.5s', trend: 'up', icon: 'fas fa-clock' },
  { label: 'Click Rate', value: '8%', change: '-15%', trend: 'up', icon: 'fas fa-mouse-pointer' },
  { label: 'Reporting', value: '92%', change: '+8%', trend: 'up', icon: 'fas fa-flag' },
])

const scenarioTemplates = ref([
  { name: 'CEO Fraud', type: 'Email Impersonation', difficulty: 'High', severity: 'red' },
  { name: 'Invoice Scam', type: 'Payment Fraud', difficulty: 'Medium', severity: 'orange' },
  { name: 'IT Support', type: 'Credential Harvesting', difficulty: 'Medium', severity: 'yellow' },
])

const threatFeed = ref([
  { id: 1, type: 'Spear Phishing', description: 'Targeting C-level executives', time: '2 min ago', severity: 'red' },
  { id: 2, type: 'Credential Theft', description: 'Fake login pages detected', time: '15 min ago', severity: 'orange' },
  { id: 3, type: 'Malware Delivery', description: 'Suspicious attachments', time: '1 hour ago', severity: 'yellow' },
])
</script>

<style scoped>
.container {
  max-width: 1400px;
}

.bg-clip-text {
  -webkit-background-clip: text;
  background-clip: text;
}
</style>
