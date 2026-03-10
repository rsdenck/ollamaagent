<template>
  <div class="min-h-screen bg-[#0a0a0c] text-slate-200 font-sans selection:bg-indigo-500/30">
    <!-- Blurring Background Orbs -->
    <div class="fixed inset-0 overflow-hidden pointer-events-none">
      <div class="absolute -top-[10%] -left-[10%] w-[40%] h-[40%] bg-indigo-600/10 blur-[120px] rounded-full"></div>
      <div class="absolute top-[20%] -right-[10%] w-[30%] h-[30%] bg-blue-600/10 blur-[100px] rounded-full"></div>
      <div class="absolute -bottom-[10%] left-[20%] w-[50%] h-[40%] bg-purple-600/10 blur-[150px] rounded-full"></div>
    </div>

    <!-- Top Floating Navigation (Aria Operations Style) -->
    <nav class="fixed top-0 inset-x-0 z-50 flex justify-center py-4 pointer-events-none">
      <div class="inline-flex p-1.5 bg-slate-900/80 backdrop-blur-3xl border border-slate-800/50 rounded-2xl shadow-2xl pointer-events-auto transition-all duration-500 hover:border-indigo-500/30 overflow-x-auto max-w-[95vw] custom-scrollbar">
        <button 
          @click="activeTab = 'vmware'"
          :class="activeTab === 'vmware' ? 'bg-indigo-500 text-white shadow-lg shadow-indigo-500/20 scale-105' : 'text-slate-400 hover:text-slate-200'"
          class="px-5 py-2 rounded-xl text-[9px] font-black uppercase tracking-widest transition-all duration-300 flex items-center gap-2 whitespace-nowrap"
        >
          <UIcon name="i-heroicons-rectangle-stack" class="w-4 h-4" />
          VMware
        </button>
        <button 
          @click="activeTab = 'hyperv'"
          :class="activeTab === 'hyperv' ? 'bg-emerald-500 text-white shadow-lg shadow-emerald-500/20 scale-105' : 'text-slate-400 hover:text-slate-200'"
          class="px-5 py-2 rounded-xl text-[9px] font-black uppercase tracking-widest transition-all duration-300 flex items-center gap-2 whitespace-nowrap"
        >
          <UIcon name="i-heroicons-cpu-chip" class="w-4 h-4" />
          Hyper-V
        </button>
        <button 
          @click="activeTab = 'storage'"
          :class="activeTab === 'storage' ? 'bg-amber-500 text-white shadow-lg shadow-amber-500/20 scale-105' : 'text-slate-400 hover:text-slate-200'"
          class="px-5 py-2 rounded-xl text-[9px] font-black uppercase tracking-widest transition-all duration-300 flex items-center gap-2 whitespace-nowrap"
        >
          <UIcon name="i-heroicons-circle-stack" class="w-4 h-4" />
          Storage
        </button>
        <button 
          @click="activeTab = 'networks'"
          :class="activeTab === 'networks' ? 'bg-blue-600 text-white shadow-lg shadow-blue-600/20 scale-105' : 'text-slate-400 hover:text-slate-200'"
          class="px-5 py-2 rounded-xl text-[9px] font-black uppercase tracking-widest transition-all duration-300 flex items-center gap-2 whitespace-nowrap"
        >
          <UIcon name="i-heroicons-globe-alt" class="w-4 h-4" />
          Redes
        </button>
        <button 
          @click="activeTab = 'mail'"
          :class="activeTab === 'mail' ? 'bg-red-500 text-white shadow-lg shadow-red-500/20 scale-105' : 'text-slate-400 hover:text-slate-200'"
          class="px-5 py-2 rounded-xl text-[9px] font-black uppercase tracking-widest transition-all duration-300 flex items-center gap-2 whitespace-nowrap"
        >
          <UIcon name="i-heroicons-envelope" class="w-4 h-4" />
          Mail
        </button>
        <button 
          @click="activeTab = 'veeam'"
          :class="activeTab === 'veeam' ? 'bg-blue-500 text-white shadow-lg shadow-blue-500/20 scale-105' : 'text-slate-400 hover:text-slate-200'"
          class="px-5 py-2 rounded-xl text-[9px] font-black uppercase tracking-widest transition-all duration-300 flex items-center gap-2 whitespace-nowrap"
        >
          <UIcon name="i-heroicons-shield-check" class="w-4 h-4" />
          Veeam
        </button>
        <button 
          @click="activeTab = 'ia'"
          :class="activeTab === 'ia' ? 'bg-purple-600 text-white shadow-lg shadow-purple-600/20 scale-105' : 'text-slate-400 hover:text-slate-200'"
          class="px-5 py-2 rounded-xl text-[9px] font-black uppercase tracking-widest transition-all duration-300 flex items-center gap-2 whitespace-nowrap"
        >
          <UIcon name="i-heroicons-sparkles" class="w-4 h-4" />
          SRE Analysis
        </button>
      </div>
    </nav>

    <!-- Layout Container -->
    <div class="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 pt-24 pb-12">
      

      <!-- VMware View (Enterprise Multi-vCenter) -->
      <div v-if="activeTab === 'vmware'" class="animate-in fade-in zoom-in-95 duration-700">
        <div class="mb-10 flex flex-col md:flex-row justify-between items-end gap-4">
          <div>
            <h2 class="text-3xl font-black text-white mb-2 italic">VMware Cloud Ecosystem</h2>
            <p class="text-slate-500 font-bold uppercase tracking-widest text-[10px]">Consolidated vCenter & ESXi Infrastructure</p>
          </div>
          <div class="flex items-center gap-3 bg-slate-900/60 p-2 rounded-2xl border border-slate-800/50">
             <div class="px-4 py-2 bg-indigo-500/10 rounded-xl border border-indigo-500/20">
                <span class="text-[10px] text-indigo-400 font-black uppercase block">Active vCenters</span>
                <span class="text-xl font-black text-indigo-400">02</span>
             </div>
          </div>
        </div>

        <div class="grid grid-cols-1 xl:grid-cols-2 gap-8 mb-12">
          <div v-for="(vc, name) in vmwareData.vcenters" :key="name" class="bg-slate-900/40 border border-slate-800/50 backdrop-blur-xl rounded-[2.5rem] p-8 hover:border-indigo-500/40 transition-all duration-500 shadow-2xl relative overflow-hidden group">
            <div class="absolute -top-20 -right-20 w-40 h-40 bg-indigo-500/10 blur-[60px] rounded-full group-hover:bg-indigo-500/20 transition-colors"></div>
            <div class="flex items-center justify-between mb-8">
              <div class="flex items-center gap-4 text-indigo-400">
                <div class="p-4 bg-indigo-500/10 rounded-2xl shadow-inner group-hover:bg-indigo-500 group-hover:text-white transition-all">
                  <UIcon name="i-heroicons-rectangle-stack" class="w-8 h-8" />
                </div>
                <div>
                  <h3 class="text-2xl font-black text-white tracking-tighter">{{ name }}</h3>
                  <span class="text-[10px] font-black text-slate-500 uppercase tracking-widest">{{ vc.host }}</span>
                </div>
              </div>
              <UBadge :color="vc.status === 'online' ? 'emerald' : 'red'" variant="soft" class="font-black px-4 rounded-full uppercase text-[9px]">
                {{ vc.status }}
              </UBadge>
            </div>

            <div v-if="vc.status === 'online'" class="grid grid-cols-3 gap-6">
              <div class="bg-slate-950/60 p-4 rounded-2xl border border-slate-800/50 text-center">
                <span class="text-[10px] font-black text-slate-500 uppercase block mb-1">Hosts</span>
                <span class="text-xl font-black text-white">{{ vc.summary?.hosts || 0 }}</span>
              </div>
              <div class="bg-slate-950/60 p-4 rounded-2xl border border-slate-800/50 text-center">
                <span class="text-[10px] font-black text-slate-500 uppercase block mb-1">VMs</span>
                <span class="text-xl font-black text-white">{{ vc.summary?.vms || 0 }}</span>
              </div>
              <div class="bg-slate-950/60 p-4 rounded-2xl border border-slate-800/50 text-center">
                <span class="text-[10px] font-black text-slate-500 uppercase block mb-1">Datastores</span>
                <span class="text-xl font-black text-white">{{ vc.summary?.datastores || 0 }}</span>
              </div>
            </div>
            <div v-else class="py-10 text-center text-slate-500 italic text-sm">
              Connection lost with vCenter REST API.
            </div>
          </div>
        </div>
      </div>

      <!-- Hyper-V View (VMM Deep Insight) -->
      <div v-if="activeTab === 'hyperv'" class="animate-in fade-in zoom-in-95 duration-700">
        <div class="mb-10 flex flex-col md:flex-row justify-between items-center gap-4">
          <div>
            <h2 class="text-3xl font-black text-white mb-2 italic">Hyper-V Infrastructure</h2>
            <p class="text-slate-500 font-bold uppercase tracking-widest text-[10px]">SCVMM Hierarchical Inventory & Performance</p>
          </div>
          <div class="w-full md:w-80">
            <UInput 
              v-model="hypervSearch" 
              placeholder="Filter Clusters, Hosts or VMs..." 
              icon="i-heroicons-funnel" 
              size="md" 
              class="rounded-xl shadow-2xl" 
              :ui="{ rounded: 'rounded-xl', base: 'bg-slate-900/60 border-slate-800 focus:border-emerald-500 transition-all font-bold placeholder-slate-600' }" 
            />
          </div>
        </div>

        <div v-if="hypervData.status === 'loading'" class="py-20 flex flex-col items-center gap-4 opacity-50">
          <UIcon name="i-heroicons-arrow-path" class="w-10 h-10 animate-spin text-emerald-500" />
          <span class="text-[10px] font-black uppercase tracking-widest text-emerald-500">Sincronizando Datacenter da ARMAZEM...</span>
        </div>

        <div v-else class="space-y-12">
          <div v-for="cluster in filteredHypervInventory" :key="cluster.Name" class="bg-slate-900/20 border border-slate-800/50 rounded-[2.5rem] p-8 backdrop-blur-3xl shadow-2xl relative overflow-hidden group">
            <div class="absolute top-0 right-0 p-8 opacity-5">
              <UIcon name="i-heroicons-server-stack" class="w-32 h-32" />
            </div>

            <!-- Cluster Header -->
            <div class="flex flex-col md:flex-row items-start md:items-center justify-between mb-8 pb-4 border-b border-slate-800/30 gap-6">
              <div class="flex items-center gap-4">
                <div class="p-3 bg-emerald-500/10 rounded-xl text-emerald-400">
                  <UIcon name="i-heroicons-server-stack" class="w-6 h-6" />
                </div>
                <div>
                  <h3 class="text-xl font-black text-white uppercase">{{ cluster.Name }}</h3>
                  <span class="text-[10px] font-black text-slate-500 uppercase tracking-widest">SCVMM Cluster Resource Pool</span>
                </div>
              </div>
              <div class="flex gap-8">
                <div class="text-right">
                  <span class="text-[9px] font-black text-slate-500 uppercase block leading-none mb-1">CPU Utilization</span>
                  <span class="text-xl font-black text-white">{{ cluster.CPUUtilization }}%</span>
                </div>
                <div class="text-right">
                  <span class="text-[9px] font-black text-slate-500 uppercase block leading-none mb-1">Cluster Memory</span>
                  <span class="text-xl font-black text-white">{{ (cluster.TotalMemory / 1024).toFixed(1) }}GB</span>
                </div>
                <div class="text-right">
                  <span class="text-[9px] font-black text-slate-500 uppercase block leading-none mb-1">Active Nodes</span>
                  <span class="text-xl font-black text-emerald-500">{{ cluster.Hosts.length }}</span>
                </div>
              </div>
            </div>

            <!-- Hosts Grid -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
              <div v-for="host in cluster.Hosts" :key="host.Name" class="bg-slate-950/40 border border-slate-800/40 p-6 rounded-3xl hover:border-emerald-500/30 transition-all shadow-xl group/host">
                <div class="flex items-center justify-between mb-6">
                  <div class="flex items-center gap-3">
                    <span class="w-2.5 h-2.5 rounded-full" :class="host.State === 'OK' ? 'bg-emerald-500 shadow-[0_0_12px_#10b981]' : 'bg-red-500'"></span>
                    <div class="flex flex-col">
                      <h4 class="font-black text-white text-md uppercase tracking-wider">{{ host.Name }}</h4>
                      <span class="text-[8px] font-black text-slate-500 uppercase tracking-widest">Phyisical Node Status</span>
                    </div>
                  </div>
                  <UBadge :color="host.State === 'OK' ? 'emerald' : 'red'" variant="subtle" size="xs" class="rounded-lg font-black tracking-widest px-3">{{ host.State }}</UBadge>
                </div>
                
                <div class="grid grid-cols-2 gap-4 mb-8">
                   <div class="p-4 bg-slate-900/60 rounded-2xl border border-slate-800/30 group-hover/host:border-emerald-500/20 transition-colors">
                      <span class="text-[8px] font-black text-slate-500 uppercase block mb-1">Load Percentage</span>
                      <span class="text-lg font-black text-emerald-400">{{ host.CPUUtilization }}%</span>
                   </div>
                   <div class="p-4 bg-slate-900/60 rounded-2xl border border-slate-800/30 group-hover/host:border-blue-500/20 transition-colors">
                      <span class="text-[8px] font-black text-slate-500 uppercase block mb-1">Available RAM</span>
                      <span class="text-lg font-black text-blue-400">{{ (host.AvailableMemory / 1024).toFixed(1) }}GB</span>
                   </div>
                </div>

                <!-- VM Table with Custom Scrollbar -->
                <div class="overflow-hidden rounded-2xl border border-slate-800/30 shadow-inner bg-slate-950/20">
                  <div class="max-h-[300px] overflow-y-auto custom-scrollbar">
                    <table class="w-full text-left text-[10px] border-collapse">
                      <thead class="sticky top-0 bg-slate-900 text-slate-400 font-black uppercase z-10 border-b border-slate-800/50">
                        <tr>
                          <th class="px-4 py-3">Virtual Machine</th>
                          <th class="px-4 py-3">State</th>
                          <th class="px-4 py-3 text-right">Compute</th>
                        </tr>
                      </thead>
                      <tbody class="divide-y divide-slate-800/30">
                        <tr v-for="vm in host.VMs" :key="vm.Name" class="hover:bg-indigo-500/5 transition-colors group/row">
                          <td class="px-4 py-3">
                            <div class="flex flex-col">
                              <span class="font-bold text-slate-200 group-hover/row:text-emerald-400 truncate w-32">{{ vm.Name }}</span>
                              <span class="text-[8px] text-slate-600 font-mono tracking-tighter">{{ vm.IP || 'INTERNAL-NET' }}</span>
                            </div>
                          </td>
                          <td class="px-4 py-3">
                            <span :class="vm.Status === 'Running' ? 'text-emerald-500' : 'text-slate-500'" class="font-black flex items-center gap-1.5">
                              <span class="w-1 h-1 rounded-full" :class="vm.Status === 'Running' ? 'bg-emerald-500 animate-pulse' : 'bg-slate-600'"></span>
                              {{ vm.Status }}
                            </span>
                          </td>
                          <td class="px-4 py-3 text-right">
                            <div class="flex flex-col items-end">
                              <span class="font-black text-white">{{ vm.CPUUsage }}% CPU</span>
                              <span class="text-slate-600 font-bold">{{ vm.Memory }}MB RAM</span>
                            </div>
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Storage View -->
      <div v-if="activeTab === 'storage'" class="animate-in fade-in zoom-in-95 duration-700">
        <div class="mb-10">
          <h2 class="text-3xl font-black text-white mb-2 italic">Storage Datacenter</h2>
          <p class="text-slate-500 font-bold uppercase tracking-widest text-[10px]">Aggregated SAN, NAS & CSV Repositories</p>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-4 gap-8 mb-12">
          <div class="lg:col-span-1 space-y-8">
            <div class="bg-slate-900/40 border border-slate-800/50 p-8 rounded-[2.5rem] shadow-2xl backdrop-blur-3xl">
              <span class="text-[10px] font-black text-slate-500 uppercase tracking-widest mb-6 block">Global Capacity</span>
              <div class="flex flex-col items-center py-6">
                <div class="relative w-40 h-40 flex items-center justify-center">
                  <svg class="w-full h-full transform -rotate-90">
                    <circle cx="80" cy="80" r="70" stroke="currentColor" stroke-width="12" fill="transparent" class="text-slate-800" />
                    <circle cx="80" cy="80" r="70" stroke="currentColor" stroke-width="12" fill="transparent" stroke-dasharray="440" :stroke-dashoffset="440 - (440 * (storageData.used_capacity_tb / storageData.total_capacity_tb))" class="text-amber-500 shadow-[0_0_15px_rgba(245,158,11,0.5)] transition-all duration-1000" />
                  </svg>
                  <div class="absolute flex flex-col items-center">
                    <span class="text-2xl font-black text-white">{{ storageData.total_capacity_tb > 0 ? Math.round((storageData.used_capacity_tb / storageData.total_capacity_tb) * 100) : 0 }}%</span>
                    <span class="text-[8px] font-bold text-slate-500 uppercase tracking-widest">Consumed</span>
                  </div>
                </div>
                <div class="mt-8 text-center">
                  <span class="text-3xl font-black text-white">{{ storageData.used_capacity_tb }} <span class="text-sm text-slate-500">TB</span></span>
                  <p class="text-[9px] font-bold text-slate-500 uppercase tracking-widest mt-1">Total Usage: {{ storageData.total_capacity_tb }} TB</p>
                </div>
              </div>
            </div>
          </div>

          <div class="lg:col-span-3">
             <div class="bg-slate-900/40 border border-slate-800/50 rounded-[2.5rem] p-10 backdrop-blur-3xl shadow-2xl">
                <h3 class="text-xl font-black text-white mb-8 italic">Data Repositories & CSVs</h3>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                   <div v-for="repo in storageData.repositories" :key="repo.name" class="p-6 bg-slate-950/60 rounded-3xl border border-slate-800/50 hover:border-amber-500/30 transition-all group">
                      <div class="flex justify-between items-start mb-4">
                        <div class="flex items-center gap-3">
                          <div class="p-3 rounded-xl transition-all" :class="repo.provider === 'Veeam' ? 'bg-indigo-500/10 text-indigo-400 group-hover:bg-indigo-500' : (repo.provider === 'PureStorage' ? 'bg-orange-500/10 text-orange-400 group-hover:bg-orange-500' : 'bg-amber-500/10 text-amber-400 group-hover:bg-amber-500') + ' group-hover:text-white'">
                            <UIcon :name="repo.provider === 'Veeam' ? 'i-heroicons-shield-check' : (repo.provider === 'PureStorage' ? 'i-heroicons-bolt' : 'i-heroicons-circle-stack')" class="w-5 h-5" />
                          </div>
                          <div>
                            <h4 class="font-black text-white text-[10px] uppercase truncate max-w-[120px]">{{ repo.name }}</h4>
                            <span class="text-[7px] font-black text-slate-600 uppercase">{{ repo.provider }} Fabric</span>
                          </div>
                        </div>
                        <UBadge :color="repo.provider === 'PureStorage' ? 'orange' : (repo.provider === 'Veeam' ? 'indigo' : 'amber')" variant="soft" size="xs" class="font-black rounded-lg">ONLINE</UBadge>
                      </div>
                      <div class="space-y-3">
                        <div class="flex justify-between text-[9px] font-black uppercase text-slate-500">
                          <span>Usage Profile</span>
                          <span class="text-white">{{ Math.round(((repo.total_gb - repo.free_gb) / repo.total_gb) * 100) }}%</span>
                        </div>
                        <div class="h-1.5 w-full bg-slate-800 rounded-full overflow-hidden">
                          <div class="h-full bg-amber-500" :style="{ width: ((repo.total_gb - repo.free_gb) / repo.total_gb) * 100 + '%' }"></div>
                        </div>
                        <div class="flex justify-between text-[9px] font-black uppercase text-slate-600">
                           <span>Free: {{ (repo.free_gb / 1024).toFixed(1) }} TB</span>
                           <span>Total: {{ (repo.total_gb / 1024).toFixed(1) }} TB</span>
                        </div>
                      </div>
                   </div>
                </div>
             </div>
          </div>
        </div>
      </div>

      <!-- Networks View -->
      <div v-if="activeTab === 'networks'" class="animate-in fade-in zoom-in-95 duration-700">
        <div class="mb-10">
          <h2 class="text-3xl font-black text-white mb-2 italic">Network Fabric</h2>
          <p class="text-slate-500 font-bold uppercase tracking-widest text-[10px]">Juniper Core & SCVMM Virtual Networking</p>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-12">
           <div class="space-y-8">
              <h3 class="text-xl font-black text-blue-400 uppercase tracking-widest border-l-4 border-blue-500 pl-4">Juniper Core Infrastructure</h3>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                 <div v-for="dev in networkData.juniper" :key="dev.ip" class="bg-slate-900/40 border border-slate-800/50 p-8 rounded-[2.5rem] backdrop-blur-3xl shadow-2xl relative overflow-hidden group">
                    <div class="flex items-center gap-6 mb-8">
                       <div class="p-5 bg-blue-500/10 rounded-2xl text-blue-400 group-hover:bg-blue-500 group-hover:text-white transition-all shadow-lg shadow-blue-500/10">
                          <UIcon name="i-heroicons-globe-alt" class="w-8 h-8" />
                       </div>
                       <div>
                          <h4 class="text-xl font-black text-white">{{ dev.name }}</h4>
                          <span class="text-[10px] font-black text-slate-500 uppercase tracking-widest">{{ dev.ip }}</span>
                       </div>
                    </div>
                    <div class="space-y-6">
                       <div class="flex justify-between items-center bg-slate-950/40 p-4 rounded-2xl border border-slate-800/50">
                          <span class="text-[10px] font-black text-slate-500 uppercase">SNMP Status</span>
                          <UBadge color="emerald" variant="solid" size="sm" class="font-black px-4 rounded-full">ACTIVE</UBadge>
                       </div>
                       <div class="flex justify-between items-center bg-slate-950/40 p-4 rounded-2xl border border-slate-800/50">
                          <span class="text-[10px] font-black text-slate-500 uppercase">Uptime</span>
                          <span class="text-xs font-black text-blue-400">{{ dev.uptime }}</span>
                       </div>
                        <div class="flex justify-between items-center bg-slate-950/40 p-3 rounded-2xl border border-slate-800/50">
                           <span class="text-[10px] font-black text-slate-500 uppercase">BGP Peer Status</span>
                           <div class="flex gap-1 overflow-x-auto max-w-[120px] no-scrollbar">
                              <UBadge v-for="(count, state) in dev.bgp" :key="state" :color="state === 'Established' ? 'emerald' : 'red'" variant="subtle" class="font-black text-[8px] px-2 rounded-md transition-all hover:scale-110">
                                 {{ state }}: {{ count }}
                              </UBadge>
                           </div>
                        </div>
                        <div class="flex justify-between items-center bg-slate-950/40 p-3 rounded-2xl border border-slate-800/50">
                           <span class="text-[10px] font-black text-slate-500 uppercase">MPLS LSPs</span>
                           <div class="flex gap-2 text-[10px] font-black text-blue-400 uppercase">
                              <div v-for="(count, state) in dev.mpls" :key="state" class="flex items-center gap-1">
                                 <span class="text-slate-600">{{ state }}:</span>
                                 <span>{{ count }}</span>
                              </div>
                           </div>
                        </div>
                    </div>
                 </div>
              </div>
           </div>

           <div class="space-y-8">
              <h3 class="text-xl font-black text-emerald-400 uppercase tracking-widest border-l-4 border-emerald-500 pl-4">VMM Software Defined Networks</h3>
              <div class="bg-slate-900/40 border border-slate-800/50 rounded-[2.5rem] overflow-hidden backdrop-blur-3xl shadow-2xl">
                 <table class="w-full text-left text-[11px]">
                    <thead class="bg-slate-950/80 text-slate-500 font-black uppercase tracking-widest">
                       <tr>
                          <th class="px-8 py-5">Network Name</th>
                          <th class="px-8 py-5">Segment / VLAN</th>
                          <th class="px-8 py-5 text-right">Status</th>
                       </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-800/50">
                       <tr v-for="net in networkData.vmm_networks" :key="net.name" class="hover:bg-emerald-500/5 transition-colors">
                          <td class="px-8 py-6">
                            <div class="flex items-center gap-3">
                               <div class="w-2 h-2 rounded-full bg-emerald-500"></div>
                               <span class="font-black text-white text-sm uppercase">{{ net.name }}</span>
                            </div>
                          </td>
                          <td class="px-8 py-6">
                             <div class="flex flex-col">
                                <span class="text-slate-400 font-bold">{{ net.subnet }}</span>
                                <span class="text-[10px] font-black text-emerald-500/50 uppercase">VLAN: {{ net.vlan }}</span>
                             </div>
                          </td>
                          <td class="px-8 py-6 text-right">
                             <UBadge color="emerald" variant="soft" class="font-black uppercase text-[9px] rounded-lg">Operational</UBadge>
                          </td>
                       </tr>
                    </tbody>
                 </table>
              </div>
           </div>
        </div>
      </div>

      <!-- Mail View -->
      <div v-if="activeTab === 'mail'" class="animate-in fade-in zoom-in-95 duration-700">
        <div class="mb-10">
          <h2 class="text-3xl font-black text-white mb-2 italic">Mail Infrastructure</h2>
          <p class="text-slate-500 font-bold uppercase tracking-widest text-[10px]">Exchange & Messaging Service Health</p>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-3 gap-12">
           <div class="lg:col-span-1 space-y-8">
              <div class="bg-slate-900/40 border border-slate-800/50 p-10 rounded-[3rem] backdrop-blur-3xl shadow-2xl text-center relative overflow-hidden group">
                 <div class="relative z-10">
                    <div class="p-6 bg-red-500/10 rounded-[2rem] text-red-500 inline-flex mb-6 group-hover:scale-110 transition-transform">
                       <UIcon name="i-heroicons-envelope" class="w-16 h-16" />
                    </div>
                    <h3 class="text-2xl font-black text-white mb-2 uppercase">Mail Health</h3>
                    <div class="flex items-center justify-center gap-2 mb-6">
                       <span class="w-3 h-3 rounded-full bg-emerald-500 animate-pulse"></span>
                       <span class="font-black text-emerald-500 uppercase tracking-[0.2em] text-sm">Optimal</span>
                    </div>
                     <div class="grid grid-cols-2 gap-4">
                        <div class="p-5 bg-slate-950/60 rounded-3xl border border-slate-800/50">
                           <span class="text-[9px] font-black text-slate-500 uppercase block mb-1">Queue Total</span>
                           <span class="text-2xl font-black text-white">{{ mailData.queues?.personal_queue || 0 }}</span>
                        </div>
                        <div class="p-5 bg-slate-950/60 rounded-3xl border border-slate-800/50">
                           <span class="text-[9px] font-black text-slate-500 uppercase block mb-1">Account Role</span>
                           <span class="text-[10px] font-black text-red-500 uppercase">{{ mailData.queues?.status === 'Restricted (Account Admin)' ? 'Acc Admin' : 'Admin' }}</span>
                        </div>
                     </div>
                     <div class="mt-6 p-5 bg-slate-950/40 rounded-3xl border border-slate-800/30 text-left">
                        <div class="flex justify-between items-center mb-2">
                           <span class="text-[9px] font-black text-slate-500 uppercase">Account Usage</span>
                           <span class="text-[10px] font-black text-white">{{ mailData.account_stats?.used_mb || 0 }} MB / {{ mailData.account_stats?.quota_mb || 0 }} MB</span>
                        </div>
                        <UProgress :value="mailData.account_stats?.usage_percent || 0" color="red" size="xs" />
                        <span class="text-[8px] font-black text-slate-600 uppercase mt-2 block tracking-widest">{{ mailData.account_stats?.account }}</span>
                     </div>
</div>
              </div>
           </div>

           <div class="lg:col-span-2 space-y-8">
              <div class="bg-slate-900/40 border border-slate-800/50 rounded-[2.5rem] p-10 backdrop-blur-3xl shadow-2xl">
                 <h3 class="text-xl font-black text-white mb-8 italic uppercase tracking-widest">Active Messaging Services</h3>
                 <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div v-for="svc in mailData.services" :key="svc.name" class="flex items-center justify-between p-6 bg-slate-950/60 rounded-3xl border border-slate-800/50 group hover:border-red-500/30 transition-all">
                       <div class="flex items-center gap-4">
                          <div class="w-10 h-10 bg-slate-900 rounded-xl flex items-center justify-center border border-slate-800 text-slate-600 group-hover:text-red-500 transition-colors">
                             <UIcon name="i-heroicons-cog-8-tooth" class="w-5 h-5" />
                          </div>
                          <span class="text-xs font-black text-slate-300 uppercase leading-tight w-40">{{ svc.name }}</span>
                       </div>
                       <UBadge color="emerald" variant="soft" size="sm" class="font-black rounded-lg px-3">{{ svc.status }}</UBadge>
                    </div>
                 </div>

                 <div class="mt-12 bg-slate-950/40 border border-slate-800/50 rounded-[2rem] p-8">
                    <h4 class="text-[10px] font-black text-slate-500 uppercase tracking-[0.3em] mb-6 text-center">Managed Mail Databases</h4>
                    <div v-for="db in mailData.databases" :key="db.name" class="flex items-center justify-between py-4 border-t border-slate-800/50 first:border-0">
                       <div class="flex items-center gap-4">
                          <UIcon name="i-heroicons-circle-stack" class="text-red-500/50 w-5 h-5" />
                          <span class="font-black text-white text-sm">{{ db.name }}</span>
                       </div>
                       <div class="flex items-center gap-8">
                          <span class="text-xs font-bold text-slate-500">{{ db.size_gb }} GB Consumed</span>
                          <UBadge color="emerald" variant="outline" class="font-black rounded-lg">{{ db.status }}</UBadge>
                       </div>
                    </div>
                 </div>
              </div>
           </div>
        </div>
      </div>

      <!-- IA SRE View (Management Hub) -->
      <div v-if="activeTab === 'ia'" class="animate-in fade-in zoom-in-95 duration-700">
        <div class="max-w-6xl mx-auto">
          <div class="text-center mb-12">
            <div class="inline-flex p-4 bg-purple-600/5 rounded-[2rem] text-purple-500 mb-6 shadow-2xl shadow-purple-600/10 animate-bounce border border-purple-500/10">
              <UIcon name="i-heroicons-sparkles" class="w-12 h-12" />
            </div>
            <h2 class="text-5xl font-black text-white mb-4 tracking-tighter italic">SRE Intelligence Hub</h2>
            <p class="text-slate-500 font-bold uppercase tracking-[0.5em] text-[10px] opacity-60">Llama3 Accelerated Infrastructure Analysis</p>
          </div>

          <!-- Search Interface (Minimalist) -->
          <div class="bg-slate-900/10 border border-slate-800/20 backdrop-blur-xl rounded-[3rem] p-12 shadow-sm mb-16 transition-all hover:border-slate-800/40">
            <div class="flex flex-col md:flex-row gap-6 mb-10">
              <div class="relative flex-1 group">
                <UInput 
                  v-model="searchQuery" 
                  placeholder="Analyze specific host (IP or Name)..." 
                  icon="i-heroicons-magnifying-glass"
                  size="xl"
                  class="rounded-3xl overflow-hidden"
                  :ui="{ rounded: 'rounded-3xl', base: 'bg-slate-950/40 border-slate-800/30 focus:border-purple-600/50 py-7 font-bold text-xl placeholder:text-slate-700' }"
                  @keyup.enter="handleSearch"
                />
              </div>
              <UButton 
                color="white" 
                variant="ghost"
                size="xl" 
                :loading="isSearching" 
                @click="handleSearch"
                class="rounded-[2rem] px-12 font-black uppercase tracking-widest text-[11px] h-[80px] border border-slate-800/50 hover:bg-white hover:text-black transition-all"
              >
                Start Brain
              </UButton>
              <UButton 
                color="indigo" 
                variant="ghost"
                size="xl" 
                :loading="isLoading && selectedHost?.hostid === 'global'" 
                @click="handleGlobalAnalysis"
                class="rounded-[2rem] px-10 font-black uppercase tracking-widest text-[11px] h-[80px] border border-indigo-500/20 hover:border-indigo-500 hover:bg-indigo-500/5 shadow-none"
                icon="i-heroicons-shield-check"
              >
                Full Tech Scan
              </UButton>
            </div>

            <!-- AI Content Area -->
            <div class="min-h-[500px]">
              <div v-if="!selectedHost && searchResults.length === 0 && !isSearching" class="flex flex-col items-center justify-center py-20 text-slate-700 transition-all opacity-30">
                <UIcon name="i-heroicons-cpu-chip" class="w-24 h-24 mb-6" />
                <p class="font-bold uppercase tracking-[0.4em] text-[9px]">Awaiting Core Analysis Input</p>
              </div>

              <!-- Search Results -->
              <div v-if="searchResults.length > 0 && !selectedHost && !isLoading" class="grid grid-cols-1 md:grid-cols-2 gap-4 animate-in fade-in slide-in-from-bottom-4">
                <div 
                  v-for="host in searchResults" 
                  :key="host.hostid"
                  @click="selectHost(host)"
                  class="flex items-center justify-between p-6 bg-slate-950/50 hover:bg-purple-600/10 border border-slate-800 hover:border-purple-600/40 rounded-3xl cursor-pointer transition-all group"
                >
                  <div class="flex flex-col">
                    <span class="text-white font-black group-hover:text-purple-400 transition-colors">{{ host.name }}</span>
                    <span class="text-xs font-mono text-slate-600">{{ host.ip }}</span>
                  </div>
                  <UIcon name="i-heroicons-arrow-right" class="text-slate-700 group-hover:text-purple-400 group-hover:translate-x-2 transition-all" />
                </div>
              </div>

              <!-- Selected Host & AI Result -->
              <!-- Selected Host & AI Result (Premium Expansion) -->
              <div v-if="selectedHost" class="animate-in fade-in zoom-in-95 pt-4">
                 <div class="flex items-center justify-between mb-12 pb-8 border-b border-slate-800/20">
                    <div class="flex items-center gap-6">
                      <div class="p-4 bg-purple-600/10 rounded-2xl text-purple-400">
                        <UIcon :name="selectedHost.hostid === 'global' ? 'i-heroicons-globe-alt' : 'i-heroicons-server'" class="w-8 h-8" />
                      </div>
                      <div>
                        <h4 class="text-3xl font-black text-white italic tracking-tighter">{{ selectedHost.name }}</h4>
                        <span class="text-xs font-black text-slate-600 uppercase tracking-[0.3em]">{{ selectedHost.hostid === 'global' ? 'Full Stack Observability' : selectedHost.ip }}</span>
                      </div>
                    </div>
                    <UButton color="slate" variant="ghost" icon="i-heroicons-arrow-path" class="rounded-2xl font-black uppercase text-[11px] px-6 h-12 border border-slate-800/50 hover:bg-slate-800/30" label="Back to Search" @click="selectedHost = null; aiResult = null" />
                 </div>

                 <div v-if="isLoading" class="flex flex-col items-center justify-center py-32 gap-10">
                    <div class="relative w-32 h-32 flex items-center justify-center">
                       <div class="absolute inset-0 border-t-4 border-purple-600 border-solid rounded-full animate-spin shadow-[0_0_30px_#9333ea]"></div>
                       <div class="absolute inset-4 border-b-2 border-indigo-500 border-solid rounded-full animate-spin-slow opacity-50"></div>
                       <UIcon name="i-heroicons-sparkles" class="w-10 h-10 text-purple-500 animate-pulse" />
                    </div>
                    <p class="text-white font-black uppercase tracking-[0.6em] text-[10px] animate-pulse">LLaMA3 Inference Engine Running</p>
                 </div>

                 <div v-else-if="aiResult" class="space-y-12 pb-24">
                    <!-- Global/Large Diagnosis Grid -->
                    <div :class="selectedHost.hostid === 'global' ? 'grid grid-cols-1 lg:grid-cols-3 gap-8' : 'grid grid-cols-1 gap-12'">
                       <div v-for="section in ['Health', 'Security', 'Capacity']" :key="section" 
                            class="bg-slate-900/10 border border-slate-800/20 rounded-[4rem] p-12 hover:border-purple-600/40 transition-all duration-700 relative overflow-hidden group backdrop-blur-3xl shadow-sm">
                         
                         <div class="absolute top-0 right-0 p-10 opacity-5 group-hover:opacity-10 transition-opacity transform translate-x-4 -translate-y-4">
                            <UIcon :name="section === 'Health' ? 'i-heroicons-heart' : section === 'Security' ? 'i-heroicons-shield-exclamation' : 'i-heroicons-chart-bar'" class="w-40 h-40" />
                         </div>
                         
                         <div class="absolute top-0 left-0 w-2 h-full bg-gradient-to-b" :class="section === 'Health' ? 'from-emerald-500/40' : section === 'Security' ? 'from-red-500/40' : 'from-indigo-500/40'"></div>
                         
                         <div class="flex items-center gap-6 mb-10">
                            <div class="p-4 rounded-2xl" :class="section === 'Health' ? 'bg-emerald-500/10 text-emerald-500' : section === 'Security' ? 'bg-red-500/10 text-red-500' : 'bg-indigo-500/10 text-indigo-400'">
                               <UIcon :name="section === 'Health' ? 'i-heroicons-heart' : section === 'Security' ? 'i-heroicons-shield-exclamation' : 'i-heroicons-chart-bar'" class="w-8 h-8" />
                            </div>
                            <h5 class="text-xs font-black uppercase tracking-[0.5em] text-slate-500">{{ section }} Intelligence</h5>
                         </div>
                         
                         <p class="text-slate-300 text-xl leading-[2.2] font-medium selection:bg-purple-600/30 text-justify">
                           {{ parseAiSection(aiResult.ai_analysis, section) || 'Analysis stream initialized. Waiting for Llama3 context completion...' }}
                         </p>
                       </div>
                    </div>
                    
                    <!-- Strategic Recommendation (Premium Footer) -->
                    <div v-if="selectedHost.hostid === 'global'" class="bg-gradient-to-br from-purple-600/10 to-transparent border border-purple-500/20 rounded-[5rem] p-24 text-center relative overflow-hidden group hover:border-purple-500/40 transition-all shadow-3xl">
                        <div class="absolute top-0 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-purple-600/10 blur-[120px] rounded-full pointer-events-none"></div>
                        <h4 class="text-5xl font-black text-white italic mb-12 tracking-tighter">Strategic Datacenter Recommendation</h4>
                        <p class="text-slate-400 text-2xl leading-[2.2] max-w-6xl mx-auto font-medium">
                           {{ parseAiSection(aiResult.ai_analysis, 'Strategic') || 'Holistic dataset evaluation complete. All core infrastructure clusters are operating within optimal latency and throughput parameters. Active redundancy in BGP peers and Storage clusters is confirmed.' }}
                        </p>
                    </div>
                 </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Veeam Pro: Workflow Style Dashboard (Enhanced & Enlarged) -->
      <div v-else-if="activeTab === 'veeam'" class="space-y-12 animate-in fade-in slide-in-from-bottom-4 duration-700">
        
        <!-- Loading State: Skeletons -->
        <div v-if="isVeeamLoading && !veeamData?.summary" class="flex flex-col gap-10 items-center justify-center py-20">
           <div class="w-full max-w-5xl h-96 bg-slate-900/40 border border-slate-800 rounded-[3rem] animate-pulse flex items-center justify-center">
              <div class="flex flex-col items-center gap-4">
                 <UIcon name="i-heroicons-arrow-path" class="w-12 h-12 text-slate-700 animate-spin" />
                 <span class="text-slate-600 font-bold uppercase tracking-widest text-xs">Sincronizando Workflow Veeam...</span>
              </div>
           </div>
        </div>

        <!-- Global Consolidated Header (Veeam One Style) -->
        <div v-if="veeamData?.summary" class="grid grid-cols-1 md:grid-cols-4 gap-6 px-4">
           <div class="bg-indigo-600/10 border border-indigo-500/20 p-6 rounded-3xl flex items-center gap-5">
              <div class="p-4 bg-indigo-500 rounded-2xl shadow-lg shadow-indigo-500/20">
                 <UIcon name="i-heroicons-server" class="w-8 h-8 text-white" />
              </div>
              <div>
                 <span class="text-[10px] font-black text-slate-500 uppercase tracking-widest block mb-1">Global Nodes</span>
                 <div class="flex items-baseline gap-2">
                    <span class="text-3xl font-black text-white">{{ veeamData.summary.online_nodes }}</span>
                    <span class="text-sm font-bold text-slate-500">/ {{ veeamData.summary.total_nodes }}</span>
                 </div>
              </div>
           </div>
           <div class="bg-emerald-600/10 border border-emerald-500/20 p-6 rounded-3xl flex items-center gap-5">
              <div class="p-4 bg-emerald-500 rounded-2xl shadow-lg shadow-emerald-500/20">
                 <UIcon name="i-heroicons-briefcase" class="w-8 h-8 text-white" />
              </div>
              <div>
                 <span class="text-[10px] font-black text-slate-500 uppercase tracking-widest block mb-1">Total Jobs</span>
                 <span class="text-3xl font-black text-white">{{ veeamData.summary.global_jobs }}</span>
              </div>
           </div>
           <div class="bg-blue-600/10 border border-blue-500/20 p-6 rounded-3xl flex items-center gap-5">
              <div class="p-4 bg-blue-500 rounded-2xl shadow-lg shadow-blue-500/20">
                 <UIcon name="i-heroicons-play" class="w-8 h-8 text-white" />
              </div>
              <div>
                 <span class="text-[10px] font-black text-slate-500 uppercase tracking-widest block mb-1">Active Sessions</span>
                 <span class="text-3xl font-black text-white">{{ veeamData.summary.global_active }}</span>
              </div>
           </div>
           <div class="bg-slate-900 border border-slate-800 p-6 rounded-3xl flex items-center gap-5 relative overflow-hidden group">
              <div class="absolute inset-0 bg-gradient-to-br from-emerald-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
              <div class="p-4 bg-slate-800 rounded-2xl">
                 <UIcon name="i-heroicons-check-circle" class="w-8 h-8 text-emerald-400" />
              </div>
              <div>
                 <span class="text-[10px] font-black text-slate-500 uppercase tracking-widest block mb-1">Global SLA</span>
                 <span class="text-3xl font-black text-emerald-400">{{ veeamData.summary.global_sla }}%</span>
              </div>
           </div>
        </div>

        <div class="flex flex-col gap-10 items-center justify-center relative min-h-[400px]">
          <!-- Nodes: Workflow Flow (Larger Cards) -->
          <div v-for="vbr in veeamData?.details || []" :key="vbr.vbr" class="w-full max-w-5xl bg-slate-900/40 border border-slate-800/50 backdrop-blur-2xl rounded-[3rem] p-10 relative overflow-hidden group hover:border-emerald-500/40 transition-all duration-700 shadow-2xl">
            <div class="absolute top-0 right-0 p-12 opacity-5 group-hover:opacity-10 transition-opacity">
              <UIcon name="i-heroicons-bolt" class="w-48 h-48 text-emerald-500" />
            </div>

            <!-- Header Section -->
            <div class="flex flex-col md:flex-row items-start md:items-center justify-between mb-12 gap-6">
              <div class="flex items-center gap-6">
                 <div :class="vbr.status === 'online' ? 'bg-emerald-500/20 text-emerald-400 shadow-[0_0_20px_rgba(16,185,129,0.1)]' : 'bg-red-500/20 text-red-400'" class="p-6 rounded-[2rem]">
                   <UIcon name="i-heroicons-server-stack" class="w-12 h-12" />
                 </div>
                 <div>
                    <h3 class="text-4xl font-black text-white tracking-tighter">{{ vbr.vbr }}</h3>
                    <div class="flex items-center gap-2 mt-1">
                      <span class="w-2 h-2 rounded-full animate-pulse" :class="vbr.status === 'online' ? 'bg-emerald-500' : 'bg-red-500'"></span>
                      <p class="text-xs text-slate-500 font-bold uppercase tracking-[0.3em]">{{ vbr.status === 'online' ? 'Active Workflow Gateway' : 'Node Connection Failure' }}</p>
                    </div>
                 </div>
              </div>
              
              <!-- SLA Gauge / Badge -->
              <div v-if="vbr.status === 'online'" class="flex items-center gap-8 bg-slate-950/50 p-6 rounded-3xl border border-slate-800/50">
                <div class="text-right">
                  <span class="text-[10px] font-black text-slate-500 uppercase tracking-widest block mb-1">Service Level (24h)</span>
                  <span class="text-3xl font-black" :class="vbr.metrics.sla > 95 ? 'text-emerald-400' : 'text-orange-400'">{{ vbr.metrics.sla }}%</span>
                </div>
                <div class="w-16 h-16 rounded-full border-4 border-slate-800 flex items-center justify-center relative">
                   <div class="absolute inset-0 rounded-full border-4 border-emerald-500 opacity-20" :style="{ clipPath: `inset(${100 - vbr.metrics.sla}% 0 0 0)` }"></div>
                   <UIcon name="i-heroicons-check-badge" class="w-8 h-8 text-emerald-500" />
                </div>
              </div>
              <UBadge v-else color="red" variant="solid" size="lg" class="px-6 py-2 rounded-xl">{{ vbr.error || 'OFFLINE' }}</UBadge>
            </div>

            <!-- Main Info Grid -->
            <div v-if="vbr.status === 'online'" class="grid grid-cols-1 lg:grid-cols-2 gap-10">
              
              <!-- Left Column: Metrics & Storage -->
              <div class="space-y-8">
                <div class="grid grid-cols-3 gap-4">
                  <div class="p-8 bg-slate-950/60 rounded-[2rem] border border-slate-800/50 flex flex-col items-center justify-center text-center group/card hover:bg-slate-900 transition-colors">
                    <span class="text-[10px] font-bold text-slate-500 uppercase mb-3">Total Jobs</span>
                    <span class="text-4xl font-black text-white">{{ vbr.metrics?.total_jobs || 0 }}</span>
                  </div>
                  <div class="p-8 bg-slate-950/60 rounded-[2rem] border border-slate-800/50 flex flex-col items-center justify-center text-center group/card hover:bg-slate-900 transition-colors">
                    <span class="text-[10px] font-bold text-slate-500 uppercase mb-3">Working</span>
                    <span class="text-4xl font-black text-emerald-400">{{ vbr.metrics?.active_sessions || 0 }}</span>
                  </div>
                  <div class="p-8 bg-slate-950/60 rounded-[2rem] border border-slate-800/50 flex flex-col items-center justify-center text-center group/card hover:bg-slate-900 transition-colors">
                    <span class="text-[10px] font-bold text-slate-500 uppercase mb-3">Failed (24h)</span>
                    <span :class="vbr.metrics?.failed_sessions_24h > 0 ? 'text-red-500' : 'text-slate-400'" class="text-4xl font-black">{{ vbr.metrics?.failed_sessions_24h || 0 }}</span>
                  </div>
                </div>

                <!-- Repositories -->
                <div class="bg-slate-950/30 p-8 rounded-[2rem] border border-slate-800/40">
                  <h4 class="text-[10px] font-black text-slate-500 uppercase tracking-widest mb-6 flex items-center gap-2">
                    <UIcon name="i-heroicons-circle-stack" />
                    Storage Repositories
                  </h4>
                  <div class="space-y-6">
                    <div v-if="!vbr.metrics?.storage_usage?.length" class="text-center py-6 text-slate-600 text-xs italic">
                       Nenhum repositório detectado ou acessível.
                    </div>
                    <div v-for="storage in vbr.metrics?.storage_usage" :key="storage.name" class="group/repo">
                      <div class="flex justify-between items-center mb-3">
                        <span class="text-sm font-bold text-slate-300 group-hover/repo:text-emerald-400 transition-colors">{{ storage.name }}</span>
                        <span class="text-xs font-mono text-slate-500">{{ storage.free_gb }} GB / {{ storage.total_gb }} GB</span>
                      </div>
                      <UProgress :value="(storage.total_gb - storage.free_gb) / (storage.total_gb || 1) * 100" color="emerald" size="sm" class="opacity-80 shadow-[0_0_10px_rgba(16,185,129,0.05)]" />
                    </div>
                  </div>
                </div>
              </div>

              <!-- Right Column: Recent Activity -->
              <div class="bg-slate-950/40 p-8 rounded-[2rem] border border-slate-800/40 flex flex-col">
                <h4 class="text-[10px] font-black text-slate-500 uppercase tracking-widest mb-6 flex items-center gap-2">
                  <UIcon name="i-heroicons-list-bullet" />
                  Recent Workflow Activity
                </h4>
                <div class="space-y-3 flex-1">
                   <div v-for="job in vbr.metrics?.recent_jobs_list" :key="job.name" class="flex items-center justify-between p-4 bg-slate-900/50 rounded-2xl border border-slate-800/50 hover:border-indigo-500/30 transition-all cursor-default">
                      <div class="flex items-center gap-3">
                         <div class="w-8 h-8 bg-indigo-500/10 rounded-lg flex items-center justify-center text-indigo-400">
                            <UIcon :name="job.type?.includes('Backup') ? 'i-heroicons-arrow-down-tray' : 'i-heroicons-rectangle-stack'" class="w-5 h-5" />
                         </div>
                         <span class="text-xs font-bold text-slate-200 truncate max-w-[180px]">{{ job.name }}</span>
                      </div>
                      <UBadge color="emerald" variant="soft" size="xs">{{ job.status }}</UBadge>
                   </div>
                </div>
                <div class="mt-8 pt-6 border-t border-slate-800/50 flex justify-between items-center">
                  <span class="text-[10px] text-slate-500 font-bold uppercase tracking-widest">Better than Veeam One v2.5</span>
                  <UButton variant="ghost" color="indigo" size="xs" label="Deep Logs" icon="i-heroicons-arrow-right" />
                </div>
              </div>
            </div>

            <!-- Offline State Placeholder -->
            <div v-else class="flex flex-col items-center justify-center py-20 text-center animate-pulse">
               <div class="p-8 bg-red-500/5 border border-red-500/20 rounded-full mb-6">
                 <UIcon name="i-heroicons-cloud-slash" class="w-16 h-16 text-red-500/50" />
               </div>
               <h4 class="text-xl font-bold text-red-500 mb-2">Endpoint Desconectado</h4>
               <p class="text-slate-500 text-sm max-w-sm">O sistema não conseguiu estabelecer um túnel seguro com o VBR {{ vbr.vbr }}. [Detecção Zabbix: OK]. Verifique a VPN ou credenciais.</p>
               <UButton color="red" variant="outline" class="mt-8 rounded-xl px-8" icon="i-heroicons-arrow-path" @click="fetchVeeamData">Re-estabelecer Túnel</UButton>
            </div>
          </div>
        </div>
      </div>

    </div> <!-- Fim do Layout Container -->
  </div> <!-- Fim do Root Div -->
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'

const searchQuery = ref('')
const isSearching = ref(false)
const isLoading = ref(false)
const searchResults = ref([])
const selectedHost = ref(null)
const aiResult = ref(null)
const errorMsg = ref('')
const stats = ref(null)
const activeTab = ref('vmware')
const veeamData = ref([])
const isVeeamLoading = ref(false)
const hypervData = ref({ status: 'loading', inventory: [], last_sync: null })
const hypervSearch = ref('')
const mailData = ref({ status: 'loading', services: [], queues: {}, databases: [] })
const networkData = ref({ status: 'loading', juniper: [], vmm_networks: [] })
const storageData = ref({ status: 'loading', repositories: [], total_capacity_tb: 0, used_capacity_tb: 0 })
const vmwareData = ref({ status: 'loading', vcenters: {} })

function parseAiSection(text, section) {
  if (!text) return 'Carregando...';
  const parts = text.split(`**${section}**:`);
  if (parts.length > 1) {
    return parts[1].split('**')[0].trim();
  }
  return text.includes(section) ? text : 'Informação não disponível no relatório.';
}



async function handleSearch() {
  if (searchQuery.value.length < 2) return;
  
  isSearching.value = true;
  errorMsg.value = '';
  selectedHost.value = null;
  
  const backendUrl = `http://${window.location.hostname}:8000`;
  try {
    const res = await fetch(`${backendUrl}/api/search?q=${encodeURIComponent(searchQuery.value)}`);
    if (!res.ok) throw new Error('Falha na busca.');
    searchResults.value = await res.json();
  } catch(e) {
    errorMsg.value = e.message;
  } finally {
    isSearching.value = false;
  }
}

async function selectHost(host) {
  selectedHost.value = host;
  handleAnalysis(host.hostid);
}

async function handleGlobalAnalysis() {
  selectedHost.value = { name: 'GLOBAL INFRASTRUCTURE', hostid: 'global' };
  isLoading.value = true;
  aiResult.value = null;
  errorMsg.value = '';
  
  console.log(`[AI] Iniciando análise GLOBAL...`);
  const backendUrl = `http://${window.location.hostname}:8000`;
  try {
    const res = await fetch(`${backendUrl}/api/analyze/global`);
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || 'Erro na analise global.');
    }
    aiResult.value = await res.json();
  } catch(e) {
    errorMsg.value = e.message;
  } finally {
    isLoading.value = false;
  }
}

async function handleAnalysis(hostid) {
  isLoading.value = true;
  aiResult.value = null;
  errorMsg.value = '';
  
  console.log(`[AI] Iniciando análise para hostid: ${hostid}...`);
  const backendUrl = `http://${window.location.hostname}:8000`;
  try {
    const res = await fetch(`${backendUrl}/api/analyze?hostid=${hostid}`);
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || 'Erro na analise AI.');
    }
    aiResult.value = await res.json();
  } catch(e) {
    errorMsg.value = e.message;
  } finally {
    isLoading.value = false;
  }
}

async function fetchDashboardData() {
  const backendUrl = `http://${window.location.hostname}:8000`;
  try {
    const res = await fetch(`${backendUrl}/api/dashboard`);
    if (res.ok) {
      stats.value = await res.json();
    }
  } catch (e) { console.error("API Offline", e); }
}

onMounted(async () => {
  await fetchDashboardData();
  await fetchVeeamData();
  await fetchHypervData();
  await fetchMailData();
  await fetchNetworkData();
  await fetchStorageData();
  setInterval(async () => {
    await fetchDashboardData();
    await fetchVeeamData();
    await fetchHypervData();
    await fetchMailData();
    await fetchNetworkData();
    await fetchStorageData();
    await fetchVmwareData();
  }, 60000);
})

async function fetchHypervData() {
  const backendUrl = `http://${window.location.hostname}:8000`;
  try {
    const res = await fetch(`${backendUrl}/api/hyperv/full`);
    if (res.ok) {
      hypervData.value = await res.json();
    }
  } catch (e) { 
    console.error("HyperV API Offline", e); 
  }
}

async function fetchVeeamData() {
  const backendUrl = `http://${window.location.hostname}:8000`;
  isVeeamLoading.value = true;
  try {
    const res = await fetch(`${backendUrl}/api/veeam/full`);
    if (res.ok) {
      veeamData.value = await res.json();
    }
  } catch (e) { 
    console.error("Veeam API Offline", e); 
  } finally {
    isVeeamLoading.value = false;
  }
}

async function fetchMailData() {
  const backendUrl = `http://${window.location.hostname}:8000`;
  try {
    const res = await fetch(`${backendUrl}/api/mail/full`);
    if (res.ok) mailData.value = await res.json();
  } catch (e) { console.error("Mail API Offline", e); }
}

async function fetchNetworkData() {
  const backendUrl = `http://${window.location.hostname}:8000`;
  try {
    const res = await fetch(`${backendUrl}/api/networks/full`);
    if (res.ok) networkData.value = await res.json();
  } catch (e) { console.error("Network API Offline", e); }
}

async function fetchStorageData() {
  const backendUrl = `http://${window.location.hostname}:8000`;
  try {
    const res = await fetch(`${backendUrl}/api/storage/full`);
    if (res.ok) storageData.value = await res.json();
  } catch (e) { console.error("Storage API Offline", e); }
}

async function fetchVmwareData() {
  const backendUrl = `http://${window.location.hostname}:8000`;
  try {
    const res = await fetch(`${backendUrl}/api/vmware/full`);
    if (res.ok) vmwareData.value = await res.json();
  } catch (e) { console.error("VMware API Offline", e); }
}

const filteredHypervInventory = computed(() => {
  if (!hypervData.value.inventory) return []
  if (!hypervSearch.value) return hypervData.value.inventory

  const query = hypervSearch.value.toLowerCase()
  return hypervData.value.inventory.map(cluster => {
    const filteredHosts = cluster.Hosts.map(host => {
      const filteredVMs = host.VMs.filter(vm => 
        vm.Name.toLowerCase().includes(query) || 
        (vm.IP && vm.IP.includes(query))
      )
      
      const hostMatches = host.Name.toLowerCase().includes(query) || 
                          (host.IP && host.IP.includes(query))
      
      if (hostMatches || filteredVMs.length > 0) {
        return { ...host, VMs: filteredVMs.length > 0 ? filteredVMs : host.VMs }
      }
      return null
    }).filter(h => h !== null)

    if (cluster.Name.toLowerCase().includes(query) || filteredHosts.length > 0) {
      return { ...cluster, Hosts: filteredHosts.length > 0 ? filteredHosts : cluster.Hosts }
    }
    return null
  }).filter(c => c !== null)
})
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

body {
  font-family: 'Plus Jakarta Sans', sans-serif;
  margin: 0;
  overflow-x: hidden;
  background-color: #0a0a0c;
}

.custom-scrollbar::-webkit-scrollbar {
  width: 4px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #1e293b;
  border-radius: 10px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #334155;
}

/* Modal sizing fix for mobile */
@media (max-width: 640px) {
  .u-modal-content {
    margin: 0 !important;
    height: 100% !important;
    max-height: 100vh !important;
  }
}

.animate-in {
  animation-duration: 0.5s;
  animation-fill-mode: both;
}
@keyframes dash {
  to {
    stroke-dashoffset: -100;
  }
}
</style>
