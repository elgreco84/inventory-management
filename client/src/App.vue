<template>
  <div class="app" :class="{ collapsed }">
    <aside class="sidebar">
      <div class="brand">
        <div class="brand-mark" aria-hidden="true">CC</div>
        <div class="brand-text">
          <div class="brand-name">{{ t('nav.companyName') }}</div>
          <div class="brand-sub">{{ t('nav.subtitle') }}</div>
        </div>
      </div>
      <nav class="nav" :aria-label="t('nav.mainNav')">
        <div class="nav-group">
          <div class="nav-group-label">{{ t('nav.groupOverview') }}</div>
          <router-link to="/" class="nav-link" :title="collapsed ? t('nav.overview') : null" :aria-label="t('nav.overview')">
            <svg class="nav-icon" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="3" width="7" height="9"/><rect x="14" y="3" width="7" height="5"/><rect x="14" y="12" width="7" height="9"/><rect x="3" y="16" width="7" height="5"/></svg>
            <span class="nav-label">{{ t('nav.overview') }}</span>
          </router-link>
        </div>
        <div class="nav-group">
          <div class="nav-group-label">{{ t('nav.groupOperations') }}</div>
          <router-link to="/inventory" class="nav-link" :title="collapsed ? t('nav.inventory') : null" :aria-label="t('nav.inventory')">
            <svg class="nav-icon" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 8l-9-5-9 5v8l9 5 9-5z"/><path d="M3 8l9 5 9-5M12 13v8"/></svg>
            <span class="nav-label">{{ t('nav.inventory') }}</span>
          </router-link>
          <router-link to="/orders" class="nav-link" :title="collapsed ? t('nav.orders') : null" :aria-label="t('nav.orders')">
            <svg class="nav-icon" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 2L3 6v14a2 2 0 002 2h14a2 2 0 002-2V6l-3-4z"/><path d="M3 6h18"/><path d="M16 10a4 4 0 01-8 0"/></svg>
            <span class="nav-label">{{ t('nav.orders') }}</span>
          </router-link>
          <router-link to="/restocking" class="nav-link" :title="collapsed ? t('nav.restocking') : null" :aria-label="t('nav.restocking')">
            <svg class="nav-icon" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12a9 9 0 11-3-6.7L21 8"/><path d="M21 3v5h-5"/></svg>
            <span class="nav-label">{{ t('nav.restocking') }}</span>
          </router-link>
          <router-link to="/demand" class="nav-link" :title="collapsed ? t('nav.demandForecast') : null" :aria-label="t('nav.demandForecast')">
            <svg class="nav-icon" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 3v18h18"/><path d="M7 15l4-4 3 3 5-6"/></svg>
            <span class="nav-label">{{ t('nav.demandForecast') }}</span>
          </router-link>
        </div>
        <div class="nav-group">
          <div class="nav-group-label">{{ t('nav.groupFinance') }}</div>
          <router-link to="/spending" class="nav-link" :title="collapsed ? t('nav.finance') : null" :aria-label="t('nav.finance')">
            <svg class="nav-icon" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="12" y1="2" x2="12" y2="22"/><path d="M17 6H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"/></svg>
            <span class="nav-label">{{ t('nav.finance') }}</span>
          </router-link>
          <router-link to="/reports" class="nav-link" :title="collapsed ? t('nav.reports') : null" :aria-label="t('nav.reports')">
            <svg class="nav-icon" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h8"/></svg>
            <span class="nav-label">{{ t('nav.reports') }}</span>
          </router-link>
        </div>
      </nav>
      <div class="sidebar-footer">
        <button
          class="collapse-toggle"
          type="button"
          :aria-label="collapsed ? t('nav.expand') : t('nav.collapse')"
          :title="collapsed ? t('nav.expand') : t('nav.collapse')"
          :aria-expanded="String(!collapsed)"
          @click="toggleCollapsed"
        >
          <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <rect x="3" y="3" width="18" height="18" rx="2"/><path d="M9 3v18"/>
          </svg>
          <span class="nav-label">{{ collapsed ? t('nav.expand') : t('nav.collapse') }}</span>
        </button>
      </div>
    </aside>

    <div class="main">
      <header class="topbar">
        <FilterBar />
        <LanguageSwitcher />
        <ProfileMenu
          @show-profile-details="showProfileDetails = true"
          @show-tasks="showTasks = true"
        />
      </header>
      <main class="content">
        <router-view />
      </main>
    </div>

    <ProfileDetailsModal
      :is-open="showProfileDetails"
      @close="showProfileDetails = false"
    />

    <TasksModal
      :is-open="showTasks"
      :tasks="tasks"
      @close="showTasks = false"
      @add-task="addTask"
      @delete-task="deleteTask"
      @toggle-task="toggleTask"
    />
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { api } from './api'
import { useAuth } from './composables/useAuth'
import { useI18n } from './composables/useI18n'
import FilterBar from './components/FilterBar.vue'
import ProfileMenu from './components/ProfileMenu.vue'
import ProfileDetailsModal from './components/ProfileDetailsModal.vue'
import TasksModal from './components/TasksModal.vue'
import LanguageSwitcher from './components/LanguageSwitcher.vue'

export default {
  name: 'App',
  components: {
    FilterBar,
    ProfileMenu,
    ProfileDetailsModal,
    TasksModal,
    LanguageSwitcher
  },
  setup() {
    const { currentUser } = useAuth()
    const { t } = useI18n()
    const showProfileDetails = ref(false)
    const showTasks = ref(false)
    let saved = false
    try { saved = localStorage.getItem('sidebar-collapsed') === '1' } catch (e) { /* storage unavailable */ }
    const collapsed = ref(saved)
    const toggleCollapsed = () => {
      collapsed.value = !collapsed.value
      try { localStorage.setItem('sidebar-collapsed', collapsed.value ? '1' : '0') } catch (e) { /* ignore */ }
    }
    const apiTasks = ref([])

    // Merge mock tasks from currentUser with API tasks
    const tasks = computed(() => {
      return [...currentUser.value.tasks, ...apiTasks.value]
    })

    const loadTasks = async () => {
      try {
        apiTasks.value = await api.getTasks()
      } catch (err) {
        console.error('Failed to load tasks:', err)
      }
    }

    const addTask = async (taskData) => {
      try {
        const newTask = await api.createTask(taskData)
        // Add new task to the beginning of the array
        apiTasks.value.unshift(newTask)
      } catch (err) {
        console.error('Failed to add task:', err)
      }
    }

    const deleteTask = async (taskId) => {
      try {
        // Check if it's a mock task (from currentUser)
        const isMockTask = currentUser.value.tasks.some(t => t.id === taskId)

        if (isMockTask) {
          // Remove from mock tasks
          const index = currentUser.value.tasks.findIndex(t => t.id === taskId)
          if (index !== -1) {
            currentUser.value.tasks.splice(index, 1)
          }
        } else {
          // Remove from API tasks
          await api.deleteTask(taskId)
          apiTasks.value = apiTasks.value.filter(t => t.id !== taskId)
        }
      } catch (err) {
        console.error('Failed to delete task:', err)
      }
    }

    const toggleTask = async (taskId) => {
      try {
        // Check if it's a mock task (from currentUser)
        const mockTask = currentUser.value.tasks.find(t => t.id === taskId)

        if (mockTask) {
          // Toggle mock task status
          mockTask.status = mockTask.status === 'pending' ? 'completed' : 'pending'
        } else {
          // Toggle API task
          const updatedTask = await api.toggleTask(taskId)
          const index = apiTasks.value.findIndex(t => t.id === taskId)
          if (index !== -1) {
            apiTasks.value[index] = updatedTask
          }
        }
      } catch (err) {
        console.error('Failed to toggle task:', err)
      }
    }

    onMounted(loadTasks)

    return {
      t,
      showProfileDetails,
      showTasks,
      collapsed,
      toggleCollapsed,
      tasks,
      addTask,
      deleteTask,
      toggleTask
    }
  }
}
</script>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }

.app { display: grid; grid-template-columns: var(--sidebar-width) 1fr; min-height: 100vh; transition: grid-template-columns .15s ease; }
.app.collapsed { --sidebar-width: 56px; }

.sidebar { position: sticky; top: 0; height: 100vh; overflow-y: auto; overflow-x: hidden;
  display: flex; flex-direction: column; background: var(--sidebar); border-right: 1px solid var(--border); }
.brand { display: flex; align-items: center; gap: var(--space-3); height: 56px; min-height: 56px; padding: 0 var(--space-3);
  border-bottom: 1px solid var(--border); }
.brand-mark { flex: none; width: 32px; height: 32px; border-radius: var(--radius); background: var(--primary);
  color: var(--primary-foreground); display: grid; place-items: center; font-size: var(--text-xs); font-weight: 600; }
.brand-text { min-width: 0; }
.brand-name { font-size: var(--text-sm); font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.brand-sub { font-size: var(--text-xs); color: var(--muted-foreground); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

.nav { flex: 1; padding: var(--space-3) var(--space-2); display: flex; flex-direction: column; gap: var(--space-4); }
.nav-group { display: flex; flex-direction: column; gap: 2px; }
.nav-group-label { padding: 0 var(--space-2) var(--space-1); font-size: var(--text-xs); font-weight: 500; color: var(--muted-foreground); white-space: nowrap; }
.nav-link, .collapse-toggle { display: flex; align-items: center; gap: var(--space-2); height: 32px; padding: 0 var(--space-2);
  border-radius: var(--radius); color: var(--muted-foreground); text-decoration: none; font: 400 var(--text-sm)/1 var(--font-sans);
  white-space: nowrap; background: transparent; border: 0; cursor: pointer; width: 100%; text-align: left; }
.nav-link:hover, .collapse-toggle:hover { background: var(--sidebar-accent); color: var(--foreground); }
.nav-link.router-link-exact-active { background: var(--sidebar-accent); color: var(--foreground); font-weight: 500; }
.nav-link:focus-visible, .collapse-toggle:focus-visible { outline-offset: -2px; }
.nav-icon { flex: none; }
.sidebar-footer { padding: var(--space-2); border-top: 1px solid var(--border); }

.app.collapsed .brand { justify-content: center; padding: 0; }
.app.collapsed .brand-text,
.app.collapsed .nav-label { display: none; }
.app.collapsed .nav { gap: var(--space-2); }
.app.collapsed .nav-group + .nav-group { border-top: 1px solid var(--border); padding-top: var(--space-2); }
.app.collapsed .nav-group-label { display: none; }
.app.collapsed .nav-link, .app.collapsed .collapse-toggle { justify-content: center; padding: 0; }

.main { min-width: 0; display: flex; flex-direction: column; }
.topbar { position: sticky; top: 0; z-index: 40; display: flex; align-items: center; gap: var(--space-3);
  min-height: 56px; flex-wrap: wrap; padding: var(--space-2) var(--space-6); background: var(--background); border-bottom: 1px solid var(--border); }
.topbar > :first-child { flex: 1 1 320px; }
.content { padding: var(--space-6); max-width: 1440px; width: 100%; }

@media (max-width: 768px) {
  .app { --sidebar-width: 56px; }
  .app .brand { justify-content: center; padding: 0; }
  .app .brand-text, .app .nav-label { display: none; }
  .app .nav-group-label { display: none; }
  .app .nav-link, .app .collapse-toggle { justify-content: center; padding: 0; }
  .topbar { position: static; padding: var(--space-2) var(--space-3); }
  .content { padding: var(--space-4) var(--space-3); }
  .card { overflow-x: auto; max-width: 100%; }
  .card .card-header { flex-wrap: wrap; gap: var(--space-2); }
  .content :where(input, select) { max-width: 100%; min-width: 0; }
  .content :where(div, section) { min-width: 0; }
}

/* Legacy shared classes used by views, now on tokens */
.page-header { display: block; margin-bottom: var(--space-6); }
.page-header h2 { font-size: var(--text-2xl); font-weight: 600; letter-spacing: -0.02em; margin-bottom: var(--space-1); }
.page-header p { color: var(--muted-foreground); font-size: var(--text-sm); }
.stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: var(--space-4); margin-bottom: var(--space-6); }
.stat-card { background: var(--card); padding: var(--space-5); border-radius: var(--radius-lg); border: 1px solid var(--border); box-shadow: var(--shadow-sm); }
.stat-label { margin-bottom: var(--space-2); }
.stat-value { font-size: var(--text-2xl); }
.card { padding: var(--space-6); margin-bottom: var(--space-5); }
.card .card-header { padding: 0 0 var(--space-4); margin-bottom: var(--space-4); border-bottom: 1px solid var(--border); }
.card-title { font-size: var(--text-base); }
.table-container { overflow-x: auto; }
table { width: 100%; border-collapse: collapse; }
thead { background: transparent; }
th { text-align: left; padding: 0 var(--space-3); height: 40px; font-weight: 500; color: var(--muted-foreground); font-size: var(--text-sm); white-space: nowrap; border-bottom: 1px solid var(--border); }
td { white-space: nowrap; padding: var(--space-3); border-top: 1px solid var(--border); color: var(--foreground); font-size: var(--text-sm); font-variant-numeric: tabular-nums; }
tbody tr:hover { background: var(--muted); }
.badge.success { background: var(--success-soft); color: var(--success); border-color: transparent; }
.badge.warning { background: var(--warning-soft); color: var(--warning); border-color: transparent; }
.badge.danger, .badge.high { background: var(--danger-soft); color: var(--danger); border-color: transparent; }
.badge.info, .badge.low { background: var(--info-soft); color: var(--info); border-color: transparent; }
.badge.increasing { background: var(--success-soft); color: var(--success); border-color: transparent; }
.badge.decreasing { background: var(--danger-soft); color: var(--danger); border-color: transparent; }
.badge.stable { background: var(--muted); color: var(--muted-foreground); }
.badge.medium { background: var(--warning-soft); color: var(--warning); border-color: transparent; }
.loading { text-align: center; padding: var(--space-10); color: var(--muted-foreground); }
.error { background: var(--danger-soft); border: 1px solid var(--danger); color: var(--danger); padding: var(--space-4); border-radius: var(--radius); margin: var(--space-4) 0; }
</style>
