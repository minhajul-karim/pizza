document.addEventListener("DOMContentLoaded", () => {
  alert("OOOOOOOOOO")
  const productCotainer = document.querySelector("#product-container");
  if (productCotainer) {
    const foodId = parseInt(window.location.pathname.split("/").pop());

    // Calculate price on page load
    calculatePrice();

    // Calculate price & display topping options on addon change
    document
      .querySelector("#select-addon")
      .addEventListener("change", (event) => {
        calculatePrice();
        if (foodId === 1 || foodId === 2) {
          switch (event.target.value) {
            case "1 topping":
              topping1Div.style.display = "block";
              topping1Select.disabled = false;
              topping2Div.style.display = "none";
              topping2Select.disabled = true;
              topping3Div.style.display = "none";
              topping3Select.disabled = true;
              break;
            case "2 toppings":
              topping1Div.style.display = "block";
              topping1Select.disabled = false;
              topping2Div.style.display = "block";
              topping2Select.disabled = false;
              topping3Div.style.display = "none";
              topping3Select.disabled = true;
              break;
            case "3 toppings":
              topping1Div.style.display = "block";
              topping1Select.disabled = false;
              topping2Div.style.display = "block";
              topping2Select.disabled = false;
              topping3Div.style.display = "block";
              topping3Select.disabled = false;
              break;
            default:
              topping1Div.style.display = "none";
              topping1Select.disabled = true;
              topping2Div.style.display = "none";
              topping2Select.disabled = true;
              topping3Div.style.display = "none";
              topping3Select.disabled = true;
          }
        }
      });

    const topping1Div = document.querySelector("#topping-1"),
      topping2Div = document.querySelector("#topping-2"),
      topping3Div = document.querySelector("#topping-3"),
      topping1Select = document.querySelector("#topping-options-1"),
      topping2Select = document.querySelector("#topping-options-2"),
      topping3Select = document.querySelector("#topping-options-3");

    if (topping1Select) topping1Select.disabled = true;
    if (topping2Select) topping2Select.disabled = true;
    if (topping3Select) topping3Select.disabled = true;

    // Variable to detect if price was incremented due to
    // extra cheese addition
    const cheeseSection = document.querySelector("#cheese-section");
    let priceIncremented = false;

    // Calculate price for small sizes, deselect extra cheese options
    // for subs
    const sizeSection = document.querySelector("#size-section");
    if (sizeSection) {
      document
        .querySelector("#inline-size-small")
        .addEventListener("change", () => {
          calculatePrice();
          if (cheeseSection) {
            deselectExtraCheeseButtons();
            priceIncremented = false;
          }
        });

      // Calculate prize for large sizes
      document
        .querySelector("#inline-size-large")
        .addEventListener("change", () => {
          calculatePrice();
          if (cheeseSection) {
            deselectExtraCheeseButtons();
            priceIncremented = false;
          }
        });
    }

    // Increment price for extra cheese with subs
    const priceSection = document.querySelector("#set-price"),
      hiddenPriceSection = document.querySelector("#hidden-price");
    if (cheeseSection) {
      document
        .querySelector("#cheese-yes")
        .addEventListener("change", (event) => {
          if (!priceIncremented) {
            let newPrice = (
              parseFloat(priceSection.textContent) + 0.5
            ).toFixed(2);
            priceSection.textContent = newPrice;
            hiddenPriceSection.value = newPrice;
            priceIncremented = true;
          }
        });

      // Decrement price for extra cheese with subs only if it was incremented before
      document
        .querySelector("#cheese-no")
        .addEventListener("change", (event) => {
          if (priceIncremented) {
            let newPrice = (
              parseFloat(priceSection.textContent) - 0.5
            ).toFixed(2);
            priceSection.textContent = newPrice;
            hiddenPriceSection.value = newPrice;
            priceIncremented = false;
          }
        });
    }

    /*
     * This function grabs food id, addon id, & size id, makes an AJAX call
     * and updates the price displayed on screen.
     */
    function calculatePrice() {
      const addon = document.querySelector("#select-addon"),
        size = document.querySelector("#size-section");
      let addonId = addon.options[addon.selectedIndex].dataset.addonId,
        sizeId = null,
        xhr = new XMLHttpRequest();

      // Add-on 18 is only served in large size.
      // So, display an alert message, disable small radio button,
      // & select the large one for add-on 18 only.
      if (size) {
        if (parseInt(addonId) === 18) {
          document.querySelector(
            "#inline-size-small"
          ).disabled = true;
          document.querySelector("#inline-size-large").checked = true;
          document.querySelector(".alert").style.display = "block";
        } else {
          // Hide alert & enable small radio button for other add-ons
          document.querySelector(".alert").style.display = "none";
          document.querySelector(
            "#inline-size-small"
          ).disabled = false;
        }
        sizeId = document.querySelector("#inline-size-small").checked
          ? 1
          : 2;
      }

      xhr.open("POST", "/tell-price");
      // Set CSRF token in the request header
      xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
      xhr.onload = () => {
        if (xhr.status >= 200 && xhr.status < 300) {
          let data = JSON.parse(xhr.responseText);
          const priceArea = document.querySelector("#set-price");
          // Update price on screen
          if (priceArea) {
            priceArea.textContent = data["price"];
            document.getElementById("hidden-food-id").value =
              foodId;
            document.getElementById("hidden-price").value =
              data["price"];
            document.getElementById("add-to-cart-btn").disabled = false;
          }
        } else {
          Error("Can not connect!");
        }
      };
      let data = new FormData();
      data.append("foodId", foodId);
      data.append("addonId", addonId);
      data.append("sizeId", sizeId);
      xhr.send(data);
    }
  }

  // Delete order from cart
  const cartContainer = document.querySelector("#cart-table");
  if (cartContainer) {
    document.querySelector("tbody").addEventListener("click", (event) => {
      if (event.target.nodeName === "path") {
        // Send the order id to server to delete order
        const orderRow = event.target.parentNode.parentNode.parentNode;
        const orderId = event.target.dataset.foodId;
        const xhr = new XMLHttpRequest();
        xhr.open("POST", "/delete-order");
        xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
        // Update cart information
        xhr.onload = () => {
          if (xhr.status >= 200 && xhr.status < 300) {
            const data = JSON.parse(xhr.responseText);
            // Hide the table row
            orderRow.style.display = "none";
            // Update price
            document.querySelector("#total-price").textContent =
              data["total_price"];
            // Update cart element count
            document.getElementById("order-count").textContent =
              data["remaining_orders"];
            // Hide order button and price when cart is empty
            if (data["remaining_orders"] === 0) {
              document.querySelector("#cart-table").innerHTML = `
                <p class="lead text-center mt-5">Your cart is currently empty!</p>
              `;
            }
          } else {
            Error("Can not connect!");
          }
        };
        let data = new FormData();
        data.append("orderId", orderId);
        xhr.send(data);
      }
    });
  }

  // Order confirmaiton for admin
  const ordersAdmin = document.querySelector("#orders-admin");
  if (ordersAdmin) {
    document.querySelector("tbody").addEventListener("click", (event) => {
      // When confirm button is pressssed, send the order id to the server
      // delete that order, disable the button and change status to completed
      if (event.target.nodeName === "BUTTON") {
        const orderRow = event.target.parentNode.parentNode;
        let orderId = orderRow.children[0].textContent,
          xhr = new XMLHttpRequest();
        xhr.open("POST", "/confirm-order-admin");
        xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
        xhr.onload = () => {
          if (xhr.status >= 200 && xhr.status < 300) {
            orderRow.children[9].textContent = "Completed";
            console.log(event.target)
            // orderRow.children[10].children[0].disabled = true;
          } else {
            Error("Error confirming order");
          }
        };
        let data = new FormData();
        data.append("orderId", orderId);
        xhr.send(data);
      }
      //
      const rows = document.querySelectorAll("tr");
    });
  }

  /*
   * This function deselects extra cheese radio buttons
   */
  function deselectExtraCheeseButtons() {
    if (document.querySelector("#cheese-yes").checked)
      document.querySelector("#cheese-yes").checked = false;
    if (document.querySelector("#cheese-no").checked)
      document.querySelector("#cheese-no").checked = false;
  }

  /*
   * This function retrieves CSRF cookie
   */
  function getCookie(name) {
    let cookieValue = null;
    // if (document.cookie && document.cookie !== "") {
    //   const cookies = document.cookie.split(";");
    //   for (let i = 0; i < cookies.length; i++) {
    //     const cookie = cookies[i].trim();
    //     // Does this cookie string begin with the name we want?
    //     if (cookie.substring(0, name.length + 1) === name + "=") {
    //       cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
    //       break;
    //     }
    //   }
    // }
    return cookieValue;
  }
});
