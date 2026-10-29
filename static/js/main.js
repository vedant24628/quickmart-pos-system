/**
 * Quick Mart - Retail Store Management System
 * Vanilla JavaScript (No jQuery / No external JS frameworks except Chart.js)
 */

document.addEventListener('DOMContentLoaded', () => {
  initMobileSidebar();
  initModals();
  initFlashDismiss();
  initBillingSystem();
  initDashboardCharts();
});

/* ==========================================
   1. Mobile Sidebar Toggle
   ========================================== */
function initMobileSidebar() {
  const toggleBtn = document.getElementById('mobile-sidebar-toggle');
  const sidebar = document.querySelector('.sidebar');

  if (toggleBtn && sidebar) {
    toggleBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      sidebar.classList.toggle('mobile-open');
    });

    document.addEventListener('click', (e) => {
      if (sidebar.classList.contains('mobile-open') && !sidebar.contains(e.target) && e.target !== toggleBtn) {
        sidebar.classList.remove('mobile-open');
      }
    });
  }
}

/* ==========================================
   2. Modal Open / Close Controller
   ========================================== */
function initModals() {
  const triggers = document.querySelectorAll('[data-modal-target]');
  triggers.forEach(btn => {
    btn.addEventListener('click', () => {
      const targetId = btn.getAttribute('data-modal-target');
      const modal = document.querySelector(targetId);
      if (modal) {
        modal.classList.add('active');
      }
    });
  });

  const closeBtns = document.querySelectorAll('.modal-close, [data-modal-close]');
  closeBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const modal = btn.closest('.modal-overlay');
      if (modal) {
        modal.classList.remove('active');
      }
    });
  });

  // Close when clicking overlay backdrop
  const modals = document.querySelectorAll('.modal-overlay');
  modals.forEach(modal => {
    modal.addEventListener('click', (e) => {
      if (e.target === modal) {
        modal.classList.remove('active');
      }
    });
  });
}

/* ==========================================
   3. Flash Message Dismissal
   ========================================== */
function initFlashDismiss() {
  const closeBtns = document.querySelectorAll('.flash-close-btn');
  closeBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const alert = btn.closest('.flash-alert');
      if (alert) {
        alert.style.opacity = '0';
        setTimeout(() => alert.remove(), 250);
      }
    });
  });

  // Auto-dismiss after 6 seconds
  const alerts = document.querySelectorAll('.flash-alert');
  if (alerts.length > 0) {
    setTimeout(() => {
      alerts.forEach(alert => {
        alert.style.transition = 'opacity 0.4s ease';
        alert.style.opacity = '0';
        setTimeout(() => alert.remove(), 400);
      });
    }, 6000);
  }
}

/* ==========================================
   4. Billing POS System
   ========================================== */
function initBillingSystem() {
  const billingContainer = document.getElementById('billing-pos-container');
  if (!billingContainer) return;

  // Cart State
  let cart = [];

  const cartItemsList = document.getElementById('cart-items-list');
  const cartCountBadge = document.getElementById('cart-count-badge');
  const subtotalEl = document.getElementById('cart-subtotal');
  const sgstEl = document.getElementById('cart-sgst');
  const cgstEl = document.getElementById('cart-cgst');
  const totalEl = document.getElementById('cart-total');
  const emptyStateEl = document.getElementById('cart-empty-state');
  const btnGenerateBill = document.getElementById('btn-generate-bill');
  const checkoutMsg = document.getElementById('billing-msg');

  // Product cards click event
  const productCards = document.querySelectorAll('.product-picker-card');
  productCards.forEach(card => {
    card.addEventListener('click', () => {
      const id = parseInt(card.dataset.id);
      const name = card.dataset.name;
      const price = parseFloat(card.dataset.price);
      const stock = parseInt(card.dataset.stock);

      if (stock <= 0) return;

      addToCart(id, name, price, stock);
    });
  });

  function addToCart(id, name, price, stock) {
    const existing = cart.find(item => item.id === id);
    if (existing) {
      if (existing.quantity < stock) {
        existing.quantity += 1;
      } else {
        alert(`Cannot add more than available stock (${stock}) for "${name}".`);
      }
    } else {
      cart.push({
        id: id,
        name: name,
        price: price,
        stock: stock,
        quantity: 1
      });
    }
    renderCart();
  }

  function updateQuantity(id, delta) {
    const item = cart.find(i => i.id === id);
    if (!item) return;

    item.quantity += delta;
    if (item.quantity <= 0) {
      removeFromCart(id);
    } else if (item.quantity > item.stock) {
      alert(`Max stock available for "${item.name}" is ${item.stock}.`);
      item.quantity = item.stock;
      renderCart();
    } else {
      renderCart();
    }
  }

  function removeFromCart(id) {
    cart = cart.filter(i => i.id !== id);
    renderCart();
  }

  function renderCart() {
    if (!cartItemsList) return;

    cartItemsList.innerHTML = '';

    if (cart.length === 0) {
      if (emptyStateEl) emptyStateEl.style.display = 'block';
      if (cartCountBadge) cartCountBadge.textContent = '0 items';
      if (subtotalEl) subtotalEl.textContent = '₹0.00';
      if (sgstEl) sgstEl.textContent = '₹0.00';
      if (cgstEl) cgstEl.textContent = '₹0.00';
      if (totalEl) totalEl.textContent = '₹0.00';
      if (btnGenerateBill) btnGenerateBill.disabled = true;
      return;
    }

    if (emptyStateEl) emptyStateEl.style.display = 'none';

    let subtotal = 0;
    let totalItems = 0;

    cart.forEach(item => {
      const itemTotal = item.price * item.quantity;
      subtotal += itemTotal;
      totalItems += item.quantity;

      const row = document.createElement('div');
      row.className = 'cart-row';
      row.innerHTML = `
        <div class="cart-row-details">
          <div class="cart-item-name" title="${item.name}">${item.name}</div>
          <div class="cart-item-price">₹${item.price.toFixed(2)} &bull; Stock: ${item.stock}</div>
        </div>
        <div class="cart-qty-ctrl">
          <button type="button" class="qty-btn" data-action="dec" data-id="${item.id}">-</button>
          <span class="cart-qty-val">${item.quantity}</span>
          <button type="button" class="qty-btn" data-action="inc" data-id="${item.id}">+</button>
        </div>
        <div class="cart-item-total">₹${itemTotal.toFixed(2)}</div>
        <button type="button" class="cart-remove-btn" data-action="del" data-id="${item.id}" title="Remove item">&times;</button>
      `;

      cartItemsList.appendChild(row);
    });

    // Tax calculation
    const sgst = subtotal * 0.09;
    const cgst = subtotal * 0.09;
    const totalAmount = subtotal + sgst + cgst;

    if (cartCountBadge) cartCountBadge.textContent = `${totalItems} item${totalItems > 1 ? 's' : ''}`;
    if (subtotalEl) subtotalEl.textContent = `₹${subtotal.toFixed(2)}`;
    if (sgstEl) sgstEl.textContent = `₹${sgst.toFixed(2)}`;
    if (cgstEl) cgstEl.textContent = `₹${cgst.toFixed(2)}`;
    if (totalEl) totalEl.textContent = `₹${totalAmount.toFixed(2)}`;
    if (btnGenerateBill) btnGenerateBill.disabled = false;

    // Attach listeners on newly rendered cart buttons
    cartItemsList.querySelectorAll('.qty-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const id = parseInt(btn.dataset.id);
        const action = btn.dataset.action;
        updateQuantity(id, action === 'inc' ? 1 : -1);
      });
    });

    cartItemsList.querySelectorAll('.cart-remove-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const id = parseInt(btn.dataset.id);
        removeFromCart(id);
      });
    });
  }

  // Payment method pill selection
  const paymentPills = document.querySelectorAll('.payment-pill');
  paymentPills.forEach(pill => {
    pill.addEventListener('click', () => {
      paymentPills.forEach(p => p.classList.remove('selected'));
      pill.classList.add('selected');
      const radio = pill.querySelector('input[type="radio"]');
      if (radio) radio.checked = true;
    });
  });

  // Category chips filtering
  const chips = document.querySelectorAll('.category-chips .chip-btn');
  chips.forEach(chip => {
    chip.addEventListener('click', () => {
      chips.forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      filterProducts();
    });
  });

  // Live search input filtering
  const searchInput = document.getElementById('billing-product-search');
  if (searchInput) {
    searchInput.addEventListener('input', () => {
      filterProducts();
    });
  }

  function filterProducts() {
    const activeChip = document.querySelector('.category-chips .chip-btn.active');
    const selectedCategory = activeChip ? activeChip.dataset.category : 'all';
    const query = searchInput ? searchInput.value.trim().toLowerCase() : '';

    productCards.forEach(card => {
      const cardCategory = card.dataset.category.toLowerCase();
      const cardName = card.dataset.name.toLowerCase();

      const matchesCat = (selectedCategory === 'all' || cardCategory === selectedCategory.toLowerCase());
      const matchesSearch = (query === '' || cardName.includes(query));

      if (matchesCat && matchesSearch) {
        card.style.display = 'flex';
      } else {
        card.style.display = 'none';
      }
    });
  }

  // Generate Bill POST
  if (btnGenerateBill) {
    btnGenerateBill.addEventListener('click', async () => {
      const nameInput = document.getElementById('cust-name');
      const mobileInput = document.getElementById('cust-mobile');
      const selectedPayment = document.querySelector('input[name="payment_method"]:checked');

      const customerName = nameInput ? nameInput.value.trim() : '';
      const customerMobile = mobileInput ? mobileInput.value.trim() : '';
      const paymentMethod = selectedPayment ? selectedPayment.value : 'Cash';

      if (!customerName) {
        alert('Please enter Customer Full Name.');
        if (nameInput) nameInput.focus();
        return;
      }

      if (!customerMobile) {
        alert('Please enter Customer Mobile Number.');
        if (mobileInput) mobileInput.focus();
        return;
      }

      if (cart.length === 0) {
        alert('Cart is empty. Please select products.');
        return;
      }

      btnGenerateBill.disabled = true;
      btnGenerateBill.textContent = 'Generating Invoice...';

      const payload = {
        customer_name: customerName,
        customer_mobile: customerMobile,
        payment_method: paymentMethod,
        items: cart.map(item => ({
          product_id: item.id,
          quantity: item.quantity
        }))
      };

      try {
        const csrfToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content') || '';
        const headers = {
          'Content-Type': 'application/json'
        };
        if (csrfToken) {
          headers['X-CSRFToken'] = csrfToken;
        }

        const res = await fetch('/billing/create', {
          method: 'POST',
          headers: headers,
          body: JSON.stringify(payload)
        });

        const data = await res.json();

        if (res.ok && data.success) {
          window.location.href = data.redirect_url;
        } else {
          alert(data.message || 'Error occurred while creating bill.');
          btnGenerateBill.disabled = false;
          btnGenerateBill.textContent = 'Generate Bill & Receipt';
        }
      } catch (err) {
        console.error('Checkout error:', err);
        alert('Network or server error while generating bill. Please try again.');
        btnGenerateBill.disabled = false;
        btnGenerateBill.textContent = 'Generate Bill & Receipt';
      }
    });
  }
}

/* ==========================================
   5. Dashboard Charts (Chart.js)
   ========================================== */
function initDashboardCharts() {
  const revenueCanvas = document.getElementById('revenueChart');
  const categoryCanvas = document.getElementById('categoryPieChart');

  if (!revenueCanvas && !categoryCanvas) return;

  // 1. Revenue Chart
  let revenueChartInstance = null;

  async function loadRevenueChart(timeframe) {
    try {
      const res = await fetch(`/dashboard/api/revenue/${timeframe}`);
      if (!res.ok) throw new Error('Failed to load revenue data');
      const json = await res.json();

      if (revenueChartInstance) {
        revenueChartInstance.destroy();
      }

      const ctx = revenueCanvas.getContext('2d');
      revenueChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: json.labels,
          datasets: [{
            label: 'Revenue (₹)',
            data: json.values,
            backgroundColor: '#E87F24',
            hoverBackgroundColor: '#cf6d17',
            borderRadius: 6,
            borderSkipped: false
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
            tooltip: {
              callbacks: {
                label: (context) => ` Revenue: ₹${context.parsed.y.toLocaleString('en-IN', { minimumFractionDigits: 2 })}`
              }
            }
          },
          scales: {
            x: {
              grid: { display: false },
              ticks: { font: { family: 'Plus Jakarta Sans', size: 11, weight: '500' } }
            },
            y: {
              beginAtZero: true,
              grid: { color: '#f1f5f9' },
              ticks: {
                callback: (val) => `₹${val}`,
                font: { family: 'Plus Jakarta Sans', size: 11, weight: '500' }
              }
            }
          }
        }
      });
    } catch (err) {
      console.error('Error rendering revenue chart:', err);
    }
  }

  if (revenueCanvas) {
    loadRevenueChart('daily');

    const tabBtns = document.querySelectorAll('.chart-tab-btn');
    tabBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        tabBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const tf = btn.dataset.timeframe;
        loadRevenueChart(tf);
      });
    });
  }

  // 2. Sales by Category Doughnut Chart
  if (categoryCanvas) {
    async function loadCategoryChart() {
      try {
        const res = await fetch('/dashboard/api/category/sales');
        if (!res.ok) throw new Error('Failed to load category sales');
        const json = await res.json();

        const ctx = categoryCanvas.getContext('2d');
        const colors = [
          '#E87F24', // Orange
          '#FFC81E', // Yellow
          '#73A5CA', // Blue
          '#10B981', // Emerald
          '#6366F1', // Indigo
          '#EC4899', // Pink
          '#8B5CF6'  // Purple
        ];

        new Chart(ctx, {
          type: 'doughnut',
          data: {
            labels: json.labels,
            datasets: [{
              data: json.values,
              backgroundColor: colors,
              borderWidth: 2,
              borderColor: '#ffffff',
              hoverOffset: 6
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: {
                position: 'bottom',
                labels: {
                  boxWidth: 12,
                  font: { family: 'Plus Jakarta Sans', size: 11, weight: '500' }
                }
              },
              tooltip: {
                callbacks: {
                  label: (context) => ` ${context.label}: ₹${context.parsed.toLocaleString('en-IN', { minimumFractionDigits: 2 })}`
                }
              }
            },
            cutout: '65%'
          }
        });
      } catch (err) {
        console.error('Error rendering category chart:', err);
      }
    }

    loadCategoryChart();
  }

  // 3. Top Products Visualization
  const topProductsContainer = document.getElementById('top-products-container');
  if (topProductsContainer) {
    async function loadTopProducts() {
      try {
        const res = await fetch('/dashboard/api/top/products');
        if (!res.ok) throw new Error('Failed to fetch top products');
        const json = await res.json();

        topProductsContainer.innerHTML = '';
        if (json.labels.length === 0) {
          topProductsContainer.innerHTML = '<p class="text-muted" style="font-size:0.85rem; padding:10px 0;">No sales recorded yet.</p>';
          return;
        }

        const maxRev = Math.max(...json.revenues, 1);

        json.labels.forEach((name, idx) => {
          const rev = json.revenues[idx];
          const units = json.units[idx];
          const pct = Math.round((rev / maxRev) * 100);

          const itemEl = document.createElement('div');
          itemEl.className = 'top-product-item';
          itemEl.innerHTML = `
            <div class="tp-info">
              <span class="tp-name">${idx + 1}. ${name} (${units} pcs)</span>
              <span class="tp-revenue">₹${rev.toLocaleString('en-IN', { minimumFractionDigits: 2 })}</span>
            </div>
            <div class="tp-bar-bg">
              <div class="tp-bar-fill" style="width: ${pct}%;"></div>
            </div>
          `;
          topProductsContainer.appendChild(itemEl);
        });
      } catch (err) {
        console.error('Error fetching top products:', err);
      }
    }

    loadTopProducts();
  }
}
