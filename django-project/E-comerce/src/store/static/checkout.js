
  function renderCheckout(orderId, data) {

    const container = document.getElementById(orderId);

    const total = data?.total || 0  ;

    container.innerHTML = `
      <div style="border:1px solid #c2bebe;color:red;padding:16px;border-radius:8px">

        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; font-size: 1.1rem;">
        <span>Total</span>
        <strong>$${total}</strong>
        </div>

        <label>
          <input type="radio" name="payment" value="card" checked />
          Card
        </label><br/>

        <label>
          <input type="radio" name="payment" value="cod" />
          Cash on delivery
        </label><br/><br/>

      </div>
    `;

  }

  window.DjangoCheckout = {
    render: renderCheckout
  };

