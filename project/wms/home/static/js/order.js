    const ordersApp_listContainer = document.getElementById('ordersApp_ordersList');
    const ordersApp_details = document.getElementById('ordersApp_details');
    const ordersApp_itemsList = document.getElementById('ordersApp_itemsList');
    const ordersApp_cancelBtn = document.getElementById('ordersApp_cancelBtn');
    let ordersApp_currentOrder = null;
    let ordersApp_orders = [];

    async function ordersApp_fetchOrders() {
      try {
        const response = await fetch('/orders/get'); // ضع هنا رابط API الفعلي
        if (!response.ok) throw new Error('فشل تحميل الطلبات');
         let data= await response.json();
         ordersApp_orders = data.data
        console.log(ordersApp_orders)
        ordersApp_renderOrders();
      } catch (err) {
        ordersApp_listContainer.textContent = 'حدث خطأ أثناء تحميل الطلبات.';
        console.error(err);
      }
    }

    function ordersApp_renderOrders() {
      ordersApp_listContainer.innerHTML = '';
      ordersApp_orders.forEach(order => {
        const card = document.createElement('div');
        card.className = 'ordersApp_orderCard';
        card.innerHTML = `
          <div class="ordersApp_orderHeader">
            <div class="ordersApp_orderId">ORD-${order.id}</div>
            <div class="ordersApp_badge ${order.status}">${order.status}</div>
          </div>
          <div><strong>تاريخ الطلب :</strong>${order.date}</div>
        `;
        card.onclick = () => ordersApp_showDetails(order);
        ordersApp_listContainer.appendChild(card);
      });
    }

    function ordersApp_showDetails(order) {
      ordersApp_currentOrder = order;
      document.getElementById('ordersApp_d_id').textContent = 'ORD-'+order.id;
      const badge = document.getElementById('ordersApp_d_status');
      badge.textContent = order.status;
      badge.className = `ordersApp_detailValue ordersApp_badge ${order.status}`;
      document.getElementById('ordersApp_d_driver').textContent = order.driver_name;
      document.getElementById('ordersApp_d_phone').textContent = order.driver_phone;
      document.getElementById('ordersApp_d_email').textContent = order.driver_email;
      document.getElementById('ordersApp_d_date').textContent = order.date;

      ordersApp_itemsList.innerHTML = '<h3>العناصر المطلوبة:</h3>';
      order.items.forEach(item => {
        const div = document.createElement('div');
        div.className = 'ordersApp_item';
        div.innerHTML = `<span>[${item.color}]${item.name}</span><span>الكمية: ${item.qty}</span>`;
        ordersApp_itemsList.appendChild(div);
      });

      ordersApp_listContainer.style.display = 'none';
      ordersApp_details.style.display = 'block';
    }

    document.getElementById('ordersApp_backBtn').onclick = () => {
      ordersApp_details.style.display = 'none';
      ordersApp_listContainer.style.display = 'grid';
    };

    ordersApp_cancelBtn.onclick = async () => {
      if (!ordersApp_currentOrder) return;

      if (confirm('هل أنت متأكد أنك تريد إلغاء هذا الطلب؟')) {
        try {
          const response = await fetch(`/api/orders/${ordersApp_currentOrder.id}/cancel`, { method: 'POST' });
          if (!response.ok) throw new Error('فشل إلغاء الطلب');
          ordersApp_currentOrder.status = 'CANCELLED';
          alert('تم إلغاء الطلب.');
          ordersApp_details.style.display = 'none';
          ordersApp_renderOrders();
          ordersApp_listContainer.style.display = 'grid';
        } catch (err) {
          alert('حدث خطأ أثناء إلغاء الطلب');
          console.error(err);
        }
      }
    };

    ordersApp_fetchOrders();