//const stripe = Stripe('pk_test_51LfjniBkHrOrPPqzFob0uyBP1AllpBmvNioBGMkP8dS9QcY6cKUx3umlbYq1SVB2kSi9dXxh8iDskrpSiuLSD3SN00ybrM7SIW');
const stripe = Stripe('pk_live_51LfjniBkHrOrPPqzuM6WfIXafq84CyWBKyRCuyilD3Fd4gnWksO6IZ857Rb78eBVhFeCUsMRar6jlbyr5Cury8dV00Y3HOHrvb');
$.ajaxSetup({async: false});
var token=localStorage.getItem('token')
const options = {
  clientSecret: '',
  // Fully customizable with appearance API.
  appearance: {/*...*/},
};
$.ajax({
    url: '/api/paymentdata',
    type: 'get',
    headers:{'Authorization': `Bearer ${token}`},
    dataType: 'json',
    contentType: 'application/json',
    success: function (data) {
      console.log(data);
      options.clientSecret=data.secret
    }
});

//'pi_3LQcfgAIj4VUJPcD3nPGvskF'
// Set up Stripe.js and Elements to use in checkout form, passing the client secret obtained in step 2
const elements = stripe.elements(options);

// Create and mount the Payment Element
const paymentElement = elements.create('payment');
paymentElement.mount('#payment-element');


const form = document.getElementById('payment-form');

form.addEventListener('submit', async (event) => {
  event.preventDefault();

  const {error} = await stripe.confirmPayment({
    //`Elements` instance that was used to create the Payment Element
    elements,
    confirmParams: {
      return_url: 'https://picupclean.com/order/webhook/',
    },
  });

  if (error) {
    // This point will only be reached if there is an immediate error when
    // confirming the payment. Show error to your customer (for example, payment
    // details incomplete)
    const messageContainer = document.querySelector('#error-message');
    messageContainer.textContent = error.message;
  } else {
    // Your customer will be redirected to your `return_url`. For some payment
    // methods like iDEAL, your customer will be redirected to an intermediate
    // site first to authorize the payment, then redirected to the `return_url`.
  }
});