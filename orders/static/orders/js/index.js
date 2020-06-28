document.addEventListener('DOMContentLoaded', () => {
  // calculate price on page load
  const addon = document.querySelector('#select-addon'),
    size = document.querySelector('#size-section')
  let sizeId = null
  if (size) {
    sizeId = document.querySelector('#inline-size-small').checked ? 1 : 2
  }
  let foodId = window.location.pathname.split('/').pop(),
    addonId = addon.options[addon.selectedIndex].dataset.addonId,
    xhr = new XMLHttpRequest()
  xhr.open('POST', '/test')
  xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'))
  xhr.onload = () => {
    if (xhr.status >= 200 && xhr.status < 300) {
      let data = JSON.parse(xhr.responseText) // {price: "6.50"}
      const priceArea = document.querySelector('#set-price')
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
