<script setup>
import {RouterView } from 'vue-router'

</script>

<template>
  <header class="flex-all">
    <h2>PIPE NETWORK ANALYSIS</h2>
  </header>
  <main class="flex-all">
    <RouterView />
  </main>
  <footer class="flex-all">
      &copy; 2024 JN. All rights reserved.
  </footer>
</template>

<style scoped>

body {
  font-family: Arial, sans-serif;
  background-color: #f4f4f9;
  color: #333;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100vh;
  overflow: hidden;
}

header, footer {
  text-align: center;
  color: white;
}

header {
  background-color: #4CAF50;
  height: 10vh;
}

main{
  height: 85vh;
  overflow-y: auto;
  background-color: #333;
}

footer {
  background-color: #4CAF50;
  height: 5vh;
}



</style>


