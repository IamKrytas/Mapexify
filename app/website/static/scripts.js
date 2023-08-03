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