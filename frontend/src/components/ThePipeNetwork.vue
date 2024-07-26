<script setup>
import { ref, computed } from 'vue'
import { defaultAxiosInstance } from '../util/axiosInstance'


const formErrorMessage = ref('')
const loading = ref(false)
const calculated = ref(false)
const testLoading = ref(null)
const results = ref(false)
const kLoops = ref([])
const errorTolerance = ref(null)
const calculatedResults = ref(null)
const darcyLoops = ref([])
const hazenLoops = ref([])
const resultType = ref(null)
const typeSelected = ref(null)
const equationType = ref(null)


const equationTypeOptions = ref([
  {'option': 'DARCY WEISBACH', 'value': 'darcy'},
  {'option': 'HAZEN WILLIAMS', 'value': 'hazen'},
])

const typeOptions = ref([
  {'type': 'USING PIPE CONSTANCE VALUES(K)', 'value': 'k'},
  {'type': "USING THE LENGTH AND DIAMETER OF THE PIPES", 'value': 'nk'}
])

const addLoop = ()=>{
  if (typeSelected.value === 'k'){
    kLoops.value.push({'name': '', 'props': []})
  }else if (typeSelected.value === 'nk' && equationType.value === 'darcy'){
    darcyLoops.value.push({'name': '', 'props': []})
  }else if (typeSelected.value === 'nk' && equationType.value === 'hazen'){
    hazenLoops.value.push({'name': '', 'props': []})
  }
}

const removeLoop = (index)=>{
  if (typeSelected.value === 'k'){
    kLoops.value.splice(index, 1)

  }else if (typeSelected.value === 'nk' && equationType.value === 'darcy'){
    darcyLoops.value.splice(index, 1)
    
  }else if (typeSelected.value === 'nk' && equationType.value === 'hazen'){
    hazenLoops.value.splice(index, 1)
  }
}

const addPipe = (index)=>{
  if (typeSelected.value === 'k'){
    kLoops.value[index]['props'].push({'pipe': '', 'K': '', 'Qa': ''})

  }else if (typeSelected.value === 'nk' && equationType.value === 'darcy'){
    darcyLoops.value[index]['props'].push({'pipe': '', 'length': '', 'diameter': '', 'f': '', 'Qa': ''})
    
  }else if (typeSelected.value === 'nk' && equationType.value === 'hazen'){
      hazenLoops.value[index]['props'].push({'pipe': '', 'length': '', 'diameter': '', 'C': '', 'Qa': ''})
  }
}

const removePipe = (index, i)=>{
  if (typeSelected.value === 'k'){
    kLoops.value[index]['props'].splice(i, 1)

  }else if (typeSelected.value === 'nk' && equationType.value === 'darcy'){
    darcyLoops.value[index]['props'].splice(i, 1)
    
  }else if (typeSelected.value === 'nk' && equationType.value === 'hazen'){
    hazenLoops.value[index]['props'].splice(i, 1)
  }
}

const checkInput = computed(()=>{
  if (typeSelected.value === 'k'){
    return !(equationType.value && kLoops.value.length > 0)
  }else if (typeSelected.value === 'nk' && equationType.value === 'darcy'){
    return !(darcyLoops.value.length > 0)
  }else if (typeSelected.value === 'nk' && equationType.value === 'hazen'){
    return !(hazenLoops.value.length > 0)
  }else {
    return true;
  }
})



const pipeNetwork = (type)=>{
  const loopNames = ref([])
  const allPipes = ref([])

  if (type === 'test'){
    testLoading.value = true
    // typeSelected.value = 'nk'
    // equationType.value = 'hazen'
    // const loops = ref([
    //   {'name': 'Loop A', 'props': [
    //       {'pipe': 'AB', 'length': 500, 'diameter':0.2, 'C': 100, 'Qa': 1},
    //       {'pipe': 'AC', 'length': 330, 'diameter':0.35, 'C': 100, 'Qa': -11},
    //       {'pipe': 'BD', 'length': 330, 'diameter':0.2, 'C': 100, 'Qa': 0.5},
    //       {'pipe': 'CD', 'length': 500, 'diameter':0.2, 'C': 100, 'Qa': -1},
    //   ]}
    // ])

    // hazenLoops.value = loops.value

    typeSelected.value = 'k'
    equationType.value = 'darcy'
    const loops = ref([
      {'name': '1', 'props': [
          {'pipe': 'AB', 'K': 4, 'Qa': 200},
          {'pipe': 'AF', 'K': 3, 'Qa': -300},
          {'pipe': 'BE', 'K': 1, 'Qa': 100},
          {'pipe': 'EF', 'K': 3, 'Qa': 50},
      ]},
      {'name': '2', 'props': [
          {'pipe': 'BC', 'K': 1, 'Qa': 100},
          {'pipe': 'BE', 'K': 1, 'Qa': -100},
          {'pipe': 'CD', 'K': 2, 'Qa': 50},
          {'pipe': 'DE', 'K': 3, 'Qa': 30},
      ]},
      {'name': '3', 'props': [
          {'pipe': 'DE', 'K': 3, 'Qa': -30},
          {'pipe': 'DJ', 'K': 5, 'Qa': -20},
          {'pipe': 'EH', 'K': 1, 'Qa': -80},
          {'pipe': 'HJ', 'K': 4, 'Qa': -280},
      ]},
      {'name': '4', 'props': [
          {'pipe': 'EF', 'K': 3, 'Qa': -50},
          {'pipe': 'EH', 'K': 1, 'Qa': 80},
          {'pipe': 'FG', 'K': 2, 'Qa': -350},
          {'pipe': 'GH', 'K': 2, 'Qa': -200},
      ]},
    ])
    kLoops.value = loops.value
    

  }else{
    loading.value = true
  }

  try {
    if (typeSelected.value === 'k'){
    kLoops.value.forEach(item =>{
      const pipeNames = ref([])
      item['props'].forEach(pipeItem =>{
        if (!pipeItem['pipe'] || !pipeItem['K'] || !pipeItem['Qa']){
          formErrorMessage.value = "Ensure you fill in all pipe data or remove the pipes that are not needed"
          clearMessage()
          throw new Error();
        }else if (pipeItem['K'].toString() === '0' || pipeItem['Qa'].toString() === '0'){
          formErrorMessage.value = `Invalid input!!. Check the values in pipe '${pipeItem['pipe']}' and ensure there are no zero values in the data`
          clearMessage()
          throw new Error();
        }
        pipeNames.value.push(pipeItem['pipe'])
        allPipes.value.push(pipeItem['pipe'])
      })

      if (pipeNames.value.length <= 2){
        formErrorMessage.value = "The number of pipes in a loop must be greater than two(2)"
        clearMessage()
        throw new Error();
      }
      if (pipeNames.value.some((pItem, index) => pipeNames.value.indexOf(pItem) !== index)){
        formErrorMessage.value = "Pipes in same loop cannot have the same name. Ensure names of pipes in same loop are different"
        clearMessage()
        throw new Error();
      }
      if (!item['name']){
        formErrorMessage.value = "Ensure you fill in all loop names or remove the loop if not needed"
        clearMessage()
        throw new Error();
      }
      loopNames.value.push(item['name'])
    })

  }else if (typeSelected.value === 'nk' && equationType.value === 'darcy'){
    darcyLoops.value.forEach(item =>{
      const pipeNames = ref([])
      item['props'].forEach(pipeItem =>{
        if (!pipeItem['pipe'] || !pipeItem['length'] || !pipeItem['diameter'] || !pipeItem['f'] || !pipeItem['Qa']){
          formErrorMessage.value = "Ensure you fill in all pipe data or remove the pipes that are not needed"
          clearMessage()
          throw new Error();
        }else if (pipeItem['length'].toString() === '0' || pipeItem['diameter'].toString() === '0' || pipeItem['f'].toString() === '0' || pipeItem['Qa'].toString() === '0'){
          formErrorMessage.value = `Invalid input!!. Check the values in pipe '${pipeItem['pipe']}' and ensure there are no zero values in the data`
          clearMessage()
          throw new Error();
        }
        pipeNames.value.push(pipeItem['pipe'])
        allPipes.value.push(pipeItem['pipe'])
      })
      if (pipeNames.value.length <= 2){
        formErrorMessage.value = "The number of pipes in a loop must be greater than two(2)"
        clearMessage()
        throw new Error();
      }
      if (pipeNames.value.some((pItem, index) => pipeNames.value.indexOf(pItem) !== index)){
        formErrorMessage.value = "Pipes in same loop cannot have the same name. Ensure names of pipes in same loop are different"
        clearMessage()
        throw new Error();
      }
      if (!item['name']){
        formErrorMessage.value = "Ensure you fill in all loop names or remove the loop if not needed"
        clearMessage()
        throw new Error();
      }
      loopNames.value.push(item['name'])
    })
  }else if (typeSelected.value === 'nk' && equationType.value === 'hazen'){
    hazenLoops.value.forEach(item =>{
      const pipeNames = ref([])
      item['props'].forEach(pipeItem =>{
        if (!pipeItem['pipe'] || !pipeItem['length'] || !pipeItem['diameter'] || !pipeItem['C'] || !pipeItem['Qa']){
          formErrorMessage.value = "Ensure you fill in all pipe data or remove the pipes that are not needed"
          clearMessage()
          throw new Error();
        }else if (pipeItem['length'].toString() === '0' || pipeItem['diameter'].toString() === '0' || pipeItem['C'].toString() === '0' || pipeItem['Qa'].toString() === '0'){
          formErrorMessage.value = `Invalid input!!. Check the values in pipe '${pipeItem['pipe']}' and ensure there are no zero values in the data`
          clearMessage()
          throw new Error();
        }
        pipeNames.value.push(pipeItem['pipe'])
        allPipes.value.push(pipeItem['pipe'])
      })
      if (pipeNames.value.length <= 2){
        formErrorMessage.value = "The number of pipes in a loop must be greater than two(2)"
        clearMessage()
        throw new Error();
      }
      if (pipeNames.value.some((pItem, index) => pipeNames.value.indexOf(pItem) !== index)){
        formErrorMessage.value = "Pipes in same loop cannot have the same name. Ensure names of pipes in same loop are different"
        clearMessage()
        throw new Error();
      }
      if (!item['name']){
        formErrorMessage.value = "Ensure you fill in all loop names or remove the loop if not needed"
        clearMessage()
        throw new Error();
      }
      loopNames.value.push(item['name'])
    })
  }
  if (loopNames.value.some((item, index) => loopNames.value.indexOf(item) !== index)){
    formErrorMessage.value = "Loops with the same name are not allowed. Ensure all loops have different names"
    clearMessage()
    throw new Error();
  }

  if (errorTolerance.value && errorTolerance.value <= 0){
    formErrorMessage.value = "The allowable error tolerance cannot be zero(0) or negative"
    clearMessage()
    throw new Error();
  }
  
  }catch(e){
    testLoading.value = false
    loading.value = false
    return;
  }
  
  const formData = new FormData()
  formData.append('equation', equationType.value)
  formData.append('K', typeSelected.value)
  errorTolerance.value ? formData.append('error', errorTolerance.value) : formData.append('error', 'false')
  typeSelected.value === 'k' ? formData.append('loops', JSON.stringify(kLoops.value)) : null
  typeSelected.value === 'nk' && equationType.value === 'darcy' ? formData.append('loops', JSON.stringify(darcyLoops.value)) : null
  typeSelected.value === 'nk' && equationType.value === 'hazen' ? formData.append('loops', JSON.stringify(hazenLoops.value)) : null

  const commonPipes = ref([])
  allPipes.value.forEach(item =>{
    const common_loops = ref([])
    if (typeSelected.value === 'k'){
      kLoops.value.forEach(loopItem =>{
        loopItem['props'].forEach(pipeItem =>{
          item === pipeItem['pipe'] ? common_loops.value.push(loopItem['name']) : null
        })
      })
    }else if (typeSelected.value === 'nk' && equationType.value === 'darcy'){
      darcyLoops.value.forEach(loopItem =>{
        loopItem['props'].forEach(pipeItem =>{
          item === pipeItem['pipe'] ? common_loops.value.push(loopItem['name']) : null
        })
      })
    }else if (typeSelected.value === 'nk' && equationType.value === 'hazen'){
      hazenLoops.value.forEach(loopItem =>{
        loopItem['props'].forEach(pipeItem =>{
          item === pipeItem['pipe'] ? common_loops.value.push(loopItem['name']) : null
        })
      })
    }
    common_loops.value.length >= 2 ? commonPipes.value.push({'name': item, 'loops': common_loops.value}) : null
  })

  commonPipes.value.length > 0 ? formData.append('commonPipes', JSON.stringify(commonPipes.value)) : formData.append('commonPipes', 'false')

  defaultAxiosInstance.post('pipe-network', formData)
  .then(response =>{
    if (response.data['results'] === 'yes'){
      calculatedResults.value = response.data['data']
      resultType.value = response.data['type']
      calculated.value = true
      results.value = true
    }else{
      formErrorMessage.value = response.data['data']
      clearMessage()
    }
    loading.value = false
    testLoading.value = false
  })
  .catch(e =>{
    loading.value = false
    testLoading.value = false
    formErrorMessage.value = "Something went wrong. Check you internet connection and try again"
    clearMessage()
  })

}

const toggleResult = (value)=>{
  results.value = value
}

const clearMessage = ()=>{
  setTimeout(()=>{
    formErrorMessage.value = ''
  }, 15000)
}

  
const clearOverlay = (type)=>{
  const overlay = document.getElementById("clearOverlay")
  if (type === 'show'){
      overlay ? overlay.style.display = 'flex': null
  }
  else if (type === 'hid'){
      overlay ? overlay.style.display = 'none': null
  }
}

const clearData = ()=>{
    formErrorMessage.value = ''
    loading.value = false
    testLoading.value = false
    calculated.value = false
    kLoops.value = []
    darcyLoops.value = []
    hazenLoops.value = []
    typeSelected.value = null
    equationType.value = null
    results.value = false
    errorTolerance.value = null
    resultType.value = null
    calculatedResults.value = null
    clearOverlay('hid')
}



</script>

<template>
    <div class="flex-all w-100 h-100">
      <div id="clearOverlay" class="clear-overlay">
        <v-card class="clear-overlay-card">
            <v-card-text class="clear-overlay-text">Are you sure you want to clear everything?</v-card-text>
            <v-card-actions class="clear-overlay-action">
                <v-btn @click="clearData" color="red" class="mr-5" >YES</v-btn>
                <v-btn class="ml-5" color="blue" @click="clearOverlay('hid')">NO</v-btn>
            </v-card-actions>
        </v-card>
      </div>
      <v-card class="card">

        <div class="error-message-container">
          <p v-if="!formErrorMessage" class="error-message">NB: Ensure consistent units</p>
          <p v-if="formErrorMessage" class="error-message">{{formErrorMessage}}</p>
        </div>
        <div class="input-container" v-if="!results">
          <v-select :items="equationTypeOptions" v-model="equationType" item-title="option" item-values="value" class="select" persistent-hint hint="Select the equation you want to use for the calculation" density="compact" variant="outlined">EQUATION</v-select>
          <v-select :items="typeOptions" v-model="typeSelected" item-title="type" item-values="value" class="select" persistent-hint hint="Select the type of data you want to use" density="compact" variant="outlined">DATA TYPE</v-select>
          <v-btn v-if="typeSelected && equationType" @click="addLoop()" class="mt-5 mb-5" color="green" size="small">ADD LOOP</v-btn>
          <div v-if="typeSelected == 'k' " class="loop-container flex-all">
            <div class="loop-wrapper" v-for="(loop, index) in kLoops" :key="index">
                <div class="w-100 loop-name">
                  <v-btn class="mr-5 mb-2" @click="removeLoop(index)" color="red" size="small">remove loop</v-btn>
                  <v-text-field class="text-field" style="max-width: 300px" label="LOOP NAME" v-model="loop['name']" density="compact" hint="Enter the name of the loop" variant="outlined"/>
                </div>
                <v-btn class="mb-2" @click="addPipe(index)" color="blue" size="small">ADD PIPE</v-btn>
                <div class="pipe-wrapper" v-for="(pipe, i) in loop['props']" :key="i">
                  <v-text-field class="text-field" v-model="pipe['pipe']" label="PIPE NAME" hint="Enter the name of the pipe" density="compact" variant="outlined"/>
                  <v-text-field class="text-field" v-model="pipe['K']" type="number" label="K" hint="Enter the pipe's K value" density="compact" variant="outlined"/>
                  <v-text-field class="text-field" v-model="pipe['Qa']" type="number" label="Qa" hint="Enter the assumed rate of the pipe" density="compact" variant="outlined"/>
                  <v-btn class="ml-3 mr-1 mb-2" @click="removePipe(index, i)" color="red" size="small">X</v-btn>
                </div>
            </div>
          </div>
          <div v-if="typeSelected == 'nk' && equationType == 'darcy' " class="loop-container flex-all">
            <div class="loop-wrapper" v-for="(loop, index) in darcyLoops" :key="index">
                <div class="w-100 loop-name">
                  <v-btn class="mr-5 mb-2" @click="removeLoop(index)" color="red" size="small">remove loop</v-btn>
                  <v-text-field class="text-field" style="max-width: 300px" label="LOOP NAME" v-model="loop['name']" hint="Enter the name of the loop" density="compact" variant="outlined"/>
                </div>
                <v-btn class="mt-5 mb-5" @click="addPipe(index)" color="blue" size="small">ADD PIPE</v-btn>
                <div class="pipe-wrapper" v-for="(pipe, i) in loop['props']" :key="i">
                  <v-text-field class="text-field" v-model="pipe['pipe']" label="PIPE NAME" hint="Enter the name of the pipe" density="compact" variant="outlined"/>
                  <v-text-field class="text-field" v-model="pipe['length']" type="number" label="LENGTH" hint="Enter the length of the pipe" density="compact" variant="outlined"/>
                  <v-text-field class="text-field" v-model="pipe['diameter']" type="number" label="DIAMETER" hint="Enter the diameter of the pipe" density="compact" variant="outlined"/>
                  <v-text-field class="text-field" v-model="pipe['f']" type="number" label="f" hint="Enter the Darcy friction factor of the pipe" density="compact" variant="outlined"/>
                  <v-text-field class="text-field" v-model="pipe['Qa']" type="number" label="Qa" hint="Enter the assumed rate of the pipe" density="compact" variant="outlined"/>
                  <v-btn class="ml-3 mr-1 mb-2" @click="removePipe(index, i)" color="red" size="small">X</v-btn>
                </div>
            </div>
          </div>

          <div v-if="typeSelected == 'nk' && equationType == 'hazen' " class="loop-container flex-all">
            <div class="loop-wrapper" v-for="(loop, index) in hazenLoops" :key="index">
                <div class="w-100 loop-name">
                  <v-btn class="mr-5 mb-2" @click="removeLoop(index)" color="red" size="small">remove loop</v-btn>
                  <v-text-field class="text-field" style="max-width: 300px" label="LOOP NAME" v-model="loop['name']" hint="Enter the name of the loop" density="compact" variant="outlined"/>                
                </div>
                <v-btn class="mt-3 mb-3" @click="addPipe(index)" color="blue" size="small">ADD PIPE</v-btn>
                <div class="pipe-wrapper" v-for="(pipe, i) in loop['props']" :key="i">
                  <v-text-field class="text-field" v-model="pipe['pipe']" label="PIPE NAME" hint="Enter the name of the pipe" density="compact" variant="outlined"/>
                  <v-text-field class="text-field" v-model="pipe['length']" type="number" label="LENGTH" hint="Enter the length of the pipe" density="compact" variant="outlined"/>
                  <v-text-field class="text-field" v-model="pipe['diameter']" type="number" label="DIAMETER" hint="Enter the diameter of the pipe" density="compact" variant="outlined"/>
                  <v-text-field class="text-field" v-model="pipe['C']" type="number" label="C" hint="Enter the Hazen William's coefficient of the pipe" density="compact" variant="outlined"/>
                  <v-text-field class="text-field" v-model="pipe['Qa']" type="number" label="Qa" hint="Enter the assumed rate of the pipe" density="compact" variant="outlined"/>
                  <v-btn class="ml-3 mr-1 mb-2" @click="removePipe(index, i)" color="red" size="small">X</v-btn>
                </div>
            </div>
          </div>
          <v-text-field v-if="typeSelected === 'k' && kLoops.length > 0 || typeSelected === 'nk' && equationType === 'hazen' && hazenLoops.length > 0 || typeSelected === 'nk' && equationType === 'darcy' && darcyLoops.length > 0 " class="text-field mb-10" style="width: 300px" v-model="errorTolerance" type="number" label="ERROR TOLERANCE(OPTIONAL)" placeholder="default: 0.00000008(1e-8)" hint="Enter the allowable error tolerance" density="compact" variant="outlined"/>
        </div>
        
        <!-- Result Overlay -->
      <div class="result-container" v-if="calculated && results">
        <v-table fixed-header height="70vh" theme="blue">
          <thead v-if="resultType === 'k'">
            <tr>
              <th class="th">Pipe</th>
              <th class="th">K</th>
              <th class="th">Qa</th>
              <th class="th">Q(corrected)</th>
              <th class="th">Head Loss</th>
            </tr>
          </thead>
          <thead v-if="resultType === 'darcy'">
            <tr>
              <th class="th">Pipe</th>
              <th class="th">Length</th>
              <th class="th">Diameter</th>
              <th class="th">f</th>
              <th class="th">Qa</th>
              <th class="th">Q(corrected)</th>
              <th class="th">Head Loss</th>
            </tr>
          </thead>
          <thead v-if="resultType === 'hazen'">
            <tr>
              <th class="th">Pipe</th>
              <th class="th">Length</th>
              <th class="th">Diameter</th>
              <th class="th">C</th>
              <th class="th">Qa</th>
              <th class="th">Q(corrected)</th>
              <th class="th">Head Loss</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(pipe, index) in calculatedResults" :key="index">
              <td v-for="(pipeData, i) in pipe" :key=i>
                {{pipeData}}
              </td>
            </tr>
          </tbody>
        </v-table>
      </div>
      
        <!-- Submit Buttons -->
      <div class="btn-container-wrapper">
        <div class="btn-container">
          <v-btn v-if="!calculated || !calculated " @click="pipeNetwork('calculate')" :disabled="checkInput || testLoading" :loading="loading" size="small" class="submit-btn" color="green">CALCULATE</v-btn>
          <v-btn v-if="!calculated " @click="pipeNetwork('test')" :loading="testLoading" :disabled="loading" size="small" class="submit-btn" color="white">TEST</v-btn>
          <v-btn v-if="calculated && !results || calculated && !results" @click="pipeNetwork('recalculate')" :disabled="checkInput || testLoading" :loading="loading" size="small" class="submit-btn" color="green">RECALCULATE</v-btn>
          <v-btn v-if="calculated && results" @click="toggleResult(false)" :disabled="loading || testLoading" size="small" color="blue" class="submit-btn">HIDE RESULT</v-btn>
          <v-btn v-if="calculated && !results" @click="toggleResult(true)" :disabled="loading || testLoading" size="small" color="blue" class="submit-btn">SHOW RESULT</v-btn>
          <v-btn @click="clearOverlay('show')" :disabled="loading || testLoading" color="red" size="small" class="submit-btn clear">CLEAR</v-btn>
        </div>
      </div>
    </v-card>
    </div>

    
</template>

<style scoped>

.clear-overlay{
  position: fixed;
  display: none;
  align-items: center;
  justify-content: center;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 100;
  background-color: rgba(0, 0, 0, 0.75);
}

.card{
  height: 95%;
  width: fit-content;
  display: flex;
  max-width: 1400px;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
}

.input-container, .result-container{
  display: flex;
  flex-direction: column;
  align-items: center;
  overflow: auto;
  justify-content: flex-start;
  width: 100%;
  height: 90%;
}

.result-container{
  width: fit-content;
}

.btn-container-wrapper{
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: black;
  width: 100%;
  height: 10%;
}

.btn-container{
  display: flex;
  align-items: center;
  justify-content: space-around;
  width: 100%;
  max-width: 400px;
  height: 100%;
}

.select{
  max-height: 50px !important;
  margin: 1em 0;
}

.text-field{
  max-height: 50px !important;
  margin: 1em 0;
  min-width: 150px !important;
}

.th{
  font-weight: bold !important;
}
.loop-container{
  width: 90%;
}

.loop-wrapper{
  display: flex;
  align-items: center;
  flex-direction: column;
  width: 100%;
  margin: 2em;
  border-top: 20px solid white;
  border-bottom: 20px solid white;
  padding: 0 1em;
  border: 2px solid black;
}

.loop-name{
  display: flex;
  align-items: center;
  justify-content: center;
}

.pipe-wrapper{
  display: flex;
  align-items: center;
  width: 100%;
}

.error-message-container{
  width: 100%;
  text-align: center;
  background-color: black;
}
.error-message{
  color: red;
  margin: 1em 0;
  font-weight: bold;
  font-family:Verdana, Geneva, Tahoma, sans-serif;
}



</style>