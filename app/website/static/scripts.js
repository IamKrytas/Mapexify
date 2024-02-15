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


// Funkcja do pobierania danych z LocalStorage
function getPointsFromLocalStorage() {
  const dataFromLocalStorage = localStorage.getItem("Points");
  return dataFromLocalStorage ? JSON.parse(dataFromLocalStorage) : null;
}

// Funkcja do zapisywania danych do LocalStorage
function saveDataToLocalStorage(data) {
  localStorage.setItem("Points", JSON.stringify(data));
}

// Funkcja do generowania elementów listy
function generateListItems(data) {
  const list = document.getElementById("plan");
  list.innerHTML = "";

  const h2 = document.createElement("h2");
  h2.textContent = "Points plan:";
  list.appendChild(h2);

  data.forEach((item, index) => {
    const listItem = document.createElement("li");
    addNameToItem(item, listItem);
    addButtonsToItem(index, data.length, listItem);
    list.appendChild(listItem);
  });
}

// Funkcja do dodawania nazwy do elementu listy
function addNameToItem(item, listItem) {
  const nameSpan = document.createElement("span");
  nameSpan.textContent = item.formattedAddress;
  listItem.appendChild(nameSpan);
}

// Funkcja do dodawania przycisków do elementu listy
function addButtonsToItem(index, dataLength, listItem) {
  const buttonsDiv = document.createElement("div");
  buttonsDiv.classList.add("buttons-container");

  if (index < dataLength - 1) {
    addButton("V", "changeOrder", () => changeOrder(index), buttonsDiv);
  }

  addButton("X", "deletePoint", () => deleteItem(index), buttonsDiv);

  listItem.appendChild(buttonsDiv);
}

// Funkcja do dodawania przycisku
function addButton(text, className, clickHandler, parentElement) {
  const button = document.createElement("button");
  button.textContent = text;
  button.classList.add(className);
  button.addEventListener("click", clickHandler);
  parentElement.appendChild(button);
}

// Funkcja do usuwania elementu z LocalStorage
function deleteItem(index) {
  const parsedData = getPointsFromLocalStorage();
  if (parsedData && index >= 0 && index < parsedData.length) {
    parsedData.splice(index, 1);
    saveDataToLocalStorage(parsedData);
    generateListItems(parsedData);
  } else {
    console.error("Invalid index:", index);
  }
}

// Funkcja do zmiany kolejności elementu
function changeOrder(index) {
  const jsonData = getPointsFromLocalStorage();
  if (jsonData && index < jsonData.length - 1) {
    const temp = jsonData[index];
    jsonData[index] = jsonData[index + 1];
    jsonData[index + 1] = temp;
    saveDataToLocalStorage(jsonData);
    generateListItems(jsonData);
  }
}

// Funkcja do wyświetlania trasy
function displayRoutePlan() {
  const jsonData = getPointsFromLocalStorage();

  if (jsonData !== null) {
    generateListItems(jsonData);
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


// Usuwanie wszyskich danych z LocalStorage
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
