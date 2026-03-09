<template>
  <div class="min-h-screen bg-[#0a0a0c] text-slate-200 font-sans selection:bg-indigo-500/30">
    <!-- Blurring Background Orbs -->
    <div class="fixed inset-0 overflow-hidden pointer-events-none">
      <div class="absolute -top-[10%] -left-[10%] w-[40%] h-[40%] bg-indigo-600/10 blur-[120px] rounded-full"></div>
      <div class="absolute top-[20%] -right-[10%] w-[30%] h-[30%] bg-blue-600/10 blur-[100px] rounded-full"></div>
      <div class="absolute -bottom-[10%] left-[20%] w-[50%] h-[40%] bg-purple-600/10 blur-[150px] rounded-full"></div>
    </div>

    <!-- Layout Container -->
    <div class="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 py-8">
      
      <!-- Header -->
      <header class="flex flex-col md:flex-row justify-between items-start md:items-center gap-6 mb-12 animate-in fade-in slide-in-from-top-4 duration-700">
        <div>
          <div class="flex items-center gap-3 mb-1">
            <div class="p-2 bg-indigo-500 rounded-xl shadow-lg shadow-indigo-500/20">
              <UIcon name="i-heroicons-bolt" class="w-6 h-6 text-white" />
            </div>
            <h1 class="text-3xl sm:text-4xl font-extrabold tracking-tight text-white">
              WARZEM<span class="text-indigo-500">.</span>
            </h1>
          </div>
          <p class="text-slate-400 font-medium text-sm sm:text-base">Infra Intelligence & Automated SRE Analyzer</p>
        </div>

        <div class="flex items-center gap-4 w-full md:w-auto">
          <div class="hidden md:flex flex-col items-end px-4 border-r border-slate-800">
            <span class="text-[10px] uppercase tracking-widest text-slate-500 font-bold">System Status</span>
            <div class="flex items-center gap-2">
              <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
              <span class="text-sm font-semibold text-emerald-500">All Systems Operational</span>
            </div>
          </div>
          <UButton 
            icon="i-heroicons-sparkles" 
            color="indigo" 
            size="xl"
            @click="openAnalyzer"
            class="rounded-2xl px-6 py-3 font-bold hover:scale-105 transition-transform flex-1 md:flex-none justify-center"
          >
            Analyzer AI
          </UButton>
        </div>
      </header>

      <!-- Navigation Tabs -->
      <div class="flex items-center justify-center mb-12 animate-in fade-in slide-in-from-bottom-2 duration-700 delay-300">
        <div class="inline-flex p-1 bg-slate-900/60 backdrop-blur-xl border border-slate-800/50 rounded-2xl shadow-2xl">
          <button 
            @click="activeTab = 'infra'"
            :class="activeTab === 'infra' ? 'bg-indigo-500 text-white shadow-lg shadow-indigo-500/20' : 'text-slate-400 hover:text-slate-200'"
            class="px-8 py-2.5 rounded-xl text-sm font-bold transition-all duration-300 flex items-center gap-2"
          >
            <UIcon name="i-heroicons-rectangle-group" class="w-4 h-4" />
            Infra Geral
          </button>
          <button 
            @click="activeTab = 'veeam'"
            :class="activeTab === 'veeam' ? 'bg-emerald-500 text-white shadow-lg shadow-emerald-500/20' : 'text-slate-400 hover:text-slate-200'"
            class="px-8 py-2.5 rounded-xl text-sm font-bold transition-all duration-300 flex items-center gap-2"
          >
            <UIcon name="i-heroicons-shield-check" class="w-4 h-4" />
            Veeam Pro
            <UBadge v-if="Array.isArray(veeamData?.details) && veeamData.details.some(v => v.metrics?.failed_sessions_24h > 0)" color="red" variant="solid" size="xs" class="animate-pulse">!</UBadge>
          </button>
        </div>
      </div>

      <div v-if="activeTab === 'infra'">
        <!-- Stats Grid -->
        <div v-if="stats" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-10 animate-in fade-in zoom-in-95 duration-1000">
        <div v-for="(stat, key) in dashboardStats" :key="key" class="bg-slate-900/40 border border-slate-800/50 backdrop-blur-md p-5 rounded-3xl">
          <span class="text-[10px] uppercase tracking-widest text-slate-500 font-bold">{{ stat.label }}</span>
          <div class="text-2xl font-bold text-white mt-1 leading-tight">{{ stat.value }}</div>
          <div class="flex items-center gap-1 mt-2">
             <UIcon :name="stat.trendIcon" :class="stat.trendClass" class="w-4 h-4" />
             <span :class="stat.trendClass" class="text-xs font-medium">{{ stat.trendText }}</span>
          </div>
        </div>
      </div>

      <!-- Main Columns -->
      <div class="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-4 gap-6 mb-12">
        
        <!-- Network Layer -->
        <div class="group h-full">
          <div class="bg-slate-900/40 border border-slate-800/50 backdrop-blur-md rounded-[2rem] p-6 sm:p-8 h-full flex flex-col hover:border-blue-500/30 transition-all duration-500 shadow-xl">
            <div class="flex items-center justify-between mb-8">
              <div class="p-4 bg-blue-500/10 rounded-2xl text-blue-400 group-hover:bg-blue-500 group-hover:text-white transition-colors duration-500 shadow-inner">
                <UIcon name="i-heroicons-globe-alt" class="w-8 h-8" />
              </div>
              <UBadge color="blue" variant="soft" class="rounded-full">Real-time SNMP</UBadge>
            </div>
            <h2 class="text-2xl font-bold text-white mb-3">Redes & Conectividade</h2>
            <p class="text-slate-400 text-sm leading-relaxed mb-8">Gestão de ativos Juniper e roteamento via Model Context Protocol (MCP).</p>
            
            <div class="mt-auto space-y-3">
              <div class="flex justify-between items-center p-4 bg-slate-950/50 rounded-2xl border border-slate-800/50 group/item hover:bg-slate-900/80 transition-color">
                <div class="flex items-center gap-3">
                  <div class="w-2 h-2 rounded-full bg-emerald-500 shadow-[0_0_8px_#10b981]"></div>
                  <span class="text-sm font-semibold text-slate-200">RT-ADC-BQ-01</span>
                </div>
                <span class="text-xs font-mono text-slate-500">192.168.0.155</span>
              </div>
              <div class="flex justify-between items-center p-4 bg-slate-950/50 rounded-2xl border border-slate-800/50 group/item hover:bg-slate-900/80 transition-color">
                <div class="flex items-center gap-3">
                  <div class="w-2 h-2 rounded-full bg-emerald-500 shadow-[0_0_8px_#10b981]"></div>
                  <span class="text-sm font-semibold text-slate-200">RT-ADC-BQ-02</span>
                </div>
                <span class="text-xs font-mono text-slate-500">192.168.0.156</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Physical Layer -->
        <div class="group h-full">
          <div class="bg-slate-900/40 border border-slate-800/50 backdrop-blur-md rounded-[2rem] p-6 sm:p-8 h-full flex flex-col hover:border-orange-500/30 transition-all duration-500 shadow-xl">
            <div class="flex items-center justify-between mb-8">
              <div class="p-4 bg-orange-500/10 rounded-2xl text-orange-400 group-hover:bg-orange-500 group-hover:text-white transition-colors duration-500 shadow-inner">
                <UIcon name="i-heroicons-server" class="w-8 h-8" />
              </div>
              <UBadge color="orange" variant="soft" class="rounded-full">Zabbix Core</UBadge>
            </div>
            <h2 class="text-2xl font-bold text-white mb-3">Hardware & Baremetal</h2>
            <p class="text-slate-400 text-sm leading-relaxed mb-8">Inventário físico completo sincronizado via API Zabbix com monitoramento de chassis.</p>
            
            <div class="mt-auto">
              <div class="p-6 bg-gradient-to-br from-orange-500/10 to-transparent rounded-[1.5rem] border border-orange-500/20">
                <div class="flex justify-between items-end">
                  <div>
                    <div class="text-3xl font-bold text-white tabular-nums">{{ stats?.physical?.hosts || 0 }}</div>
                    <div class="text-[10px] text-orange-400 font-black uppercase tracking-widest mt-1">Ativos Monitorados</div>
                  </div>
                  <div class="text-right">
                    <div class="text-xl font-bold text-red-500 tabular-nums">{{ stats?.physical?.problems || 0 }}</div>
                    <div class="text-[10px] text-slate-500 uppercase font-black tracking-widest leading-none">Problemas Ativos</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Virtual Layer -->
        <div class="group h-full">
          <div class="bg-slate-900/40 border border-slate-800/50 backdrop-blur-md rounded-[2rem] p-6 sm:p-8 h-full flex flex-col hover:border-purple-500/30 transition-all duration-500 shadow-xl">
            <div class="flex items-center justify-between mb-8">
              <div class="p-4 bg-purple-500/10 rounded-2xl text-purple-400 group-hover:bg-purple-500 group-hover:text-white transition-colors duration-500 shadow-inner">
                <UIcon name="i-heroicons-cpu-chip" class="w-8 h-8" />
              </div>
              <UBadge color="purple" variant="soft" class="rounded-full">VMware & NSX</UBadge>
            </div>
            <h2 class="text-2xl font-bold text-white mb-3">Nuvem Virtualizada</h2>
            <p class="text-slate-400 text-sm leading-relaxed mb-8">Clusters vSphere e Micro-segmentação NSX-T integrados nativamente.</p>
            
            <div class="mt-auto space-y-3">
              <div class="flex justify-between items-center p-4 bg-slate-950/50 rounded-2xl border border-slate-800/50">
                <div class="flex items-center gap-3">
                  <div class="w-2 h-2 rounded-full bg-emerald-500 shadow-[0_0_8px_#10b981]"></div>
                  <span class="text-sm font-semibold text-slate-200">vCenter Cluster</span>
                </div>
                <UIcon name="i-heroicons-check-circle" class="text-emerald-500 w-5 h-5" />
              </div>
              <div class="flex justify-between items-center p-4 bg-slate-950/50 rounded-2xl border border-slate-800/50">
                <div class="flex items-center gap-3">
                  <div class="w-2 h-2 rounded-full bg-emerald-500 shadow-[0_0_8px_#10b981]"></div>
                  <span class="text-sm font-semibold text-slate-200">NSX-T Manager</span>
                </div>
                <UIcon name="i-heroicons-shield-check" class="text-emerald-500 w-5 h-5" />
              </div>
            </div>
          </div>
        </div>

        <!-- Backup Layer (Veeam) -->
        <div class="group h-full lg:col-span-3 xl:col-span-1">
          <div class="bg-slate-900/40 border border-slate-800/50 backdrop-blur-md rounded-[2rem] p-6 sm:p-8 h-full flex flex-col hover:border-emerald-500/30 transition-all duration-500 shadow-xl">
            <div class="flex items-center justify-between mb-8">
              <div class="p-4 bg-emerald-500/10 rounded-2xl text-emerald-400 group-hover:bg-emerald-500 group-hover:text-white transition-colors duration-500 shadow-inner">
                <UIcon name="i-heroicons-shield-check" class="w-8 h-8" />
              </div>
              <UBadge color="emerald" variant="soft" class="rounded-full">Veeam Continuous Protection</UBadge>
            </div>
            <h2 class="text-2xl font-bold text-white mb-3">Backup & Resiliência</h2>
            <p class="text-slate-400 text-sm leading-relaxed mb-6">Visão consolidada multi-VBR (JLLE & BRQ). Monitoramento de SLAs e Repositórios.</p>
            
            <div class="grid grid-cols-2 gap-3 mb-6">
               <div class="p-4 bg-slate-950/50 rounded-2xl border border-slate-800/50">
                  <span class="text-[9px] font-black text-slate-500 uppercase tracking-widest block mb-1">JLLE-VBR (10.21.40.5)</span>
                  <div class="flex items-center gap-2">
                    <span class="w-2 h-2 rounded-full" :class="stats?.backup?.status === 'online' ? 'bg-emerald-500' : 'bg-red-500'"></span>
                    <span class="text-xs font-bold text-white">{{ stats?.backup?.status === 'online' ? 'Protegido' : 'Verificar' }}</span>
                  </div>
               </div>
               <div class="p-4 bg-slate-950/50 rounded-2xl border border-slate-800/50">
                  <span class="text-[9px] font-black text-slate-500 uppercase tracking-widest block mb-1">BRQ-VBR (10.1.247.5)</span>
                  <div class="flex items-center gap-2">
                    <span class="w-2 h-2 rounded-full" :class="stats?.backup?.status === 'online' ? 'bg-emerald-500' : 'bg-red-500'"></span>
                    <span class="text-xs font-bold text-white">{{ stats?.backup?.status === 'online' ? 'Protegido' : 'Verificar' }}</span>
                  </div>
               </div>
            </div>

            <div class="mt-auto">
               <div class="p-4 bg-emerald-500/5 border border-emerald-500/10 rounded-2xl">
                 <div class="flex items-center gap-2 text-emerald-400 mb-2">
                    <UIcon name="i-heroicons-information-circle" class="w-4 h-4" />
                    <span class="text-[10px] font-bold uppercase tracking-wider">Health Summary</span>
                 </div>
                 <p class="text-[11px] text-slate-400 italic">"{{ stats?.backup?.summary || 'Coletando dados dos VBRs...' }}"</p>
               </div>
            </div>
          </div>
        </div>

      </div> <!-- Fim da Grid de Colunas -->
    </div> <!-- Fim do activeTab === 'infra' -->

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

    <!-- Modal Analyzer AI (Advanced Filter + Search) -->
    <UModal v-model="isAnalyzerOpen" :ui="{ width: 'sm:max-w-3xl' }">
      <div class="bg-[#0f111a] border border-slate-800 sm:rounded-3xl overflow-hidden shadow-2xl flex flex-col max-h-[90vh]">
        <!-- Modal Header -->
        <div class="p-6 sm:p-8 border-b border-slate-800 sticky top-0 bg-[#0f111a] z-30">
          <div class="flex items-center justify-between mb-6">
            <div class="flex items-center gap-3">
              <div class="p-3 bg-indigo-500 rounded-xl shadow-lg shadow-indigo-500/20">
                <UIcon name="i-heroicons-sparkles" class="w-6 h-6 text-white" />
              </div>
              <div>
                <h3 class="text-xl font-bold text-white">Analyzer AI Core</h3>
                <p class="text-slate-500 text-xs font-bold uppercase tracking-widest">Busca avançada Zabbix (IP/Nome)</p>
              </div>
            </div>
            <UButton color="slate" variant="ghost" icon="i-heroicons-x-mark-20-solid" class="rounded-full" @click="closeAnalyzer" />
          </div>

          <!-- Search Interface -->
          <div class="flex gap-2">
            <div class="relative flex-1 group">
              <UInput 
                v-model="searchQuery" 
                placeholder="Busque por IP ou Nome do Host..." 
                icon="i-heroicons-magnifying-glass"
                size="xl"
                class="rounded-xl overflow-hidden"
                :ui="{ rounded: 'rounded-xl', base: 'bg-slate-950 border-slate-700/50 focus:border-indigo-500' }"
                @keyup.enter="handleSearch"
              />
            </div>
            <UButton 
              color="indigo" 
              size="xl" 
              icon="i-heroicons-funnel"
              :loading="isSearching" 
              @click="handleSearch"
              class="rounded-xl px-4 sm:px-8 font-extrabold uppercase text-xs"
            >
              Filtrar
            </UButton>
          </div>
        </div>

        <!-- Modal Content Area -->
        <div class="flex-1 overflow-y-auto p-6 sm:p-8 custom-scrollbar">
          
          <!-- State 1: Results Table -->
          <div v-if="searchResults.length > 0 && !selectedHost && !isLoading" class="animate-in fade-in slide-in-from-bottom-2">
             <div class="flex items-center justify-between mb-4 px-1">
                <span class="text-xs font-bold text-slate-500 uppercase tracking-widest">{{ searchResults.length }} Resultados Encontrados</span>
             </div>
             <div class="space-y-2">
                <div 
                  v-for="host in searchResults" 
                  :key="host.hostid"
                  @click="selectHost(host)"
                  class="flex items-center justify-between p-4 bg-slate-900/50 hover:bg-slate-800 border border-slate-800/80 rounded-2xl cursor-pointer transition-all group"
                >
                  <div class="flex flex-col">
                    <span class="text-white font-bold">{{ host.name }}</span>
                    <span class="text-xs font-mono text-slate-500">{{ host.ip }}</span>
                  </div>
                  <div class="flex items-center gap-3">
                    <UBadge :color="host.status == '0' ? 'emerald' : 'red'" variant="subtle" size="xs">
                      {{ host.status == '0' ? 'Enabled' : 'Disabled' }}
                    </UBadge>
                    <UIcon name="i-heroicons-chevron-right" class="text-slate-600 group-hover:text-indigo-400 group-hover:translate-x-1 transition-all" />
                  </div>
                </div>
             </div>
          </div>

          <!-- State 2: Selected Host & AI Result -->
          <div v-if="selectedHost" class="animate-in fade-in zoom-in-95">
             <!-- Selected Host Header -->
             <div class="bg-indigo-500/10 border border-indigo-500/30 p-5 rounded-2xl mb-8 flex justify-between items-center">
                <div>
                   <span class="text-[10px] font-black text-indigo-400 uppercase tracking-widest block mb-1">Host Selecionado</span>
                   <h4 class="text-lg font-bold text-white">{{ selectedHost.name }} <span class="text-slate-500 font-mono text-sm ml-2">({{ selectedHost.ip }})</span></h4>
                </div>
                <UButton color="slate" variant="ghost" size="xs" label="Mudar Host" @click="selectedHost = null; aiResult = null" />
             </div>

             <!-- AI Report UI -->
             <div v-if="isLoading" class="flex flex-col items-center justify-center py-12 gap-4">
                <div class="relative">
                  <div class="absolute inset-0 bg-indigo-500/20 blur-xl animate-pulse rounded-full"></div>
                  <UIcon name="i-heroicons-cpu-chip" class="relative w-16 h-16 text-indigo-500 animate-bounce" />
                </div>
                <div class="text-center space-y-2">
                   <p class="text-white font-bold text-lg">Iniciando Inferência LLaMA3</p>
                   <p class="text-slate-500 text-sm max-w-[280px]">Extraindo métricas reais do Zabbix e consolidando relatório SRE...</p>
                </div>
             </div>

             <div v-else-if="aiResult" class="space-y-6">
                <div class="flex items-center justify-between mb-2">
                   <span class="text-[10px] font-black text-indigo-500 uppercase tracking-[0.2em]">Relatório SRE Consolidado</span>
                   <UBadge color="emerald" variant="soft" size="xs">{{ aiResult.raw_data_points }} Data Points</UBadge>
                </div>

                <!-- Structured AI Cards -->
                <div class="grid grid-cols-1 gap-4">
                   <!-- Health Card -->
                   <div class="bg-slate-900/50 border border-slate-800 rounded-[1.5rem] p-6 hover:border-emerald-500/30 transition-all duration-500 group/sre">
                      <div class="flex items-center gap-3 mb-4 text-emerald-400">
                         <UIcon name="i-heroicons-heart" class="w-5 h-5" />
                         <span class="text-xs font-black uppercase tracking-widest">System Health</span>
                      </div>
                      <p class="text-slate-300 text-sm leading-relaxed font-medium">
                        {{ parseAiSection(aiResult.ai_analysis, 'Health') }}
                      </p>
                   </div>

                   <!-- Security Card -->
                   <div class="bg-slate-900/50 border border-slate-800 rounded-[1.5rem] p-6 hover:border-orange-500/30 transition-all duration-500 group/sre">
                      <div class="flex items-center gap-3 mb-4 text-orange-400">
                         <UIcon name="i-heroicons-shield-check" class="w-5 h-5" />
                         <span class="text-xs font-black uppercase tracking-widest">Security & Alerts</span>
                      </div>
                      <p class="text-slate-300 text-sm leading-relaxed font-medium">
                        {{ parseAiSection(aiResult.ai_analysis, 'Security') }}
                      </p>
                   </div>

                   <!-- Capacity Card -->
                   <div class="bg-slate-900/50 border border-slate-800 rounded-[1.5rem] p-6 hover:border-indigo-500/30 transition-all duration-500 group/sre">
                      <div class="flex items-center gap-3 mb-4 text-indigo-400">
                         <UIcon name="i-heroicons-chart-bar" class="w-5 h-5" />
                         <span class="text-xs font-black uppercase tracking-widest">Resource Capacity</span>
                      </div>
                      <p class="text-slate-300 text-sm leading-relaxed font-medium">
                        {{ parseAiSection(aiResult.ai_analysis, 'Capacity') }}
                      </p>
                   </div>
                </div>
                <UButton block color="slate" variant="ghost" icon="i-heroicons-arrow-path" class="rounded-xl font-bold py-3 border border-slate-800 hover:bg-slate-800" @click="handleAnalysis(selectedHost.hostid)">Recalcular Análise Inteligente</UButton>
             </div>
          </div>

          <!-- Empty States / Errors -->
          <div v-if="searchResults.length === 0 && searchQuery.length > 2 && !isSearching && !selectedHost" class="flex flex-col items-center justify-center py-12 text-center text-slate-500">
             <UIcon name="i-heroicons-magnifying-glass-circle" class="w-12 h-12 mb-3 opacity-20" />
             <p class="font-bold">Nenhum host encontrado</p>
             <p class="text-xs">Tente outro nome ou IP parcial</p>
          </div>
          
          <div v-if="errorMsg" class="mt-4 p-4 bg-red-500/5 border border-red-500/20 rounded-2xl text-red-500 text-sm font-bold text-center">
            {{ errorMsg }}
          </div>
        </div>
      </div>
    </UModal>
    </div> <!-- Fim do Layout Container -->
  </div> <!-- Fim do Root Div -->
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'

const isAnalyzerOpen = ref(false)
const searchQuery = ref('')
const isSearching = ref(false)
const isLoading = ref(false)
const searchResults = ref([])
const selectedHost = ref(null)
const aiResult = ref(null)
const errorMsg = ref('')
const stats = ref(null)
const activeTab = ref('infra')
const veeamData = ref([])
const isVeeamLoading = ref(false)

function parseAiSection(text, section) {
  if (!text) return 'Carregando...';
  const parts = text.split(`**${section}**:`);
  if (parts.length > 1) {
    return parts[1].split('**')[0].trim();
  }
  return text.includes(section) ? text : 'Informação não disponível no relatório.';
}

const dashboardStats = computed(() => {
  if (!stats.value) return []
  return [
    { label: 'Redes (MCP)', value: stats.value.network.hosts, trendText: '2 ativos SNMP', trendIcon: 'i-heroicons-link', trendClass: 'text-blue-500' },
    { label: 'Física (Zabbix)', value: stats.value.physical.hosts, trendText: 'Nós Baremetal', trendIcon: 'i-heroicons-server', trendClass: 'text-orange-500' },
    { label: 'VM Instances', value: stats.value.virtual.hosts, trendText: 'vSphere Cluster', trendIcon: 'i-heroicons-cloud', trendClass: 'text-purple-500' },
    { label: 'Backup Health', value: stats.value.backup.status === 'online' ? '100%' : 'Alarm', trendText: 'Dual VBR V12', trendIcon: 'i-heroicons-shield-check', trendClass: stats.value.backup.status === 'online' ? 'text-emerald-500' : 'text-red-500' },
    { label: 'Active Alerts', value: stats.value.physical.problems, trendText: 'Attention required', trendIcon: 'i-heroicons-exclamation-triangle', trendClass: 'text-red-500' }
  ]
})

function openAnalyzer() {
  isAnalyzerOpen.value = true
}

function closeAnalyzer() {
  isAnalyzerOpen.value = false
  // Reset states
  searchResults.value = []
  selectedHost.value = null
  aiResult.value = null
  errorMsg.value = ''
  searchQuery.value = ''
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
  setInterval(async () => {
    await fetchDashboardData();
    await fetchVeeamData();
  }, 60000);
})

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
