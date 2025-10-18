<template>
  <div class="flex flex-col min-h-screen">
    <Navbar/>
    <HeroSection/>
    <FeaturesOverview/>
    <Footer/>
  </div>
</template>

<script setup>
import HeroSection from '@/components/headers/HeroSection.vue';
import Navbar from '@/components/Navbar.vue';
import Footer from '@/components/Footer.vue';
import FeaturesOverview from '@/components/headers/FeaturesOverview.vue';
</script>
