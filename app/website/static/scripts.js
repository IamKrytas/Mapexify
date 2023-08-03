/* Scripts */


// Function to switch between tabs in navbar
function switchTab(tabName) {
  const tabContents = document.getElementsByClassName('tab-content');

  for (const tab of tabContents) {
    tab.style.display = 'none';
  }

  const tabToShow = document.getElementById(tabName + 'Tab');
  tabToShow.style.display = 'block';

  const buttons = document.getElementsByClassName('nav-btn');
  for (const button of buttons) {
    button.classList.remove('active');
  }
  event.currentTarget.classList.add('active');
}


// Function to save data in localStorage with a limit of 10 items
function saveToLocalStorage(data) {
  var storedData = localStorage.getItem('Points');
  var dataArray = storedData ? JSON.parse(storedData) : [];
  if (dataArray.length >= 10) {
    console.log('Cannot add more items. Limit of 10 reached.');
    return;
  }
  dataArray.push(data);
  localStorage.setItem('Points', JSON.stringify(dataArray));
}


// Function to fetch data from LocalStorage and display suggestions
function displaySuggestions() {
  const dataFromLocalStorage = localStorage.getItem("Points");
  if (dataFromLocalStorage !== null) {
    try {
      const jsonData = JSON.parse(dataFromLocalStorage);
      function generateListItems(data) {
        const list = document.getElementById("plan");
        data.forEach((item) => {
          const listItem = document.createElement("li");
          listItem.textContent = item.formattedAddress;
          list.appendChild(listItem);
        });
      }
      generateListItems(jsonData);
    } catch (error) {
      console.error("Error decoding JSON data:", error);
    }
  } else {
    console.log("No data in LocalStorage");
  }
}


// Function to send data to backend
function sendData() {
  const profileValue = document.querySelector('[name="profile"]').value;
  const currencyValue = document.querySelector('[name="currency"]').value;
  const localStorageData = localStorage.getItem('Points');

  const dataToSend = {
    profile: profileValue,
    currency: currencyValue,
    localStorageData: localStorageData
  };

  fetch('/toll', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(dataToSend)
  })
    .then(response => response.json())
    .then(data => {
      let currency = data.converted_currency;
      let price = data.converted_price;
      let distance = data.distance;
      let time = data.time;

      const distanceElement = document.getElementById('distance');
      const timeElement = document.getElementById('time');
      const priceElement = document.getElementById('price');

      distanceElement.innerHTML = `Distance: ${distance} km`;
      timeElement.innerHTML = `Travel time: ${time}`;
      priceElement.innerHTML = `Cost: ${price} ${currency}`;

      const resultContainer = document.getElementById("result");
      resultContainer.style.display = "block";
    })
    .catch(error => {
      console.error('Error:', error);
    });
}


// Function to clear local storage, points plan, result and map layer
function clearRoute() {
  localStorage.clear();

  const planDiv = document.getElementById("plan");
  const liElements = planDiv.getElementsByTagName("li");

  for (var i = liElements.length - 1; i >= 0; i--) {
    var li = liElements[i];
    li.parentNode.removeChild(li);
  }

  var mapLayer = map.getLayer('route');
  if (mapLayer) {
    map.removeLayer('route');
  } else {
    console.warn('Layer with given ID does not exist on the map.')
  }
  const resultContainer = document.getElementById("result");
  resultContainer.style.display = "none";

}

// Function to reset vehicle lists
function resetVehicleLists() {
  const selectElements = document.querySelectorAll('.vehicle-lists');

  for (let i = 0; i < selectElements.length; i++) {
    const selectElement = selectElements[i];
    if (selectElement.name === 'currency' || selectElement.name === 'profile') {
      selectElement.selectedIndex = 0;
    }
  }
}