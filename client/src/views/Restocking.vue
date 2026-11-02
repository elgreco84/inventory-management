<template>
  <div class="restocking">
    <div class="page-header">
      <h2>{{ t('restocking.title') }}</h2>
      <p>{{ t('restocking.description') }}</p>
    </div>

    <div v-if="loading" class="loading">{{ t('common.loading') }}</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else>
      <div class="card">
        <div class="card-header">
          <h3 class="card-title">{{ t('restocking.budget') }}: {{ money(budget) }}</h3>
        </div>
        <input
          v-model.number="budget"
          class="budget-slider"
          type="range"
          min="0"
          :max="sliderMax"
          step="1"
          :aria-label="t('restocking.budget')"
          @input="scheduleFetch"
        />
      </div>

      <div class="stats-grid">
        <div class="stat-card info">
          <div class="stat-label">{{ t('restocking.budget') }}</div>
          <div class="stat-value">{{ money(budget) }}</div>
        </div>
        <div class="stat-card success">
          <div class="stat-label">{{ t('restocking.recommendedTotal') }}</div>
          <div class="stat-value">{{ money(totalCost) }}</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">{{ t('restocking.remaining') }}</div>
          <div class="stat-value">{{ money(Math.max(budget - totalCost, 0)) }}</div>
        </div>
      </div>

      <div v-if="confirmation" class="confirmation">{{ confirmation }}</div>
      <div v-if="submitError" class="error">{{ submitError }}</div>

      <div class="card">
        <div class="card-header">
          <h3 class="card-title">{{ t('restocking.recommendedItems') }} ({{ items.length }})</h3>
          <button class="place-order" :disabled="!items.length || submitting || stale" @click="placeOrder">
            {{ submitting ? t('restocking.submitting') : t('restocking.placeOrder') }}
          </button>
        </div>
        <div v-if="!items.length" class="loading">{{ t('restocking.empty') }}</div>
        <div v-else class="table-container">
          <table>
            <thead>
              <tr>
                <th>{{ t('restocking.table.sku') }}</th>
                <th>{{ t('restocking.table.name') }}</th>
                <th>{{ t('restocking.table.trend') }}</th>
                <th>{{ t('restocking.table.quantity') }}</th>
                <th>{{ t('restocking.table.unitCost') }}</th>
                <th>{{ t('restocking.table.lineTotal') }}</th>
                <th>{{ t('restocking.table.leadTime') }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in items" :key="item.item_sku">
                <td><strong>{{ item.item_sku }}</strong></td>
                <td>{{ translateProductName(item.item_name) }}</td>
                <td>
                  <span :class="['badge', item.trend]">{{ t(`trends.${item.trend}`) }}</span>
                </td>
                <td>{{ item.quantity }}</td>
                <td>{{ money(item.unit_cost, 2) }}</td>
                <td><strong>{{ money(item.line_total, 2) }}</strong></td>
                <td>{{ item.lead_time_days }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { api } from '../api'
import { useI18n } from '../composables/useI18n'
import { formatCurrencyWithDecimals } from '../utils/currency'

export default {
  name: 'Restocking',
  setup() {
    const { t, currentCurrency, currentLocale, translateProductName } = useI18n()

    const loading = ref(true)
    const error = ref(null)
    const sliderMax = ref(0)
    const budget = ref(0)
    const items = ref([])
    const totalCost = ref(0)
    const submitting = ref(false)
    const submitError = ref(null)
    const confirmation = ref(null)
    const stale = ref(false) // items lag the slider until the debounced fetch lands

    let timer = null
    let requestId = 0 // drops stale responses

    const money = (amount, decimals = 0) =>
      formatCurrencyWithDecimals(amount, currentCurrency.value, decimals)

    const formatDate = (dateString) => {
      const d = new Date(dateString)
      if (isNaN(d.getTime())) return '-'
      return d.toLocaleDateString(currentLocale.value === 'ja' ? 'ja-JP' : 'en-US', {
        year: 'numeric', month: 'short', day: 'numeric'
      })
    }

    const fetchRecommendations = async () => {
      const id = ++requestId
      try {
        const res = await api.getRestockRecommendations(budget.value)
        if (id !== requestId) return
        items.value = res.items
        totalCost.value = res.total_cost
        error.value = null
        stale.value = false
      } catch (err) {
        if (id !== requestId) return
        error.value = t('restocking.loadFailed') + ': ' + err.message
      }
    }

    const scheduleFetch = () => {
      clearTimeout(timer)
      stale.value = true
      confirmation.value = null
      timer = setTimeout(fetchRecommendations, 250)
    }

    const placeOrder = async () => {
      submitting.value = true
      submitError.value = null
      confirmation.value = null
      try {
        const order = await api.createRestockOrder(
          items.value.map(i => ({ item_sku: i.item_sku, quantity: i.quantity }))
        )
        confirmation.value = t('restocking.confirmed', {
          id: order.id,
          total: money(order.total_cost, 2),
          date: formatDate(order.expected_delivery)
        })
      } catch (err) {
        const detail = err.response?.data?.detail
        submitError.value = t('restocking.failed') + ': ' +
          (typeof detail === 'string' ? detail : err.message)
      } finally {
        submitting.value = false
      }
    }

    onMounted(async () => {
      try {
        const res = await api.getRestockRecommendations()
        items.value = res.items
        totalCost.value = res.total_cost
        sliderMax.value = Math.max(Math.ceil(res.max_cost / 100) * 100, 100)
        budget.value = res.max_cost
      } catch (err) {
        error.value = t('restocking.loadFailed') + ': ' + err.message
      } finally {
        loading.value = false
      }
    })

    onBeforeUnmount(() => clearTimeout(timer))

    return {
      t, loading, error, sliderMax, budget, items, totalCost, submitting,
      submitError, confirmation, stale, money, scheduleFetch, placeOrder, translateProductName
    }
  }
}
</script>

<style scoped>
.budget-slider {
  width: 100%;
  accent-color: var(--primary);
}

.place-order {
  background: var(--primary);
  color: var(--primary-foreground);
  border: none;
  border-radius: var(--radius);
  padding: 0.5rem 1.25rem;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
}

.place-order:hover:not(:disabled) {
  background: var(--primary);
}

.place-order:disabled {
  background: var(--input);
  cursor: not-allowed;
}

.confirmation {
  background: var(--success-soft);
  border: 1px solid var(--success-soft);
  color: var(--success);
  padding: 1rem;
  border-radius: var(--radius);
  margin-bottom: 1.25rem;
  font-size: 0.938rem;
}
</style>
