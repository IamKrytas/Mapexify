/* Scripts */
function switchTab(tabName) {
  // Pobierz wszystkie elementy tab-content
  const tabContents = document.getElementsByClassName('tab-content');

  // Ukryj wszystkie elementy tab-content
  for (const tab of tabContents) {
    tab.style.display = 'none';
  }

  // Znajdź odpowiedni element tab-content i wyświetl go
  const tabToShow = document.getElementById(tabName + 'Tab');
  tabToShow.style.display = 'block';

  // Ustaw klasę aktywnego przycisku
  const buttons = document.getElementsByClassName('nav-btn');
  for (const button of buttons) {
    button.classList.remove('active');
  }
  event.currentTarget.classList.add('active');
}

function clearStorage(){
  localStorage.clear();
}