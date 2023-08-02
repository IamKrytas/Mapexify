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

// Function to clear local storage, points plan and map layer
function clearStorage(layerId) {
  localStorage.clear();

  var planDiv = document.getElementById("plan");
  var liElements = planDiv.getElementsByTagName("li");

  for (var i = liElements.length - 1; i >= 0; i--) {
    var li = liElements[i];
    li.parentNode.removeChild(li);
  }

  var mapLayer = map.getLayer(layerId);
  if (mapLayer) {
    map.removeLayer(layerId);
  } else {
    console.warn('Layer with given ID does not exist on the map.')
  }
}
function resetVehicleLists() {
  const selectElements = document.querySelectorAll('.vehicle-lists');

  for (let i = 0; i < selectElements.length; i++) {
    const selectElement = selectElements[i];
    if (selectElement.name === 'currency' || selectElement.name === 'profile') {
      selectElement.selectedIndex = 0;
    }
  }
}