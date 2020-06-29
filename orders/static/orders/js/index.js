document.addEventListener('DOMContentLoaded', () => {
  const cheeseSection = document.querySelector('#cheese-section')
  let foodId = window.location.pathname.split('/').pop()
  // Display extra cheese option for subs
  parseInt(foodId) === 3
    ? (cheeseSection.style.display = 'block')
    : (cheeseSection.style.display = 'none')

  // Calculate price on page load
  calculatePrice()

  // Calculate price & display topping options on addon change
  document
    .querySelector('#select-addon')
    .addEventListener('change', (event) => {
      calculatePrice()
      const top1 = document.querySelector('#toppings-1'),
        top2 = document.querySelector('#toppings-2'),
        top3 = document.querySelector('#toppings-3')
      let selectedAddon = event.target.value
      switch (selectedAddon) {
        case '1 topping':
          top1.style.display = 'block'
          top2.style.display = 'none'
          top3.style.display = 'none'
          break
        case '2 toppings':
          top1.style.display = 'block'
          top2.style.display = 'block'
          top3.style.display = 'none'
          break
        case '3 toppings':
          top1.style.display = 'block'
          top2.style.display = 'block'
          top3.style.display = 'block'
          break
        default:
          top1.style.display = 'none'
          top2.style.display = 'none'
          top3.style.display = 'none'
      }
    })

  // Calculate price for small sizes
  document
    .querySelector('#inline-size-small')
    .addEventListener('change', () => {
      calculatePrice()
      // Deselect extra cheese buttons
      if (document.querySelector('#cheese-yes').checked)
        document.querySelector('#cheese-yes').checked = false
      if (document.querySelector('#cheese-no').checked)
        document.querySelector('#cheese-no').checked = false
    })

  // Calculate prize for large sizes
  document
    .querySelector('#inline-size-large')
    .addEventListener('change', () => {
      calculatePrice()
      // Deselect extra cheese buttons
      if (document.querySelector('#cheese-yes').checked)
        document.querySelector('#cheese-yes').checked = false
      if (document.querySelector('#cheese-no').checked)
        document.querySelector('#cheese-no').checked = false
    })

  // Increment price for extra cheese with subs
  let priceIncremented = false
  const priceSection = document.querySelector('#set-price')
  document.querySelector('#cheese-yes').addEventListener('change', (event) => {
    if (!priceIncremented) {
      priceSection.textContent = (
        parseFloat(priceSection.textContent) + parseFloat(event.target.value)
      ).toFixed(2)
      priceIncremented = true
    }
  })

  // Decrement price for extra cheese with subs only if it was incremented before
  document.querySelector('#cheese-no').addEventListener('change', (event) => {
    if (priceIncremented) {
      priceSection.textContent = (
        parseFloat(priceSection.textContent) + parseFloat(event.target.value)
      ).toFixed(2)
      priceIncremented = false
    }
  })

  /*
   * This function grabs food id, addon id, & size id, makes an AJAX call
   * and updates the price displayed on screen.
   */
  function calculatePrice() {
    const addon = document.querySelector('#select-addon'),
      size = document.querySelector('#size-section')
    let addonId = addon.options[addon.selectedIndex].dataset.addonId,
      sizeId = null,
      xhr = new XMLHttpRequest()

    // Add-on 18 is only served in large size.
    // So, display an alert message, disable small radio button,
    // & select the large one for add-on 18 only.
    if (size) {
      if (parseInt(addonId) === 18) {
        document.querySelector('#inline-size-small').disabled = true
        document.querySelector('#inline-size-large').checked = true
        document.querySelector('.alert').style.display = 'block'
      } else {
        // Hide alert & enable small radio button for other add-ons
        document.querySelector('.alert').style.display = 'none'
        document.querySelector('#inline-size-small').disabled = false
      }
      sizeId = document.querySelector('#inline-size-small').checked ? 1 : 2
    }

    xhr.open('POST', '/tell_price')
    // Set CSRF token in the request header
    xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'))
    xhr.onload = () => {
      if (xhr.status >= 200 && xhr.status < 300) {
        let data = JSON.parse(xhr.responseText)
        const priceArea = document.querySelector('#set-price')
        // Update price on screen
        if (priceArea) {
          priceArea.textContent = data['price']
        }
      } else {
        Error('Price not available')
      }
    }
    let data = new FormData()
    data.append('foodId', foodId)
    data.append('addonId', addonId)
    data.append('sizeId', sizeId)
    xhr.send(data)
  }

  /*
   * This function retrieves CSRF cookie
   */
  function getCookie(name) {
    let cookieValue = null
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';')
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim()
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === name + '=') {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
          break
        }
      }
    }
    return cookieValue
  }
})
